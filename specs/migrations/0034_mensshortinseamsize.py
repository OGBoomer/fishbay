# Generated by Django 4.1.7 on 2023-09-04 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0033_mensshirtnecksize'),
    ]

    operations = [
        migrations.CreateModel(
            name='MensShortInseamSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, unique=True)),
                ('code', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
