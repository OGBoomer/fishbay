# Generated by Django 4.1.7 on 2023-07-16 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchprofile', '0015_alter_searchresult_heading'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericmenspant',
            name='closure',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
