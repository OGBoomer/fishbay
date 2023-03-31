# Generated by Django 4.1.7 on 2023-03-18 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0008_delete_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('keyword', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
