from django.urls import path
from . import views
app_name = 'category'

urlpatterns = [
    path('categorylist/', views.category_list, name='category_list'),
    path('addrootnode/', views.category_add_root, name='category_add_root'),
    path('addchildnode/<int:parent_id>/', views.category_add_child, name='category_add_child'),
]
