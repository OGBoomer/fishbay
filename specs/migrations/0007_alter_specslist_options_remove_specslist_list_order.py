# Generated by Django 4.1.7 on 2023-04-08 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0006_menjeansbtsize_menjeansregsize_menjeanswaistsize'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specslist',
            options={},
        ),
        migrations.RemoveField(
            model_name='specslist',
            name='list_order',
        ),
    ]
