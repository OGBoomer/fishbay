# Generated by Django 4.1.7 on 2023-07-20 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searchprofile', '0023_mensdressshirt'),
    ]

    operations = [
        migrations.CreateModel(
            name='MensTShirt',
            fields=[
                ('genericmenstop_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='searchprofile.genericmenstop')),
                ('place_holder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='searchprofile.searchresult')),
            ],
            options={
                'abstract': False,
            },
            bases=('searchprofile.genericmenstop',),
        ),
        migrations.CreateModel(
            name='MensSweater',
            fields=[
                ('genericmenstop_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='searchprofile.genericmenstop')),
                ('place_holder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='searchprofile.searchresult')),
            ],
            options={
                'abstract': False,
            },
            bases=('searchprofile.genericmenstop',),
        ),
    ]
