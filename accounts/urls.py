from django.urls import path

from accounts import views
from accounts.views import reset_password

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('resetpassword_validate/<uidb64>/<token>/', reset_password, name='reset_password'),
    path('forgotpassword/', views.forgot_password, name='forgot_password'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
]