# Generated by Django 4.1.7 on 2023-06-06 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0013_rename_genericsizes_genericsize'),
    ]

    operations = [
        migrations.CreateModel(
            name='MensPantWaistSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, unique=True)),
                ('code', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.RenameModel(
            old_name='MensWaistSize',
            new_name='MenPantBTSize',
        ),
        migrations.RenameModel(
            old_name='MensPantsInseam',
            new_name='MensPantInseam',
        ),
        migrations.DeleteModel(
            name='BigTallSize',
        ),
        migrations.DeleteModel(
            name='MenJeansBTSize',
        ),
        migrations.DeleteModel(
            name='MenJeansRegSize',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
        migrations.AlterModelOptions(
            name='menpantbtsize',
            options={},
        ),
    ]