# Generated by Django 4.1.7 on 2023-03-23 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('searchprofile', '0013_searchresult_search_url_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resultspecs',
            old_name='condition_name',
            new_name='spec_name',
        ),
        migrations.RenameField(
            model_name='resultspecs',
            old_name='condition_value',
            new_name='spec_value',
        ),
    ]
