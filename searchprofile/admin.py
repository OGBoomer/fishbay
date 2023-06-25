from django.contrib import admin
from django.apps import apps


searchprofile_models = apps.get_app_config('searchprofile').get_models()

for model in searchprofile_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
