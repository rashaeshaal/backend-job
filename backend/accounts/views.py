from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
import os
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.conf import settings
from .models import UserProfile, State,City,JobApplication
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from datetime import datetime
from django.shortcuts import get_object_or_404
from adminapp.models import JobPosting
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser, FormParser

class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data, 'hiii')

            full_name = data.get('full_name')
            email = data.get('email')
            gender = data.get('gender')
            phone_number = data.get('phone_number')
            state_id = data.get('state')
            city_id = data.get('city')
            date_of_birth = data.get('date_of_birth')
            terms_and_conditions = data.get('terms_and_conditions')
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            profile_picture = data.get('profile_picture') 

           
            if password != confirm_password:
                raise ValidationError("Passwords do not match.")

        
            if date_of_birth:
                date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
                if (datetime.now().date() - date_of_birth).days < 18 * 365:
                    raise ValidationError("You must be at least 18 years old.")

            
            if User.objects.filter(email=email).exists():
                raise ValidationError("A user with this email already exists.")

            # Create user
            user = User.objects.create(
                username=email, 
                email=email, 
                password=make_password(password)
            )

            
            user_profile = UserProfile.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                gender=gender,
                phone_number=phone_number,
                state_id=state_id,
                city_id=city_id,
                date_of_birth=date_of_birth,
                terms_and_conditions=terms_and_conditions,
                profile_picture=profile_picture 
            )

           
            return JsonResponse({"message": "User registered successfully!"}, status=201)

        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)
        




class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        print('Login Request Data:', request.data)
        try:
            data = request.data
            email = data.get('email')
            password = data.get('password')

           
            user = authenticate(username=email, password=password)

            if user is not None:
               
                return JsonResponse({
                    "message": "Login successful",
                    "user": {
                        "id": user.id,  
                        "email": user.email,
                        "full_name": user.userprofile.full_name,
        
                        "user_type": 1  
                    }
                }, status=status.HTTP_200_OK)
            else:
             
                return JsonResponse({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
class StateAPIView(APIView):

    def get(self, request):
        states = State.objects.all()
        state_list = [{"id": state.id, "name": state.name} for state in states]
        return Response(state_list)
    
class CityAPIView(APIView):

    def get(self, request, state_id):
        cities = City.objects.filter(state_id=state_id)
        city_list = [{"id": city.id, "name": city.name} for city in cities]
        return Response(city_list)  
    
class JobListingView(APIView):
    
    def get(self, request, job_id=None):
        if job_id:
            try:
                job = JobPosting.objects.get(id=job_id)
                job_data = {
                    'id': job.id,
                    'title': job.job_title,
                    'description': job.job_description,
                    'salary_min': job.salary_min,
                    'salary_max': job.salary_max,
                    'industry': job.job_industry.name,
                    'role': job.job_role.name,
                }
                return JsonResponse({'job': job_data}, status=200)
            except JobPosting.DoesNotExist:
                return JsonResponse({'error': 'Job not found'}, status=404)

        industry_name = request.GET.get('industry')  
        role_name = request.GET.get('role')  

        jobs = JobPosting.objects.all()

        if industry_name:
            jobs = jobs.filter(job_industry__name__icontains=industry_name)  

        if role_name:
            jobs = jobs.filter(job_role__name__icontains=role_name) 

        jobs_data = [
            {
                'id': job.id,
                'title': job.job_title,
                'description': job.job_description,
                'salary_min': job.salary_min,
                'salary_max': job.salary_max,
                'industry': job.job_industry.name,
                'role': job.job_role.name,
            }
            for job in jobs
        ]
        
        return JsonResponse({'jobs': jobs_data}, safe=False)
class ApplyJobView(APIView):
    def post(self, request, *args, **kwargs):
        data=request.data
        email = request.data.get('email')  
        job_posting_id = request.data.get('job_posting_id')
        resume = request.FILES.get('resume')
        print(resume)

      
        if not all([email, job_posting_id, resume]):
            print("Email, Job posting ID, and resume are required.")
            
            return JsonResponse({'error': 'Email, Job posting ID, and resume are required.'}, status=400)

       
        try:
            user_profile = UserProfile.objects.get(email=email)
            print(user_profile,"hiiiiiiiiiiiiiiii")
            user = user_profile.user 
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User with the provided email does not exist.'}, status=404)

        try:
            job_posting = JobPosting.objects.get(id=job_posting_id)
        except JobPosting.DoesNotExist:
            return JsonResponse({'error': 'Job posting does not exist.'}, status=404)

        if JobApplication.objects.filter(user=user, job_posting=job_posting).exists():
            return JsonResponse({'error': 'You have already applied for this job.'}, status=400)

       
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'job_applications/resumes/'))
        filename = fs.save(resume.name, resume)
        file_url = fs.url(filename)

        job_application = JobApplication.objects.create(
            user=user,
            job_posting=job_posting,
            resume=f'job_applications/resumes/{filename}',
            status='Applied'
        )

        return JsonResponse({
            'message': 'Application submitted successfully',
            'job_application_id': job_application.id
        }, status=201)


class UserJobApplicationsView(APIView):
    def get(self, request):
        """
        Get all job applications for the user by checking their email
        """
        email = request.GET.get('email') 
        if not email:
            return JsonResponse({'error': 'Email is required.'}, status=400)

        try:
            user_profile = UserProfile.objects.get(email=email)
            user = user_profile.user  
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'No user found with this email.'}, status=404)

        job_applications = JobApplication.objects.filter(user=user).select_related('job_posting')

        applications_list = [
            {
                'id': app.id,
                'job_title': app.job_posting.job_title,
                'status': app.status,
                'resume_url': app.resume.url if app.resume else None,
                'applied_on': app.applied_on.strftime('%d/%m/%Y')
            }
            for app in job_applications
        ]

        return JsonResponse(applications_list, safe=False)