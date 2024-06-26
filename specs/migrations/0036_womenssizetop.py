# Generated by Django 4.1.7 on 2023-10-25 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0035_rename_sizetype_womenssizetype'),
    ]

    operations = [
        migrations.CreateModel(
            name='WomensSizeTop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, unique=True)),
                ('code', models.CharField(max_length=100)),
                ('size_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Womenssizetype', to='specs.genericsizetype')),
            ],
        ),
    ]
