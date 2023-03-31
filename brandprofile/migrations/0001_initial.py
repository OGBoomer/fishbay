# Generated by Django 4.1.7 on 2023-03-26 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            options={
                'ordering': ['name'],
            },
        ),
    ]
