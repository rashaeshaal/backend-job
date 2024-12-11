
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from .views import JobPostingView,AddStateAPIView,AddCityAPIView,IndustryAPIView,RoleAPIView,JobApplicationView,RolelistView,SuperuserLoginView

urlpatterns = [
    path('jobs/', JobPostingView.as_view(), name='job_list_create'),  
    path('jobs/<int:job_id>/', JobPostingView.as_view(), name='job_update_delete'),
    path('add-state/', AddStateAPIView.as_view(), name='add-state'),
    path('add-city/', AddCityAPIView.as_view(), name='add-city'),
    path('industries/', IndustryAPIView.as_view(), name='industries'),
    path('roles/', RoleAPIView.as_view(), name='roles'),
    path('states/', AddStateAPIView.as_view(), name='add_state'),  
    path('states/<int:state_id>/', AddStateAPIView.as_view(), name='state_update_delete'),
    path('states/<int:state_id>/', AddStateAPIView.as_view(), name='update_state'),
    path('cities/<int:city_id>/', AddCityAPIView.as_view(), name='delete_city'),
    path('citiesed/<int:city_id>/', AddCityAPIView.as_view(), name='update_city'),
    path('job-applications/', JobApplicationView.as_view(), name='job_applications_list'),
    path('job-applications/<int:application_id>/', JobApplicationView.as_view(), name='update-job-application'),
    path('superuser-login/', SuperuserLoginView.as_view(), name='superuser-login'),
    path('roleli/',RolelistView.as_view(),name='rolelist'),


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
