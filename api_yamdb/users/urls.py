from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('users/', views.SignupView.as_view()),
    path('auth/token/', views.ConfirmRegisteredView.as_view()),
    path('auth/signup/', views.SignupView.as_view())]
