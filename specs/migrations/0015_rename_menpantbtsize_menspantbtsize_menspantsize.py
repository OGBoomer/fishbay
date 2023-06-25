# Generated by Django 4.1.7 on 2023-06-10 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0014_menspantwaistsize_rename_menswaistsize_menpantbtsize_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MenPantBTSize',
            new_name='MensPantBTSize',
        ),
        migrations.CreateModel(
            name='MensPantSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, unique=True)),
                ('code', models.CharField(max_length=100)),
                ('size_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='specs.genericsizetype')),
            ],
        ),
    ]