# Generated by Django 4.1.7 on 2023-03-20 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('searchprofile', '0005_searchresult_resultspecs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resultspecs',
            old_name='result_id',
            new_name='result',
        ),
    ]
