# Generated by Django 4.1.7 on 2023-08-16 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_remove_stripepayment_profile_stripepayment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stripepayment',
            old_name='user',
            new_name='profile',
        ),
    ]
