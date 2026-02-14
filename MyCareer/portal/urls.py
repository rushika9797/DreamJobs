from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path("dashboard/", views.dashboard, name="dashboard"),

    path('post-job/', views.post_job, name='post_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),
    path("approve/<int:app_id>/", views.approve_application, name="approve_application"),
    path("reject/<int:app_id>/", views.reject_application, name="reject_application"),
]
