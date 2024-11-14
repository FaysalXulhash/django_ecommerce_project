from django.urls import path
from accounts import views


urlpatterns = [
    path('register/', views.register, name='user-register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password-validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('email-info/', views.email_info, name='email_info'),  # just for show the email message

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
