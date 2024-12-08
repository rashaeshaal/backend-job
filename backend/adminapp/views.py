from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views import View
from .models import Industry, Role, JobPosting
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from accounts.models import State,City,JobApplication
import json

class JobPostingView(APIView):
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

        industry_name = request.GET.get('industry')  # Fetch industry from query params
        role_name = request.GET.get('role')  # Fetch role from query params

        jobs = JobPosting.objects.all()

        if industry_name:
            jobs = jobs.filter(job_industry__name__icontains=industry_name)  # Use __icontains for case-insensitive filtering

        if role_name:
            jobs = jobs.filter(job_role__name__icontains=role_name)  # Use __icontains for case-insensitive filtering

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

    def post(self, request):
        data = request.data  # Use request.data instead of request.POST
        try:
            industry = Industry.objects.get(id=data['industry_id'])
            role = Role.objects.get(id=data['role_id'])

            # Create the job posting
            job = JobPosting.objects.create(
                job_title=data['job_title'],
                job_description=data['job_description'],
                salary_min=data['salary_min'],
                salary_max=data['salary_max'],
                job_industry=industry,
                job_role=role
            )
            return JsonResponse({'message': 'Job created successfully!', 'job_id': job.id}, status=201)
        except Industry.DoesNotExist:
            return JsonResponse({'error': 'Invalid industry ID'}, status=400)
        except Role.DoesNotExist:
            return JsonResponse({'error': 'Invalid role ID'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)

    def put(self, request, job_id):
        data = request.data
        try:
            job = JobPosting.objects.get(id=job_id)
            job.job_title = data.get('job_title', job.job_title)
            job.job_description = data.get('job_description', job.job_description)
            job.salary_min = data.get('salary_min', job.salary_min)
            job.salary_max = data.get('salary_max', job.salary_max)
            job.job_industry = Industry.objects.get(id=data['industry_id'])
            job.job_role = Role.objects.get(id=data['role_id'])
            job.save()

            return JsonResponse({'message': 'Job updated successfully!'}, status=200)

        except JobPosting.DoesNotExist:
            return JsonResponse({'error': 'Job not found'}, status=404)
        except Industry.DoesNotExist:
            return JsonResponse({'error': 'Invalid industry ID'}, status=400)
        except Role.DoesNotExist:
            return JsonResponse({'error': 'Invalid role ID'}, status=400)
    def delete(self, request, job_id):
        try:
            job = JobPosting.objects.get(id=job_id)
            job.delete()
            return JsonResponse({'message': 'Job deleted successfully!'}, status=200)
        except JobPosting.DoesNotExist:
            return JsonResponse({'error': 'Job not found'}, status=404)
class AddStateAPIView(APIView):
    def get(self, request):
        states = State.objects.all()
        states_data = [{'id': state.id, 'name': state.name} for state in states]
        return Response(states_data)
    def post(self, request):
        data = request.data
        state_name = data.get('name')
        
        if not state_name:
            return Response({"error": "State name is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        state = State.objects.create(name=state_name)
        return Response({"message": "State added successfully", "state": state.name}, status=status.HTTP_201_CREATED)
    
    def put(self, request, state_id):
        state = get_object_or_404(State, id=state_id)
        state_name = request.data.get('name')
        
        if not state_name:
            return Response({"error": "State name is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        state.name = state_name
        state.save()
        return Response({"message": "State updated successfully", "state": state.name}, status=status.HTTP_200_OK)


    def delete(self, request, state_id):
        state = get_object_or_404(State, id=state_id)
        state.delete()
        return Response({"message": "State deleted successfully"}, status=status.HTTP_200_OK)


class AddCityAPIView(APIView):
    def post(self, request):
        data = request.data
        city_name = data.get('name')
        state_id = data.get('state_id')
        
        if not city_name or not state_id:
            return Response({"error": "City name and state ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        state = get_object_or_404(State, id=state_id)
        city = City.objects.create(name=city_name, state=state)
        return Response({"message": "City added successfully", "city": city.name}, status=status.HTTP_201_CREATED) 
    def put(self, request, city_id):
        city = get_object_or_404(City, id=city_id)
        data = request.data
        city_name = data.get('name')
        state_id = data.get('state_id')

        if not city_name or not state_id:
            return Response({"error": "City name and state ID are required."}, status=status.HTTP_400_BAD_REQUEST)

        state = get_object_or_404(State, id=state_id)
        city.name = city_name
        city.state = state
        city.save()

        # Send updated data back for confirmation
        return Response({"message": "City updated successfully", "city": {"name": city.name, "state_id": city.state.id}}, status=status.HTTP_200_OK)

    # Delete City
    def delete(self, request, city_id):
        city = get_object_or_404(City, id=city_id)
        city.delete()
        return Response({"message": "City deleted successfully"}, status=status.HTTP_200_OK)   
    
    
class IndustryAPIView(APIView): 
    def get(self,request):
        industries = Industry.objects.all()
        data = [{'id': industry.id, 'name': industry.name} for industry in industries]
        return Response(data)
    
    def post(self, request):
        name=request.data.get('name')
        if name:
            industry = Industry.objects.create(name=name)
            return Response({"message": "Industry added successfully", "industry": industry.name}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Industry name is required"}, status=status.HTTP_400_BAD_REQUEST) 
        
        
class RoleAPIView(APIView):
    def get(self, request):
        industry_id = request.GET.get('industry')
        
        if industry_id:
            try:
                industry_id = int(industry_id)  # Convert to integer
                roles = Role.objects.filter(industry_id=industry_id)
            except ValueError:
                return Response({"error": "Invalid industry ID"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            roles = Role.objects.all()
        
        data = [{'id': role.id, 'name': role.name, 'industry_id': role.industry.id} for role in roles]
        return Response(data)


    
    def post(self, request):
        name = request.data.get('name')
        industry_id = request.data.get('industry_id')
        if name and industry_id:
            industry = get_object_or_404(Industry, id=industry_id)
            role = Role.objects.create(name=name, industry=industry)
            return Response({'id': role.id, 'name': role.name}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Name and Industry ID are required'}, status=status.HTTP_400_BAD_REQUEST)



class JobApplicationView(APIView):
    def get(self, request):
        """
        Get all job applications
        """
        job_applications = JobApplication.objects.select_related('user', 'job_posting').all()
        
        # Create a list of dictionaries for the response
        applications_data = []
        for application in job_applications:
            applications_data.append({
                'id': application.id,
                'username': application.user.username,
                'email': application.user.email,
                'job_title': application.job_posting.job_title,
                'resume_url': request.build_absolute_uri(application.resume.url),
                'status': application.status,
                'applied_on': application.applied_on.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse(applications_data, safe=False)

    def put(self, request, application_id):
        """
        Update the status of a specific job application
        """
        try:
            # Get the job application by ID
            application = JobApplication.objects.get(id=application_id)
        except JobApplication.DoesNotExist:
            return HttpResponseNotFound('Job application not found.')

        try:
            # Parse JSON request body
            data = json.loads(request.body)
            new_status = data.get('status')

            if new_status not in ['Applied', 'Interview', 'Hired']:
                return HttpResponseBadRequest('Invalid status. Status must be one of: Applied, Interview, Hired.')

            # Update the status of the job application
            application.status = new_status
            application.save()

            return JsonResponse({
                'message': 'Status updated successfully',
                'id': application.id,
                'status': application.status
            })
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid JSON body.')

class SuperuserLoginView(APIView):
    # Allow any user (for now) to access this endpoint
    permission_classes = [AllowAny]

    def post(self, request):
        # Get username and password from the request body
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user using Django's authenticate function
        user = authenticate(username=username, password=password)
        
        if user is not None and user.is_superuser:
            # Log in the superuser
            login(request, user)
            return Response({'message': 'Login successful', 'status': 'success'})
        else:
            # If authentication fails or user is not a superuser
            return Response({'message': 'Invalid credentials or not a superuser', 'status': 'error'}, status=400)

        return JsonResponse({'message': 'Invalid request method', 'status': 'error'}, status=405)