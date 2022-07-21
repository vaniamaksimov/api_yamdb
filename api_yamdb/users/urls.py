from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('token/', views.ConfirmRegisteredView.as_view()),
    path('signup/', views.SignupView.as_view()),
    path('users/', views.CreateUserAdmView.as_view())
]
