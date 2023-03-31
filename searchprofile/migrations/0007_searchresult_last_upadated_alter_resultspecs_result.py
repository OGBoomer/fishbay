# Generated by Django 4.1.7 on 2023-03-21 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searchprofile', '0006_rename_result_id_resultspecs_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchresult',
            name='last_upadated',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='resultspecs',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spec_line', to='searchprofile.searchresult'),
        ),
    ]
