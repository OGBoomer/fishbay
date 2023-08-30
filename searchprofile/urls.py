from django.urls import path
from . import views
app_name = 'searchprofile'

urlpatterns = [
    path('profilelist/', views.profile_list, name='profile_list'),
    path('brandlist/', views.brand_list, name='brand_list'),
    path('update_profile_list/', views.update_profile_list, name='update_profile_list'),
    path('update_result_list/<int:profile_id>', views.update_result_list, name='update_result_list'),
    path('updatesearch/<int:search_id>', views.update_search, name='update_search'),
    path('update_model_list/<int:profile_id>', views.update_model_list, name='update_model_list'),
    path('update_brand_list/', views.update_brand_list, name='update_brand_list'),
    path('profiledetail/<int:profile_id>', views.profile_detail, name='profile_detail'),
    path('branddetail/<int:brand_id>', views.brand_detail, name='brand_detail'),
    path('modeldetail/<int:profile_id>', views.model_detail, name='model_detail'),
    path('delete_profile/<int:profile_id>', views.delete_profile, name='delete_profile'),
    path('delete_brand/<int:brand_id>', views.delete_brand, name='delete_brand'),
    path('deletemodel/<int:profile_id>/<int:model_id>', views.delete_model, name='delete_model'),
    path('deletesearch/<int:search_id>/', views.delete_search, name='delete_search'),
    path('check_notice/', views.check_notice, name='check_notice'),
    path('createsearch/', views.create_search, name='create_search'),
    path('updatesize/', views.update_size, name='update_size'),

    # path('addmodel/<int:profile_id>', views.add_model, name='add_model'),


    path('jplay/', views.jplay, name='jplay'),
]
