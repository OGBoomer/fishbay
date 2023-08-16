# Generated by Django 4.1.7 on 2023-08-16 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0003_rename_user_stripepayment_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="stripepayment",
            name="user",
            field=models.ForeignKey(
                blank=True,
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="doomed",
                to="account.accountprofile",
            ),
            preserve_default=False,
        ),
    ]
