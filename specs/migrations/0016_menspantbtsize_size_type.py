# Generated by Django 4.1.7 on 2023-06-10 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0015_rename_menpantbtsize_menspantbtsize_menspantsize'),
    ]

    operations = [
        migrations.AddField(
            model_name='menspantbtsize',
            name='size_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='specs.genericsizetype'),
            preserve_default=False,
        ),
    ]
