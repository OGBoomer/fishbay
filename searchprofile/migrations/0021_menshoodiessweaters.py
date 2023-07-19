# Generated by Django 4.1.7 on 2023-07-19 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searchprofile', '0020_alter_mensactiveweartop_place_holder_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MensHoodiesSweaters',
            fields=[
                ('genericmenstop_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='searchprofile.genericmenstop')),
                ('feature', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('searchprofile.genericmenstop',),
        ),
    ]
