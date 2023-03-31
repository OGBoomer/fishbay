from django.urls import path
from . import views
app_name = 'brandprofile'

urlpatterns = [
    path('brandlist/', views.brand_profile_list, name='brand_profile_list'),
    path('brandprofile/<int:brand_id>', views.brand_profile_detail, name='brand_profile_detail'),
]
