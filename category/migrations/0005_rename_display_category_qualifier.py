# Generated by Django 4.1.7 on 2023-05-18 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_alter_category_display'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='display',
            new_name='qualifier',
        ),
    ]