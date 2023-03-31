from django.urls import path
from . import views
app_name = 'searchprofile'

urlpatterns = [
    path('profilelist/', views.profile_list, name='profile_list'),
    path('createprofile/', views.create_profile, name='create_profile'),
    path('profiledetail/<int:profile_id>', views.profile_detail, name='profile_detail'),
    path('createsearch/', views.create_search, name='create_search'),
    path('deletesearch/<int:search_id>', views.delete_search, name='delete_search'),
    path('updatesearch/<int:search_id>', views.update_search, name='update_search'),
    path('jplay/', views.jplay, name='jplay'),
]
