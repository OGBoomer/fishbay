# Generated by Django 4.1.7 on 2023-10-26 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0037_rename_womenssizetop_womenstopsize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='womenstopsize',
            name='size_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Womenssizetype', to='specs.womenssizetype'),
        ),
    ]