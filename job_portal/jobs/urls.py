from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Home and dashboard
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Employer URLs
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('employer/post-job/', views.post_job, name='post_job'),
    path('employer/my-jobs/', views.my_jobs, name='my_jobs'),
    path('employer/job/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    
    # Applicant URLs
    path('applicant/dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('jobs/', views.job_list, name='job_list'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('applicant/my-applications/', views.my_applications, name='my_applications'),
]

