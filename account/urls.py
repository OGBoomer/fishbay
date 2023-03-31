from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('login/', views.loginpage, name='loginpage'),
    path('register/', views.register, name='register'),
]

