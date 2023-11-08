# Generated by Django 4.1.7 on 2023-10-31 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0041_womensneckline'),
    ]

    operations = [
        migrations.CreateModel(
            name='DressStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, unique=True)),
                ('code', models.CharField(max_length=100)),
            ],
        ),
    ]
