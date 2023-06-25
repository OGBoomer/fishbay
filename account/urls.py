from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('', views.loginpage, name='loginpage'),
    path('login/', views.loginpage, name='loginpage'),
    path('register/', views.register, name='register'),
    path('logoutpage/', views.logoutpage, name='logoutpage'),
    path('home/', views.homepage, name='homepage'),
]
