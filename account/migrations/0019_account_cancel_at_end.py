# Generated by Django 4.1.7 on 2023-08-24 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0018_account_sub_auto_renew"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="cancel_at_end",
            field=models.BooleanField(default=False),
        ),
    ]
