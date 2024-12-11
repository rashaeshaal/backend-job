from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from .views import UserRegisterView,StateAPIView,CityAPIView,UserLoginView,ApplyJobView,JobListingView,UserJobApplicationsView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('states/', StateAPIView.as_view(), name='states'),
    path('citiesl/<int:state_id>/', CityAPIView.as_view(), name='cities'),
    path('handlelogin/', UserLoginView.as_view(), name='login'),
    path('apply/', ApplyJobView.as_view(), name='apply-for-job'),
    path('joblist/', JobListingView.as_view(), name='job_list_create'),
    path('user-job-applications/', UserJobApplicationsView.as_view(), name='user-job-applications'), 

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
