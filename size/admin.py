from django.contrib import admin
from django.apps import apps

size_models = apps.get_app_config('size').get_models()

for model in size_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
