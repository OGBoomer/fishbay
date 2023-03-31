from django.contrib import admin
from django.apps import apps

specs_models = apps.get_app_config('specs').get_models()

for model in specs_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
