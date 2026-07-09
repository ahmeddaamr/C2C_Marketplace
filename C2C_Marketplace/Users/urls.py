from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view() , name='register'),
    path('login/', views.LoginView.as_view() , name='login'),
    path('forget-password/', views.ForgetPasswordView.as_view() , name='forget-password'),
    path('logout/', views.LogoutView.as_view() , name='logout'),
    path('reset-password/',views.ResetPasswordView.as_view(),name='reset-password'),
    path('update/',views.UpdateUserView.as_view(),name='update'),
]
