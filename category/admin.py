from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['tree_id', 'qualifier', 'name', 'code', 'parent']


admin.site.register(ItemType)
