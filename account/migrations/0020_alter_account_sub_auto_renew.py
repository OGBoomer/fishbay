# Generated by Django 4.1.7 on 2023-08-26 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_account_cancel_at_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='sub_auto_renew',
            field=models.BooleanField(default=False),
        ),
    ]
