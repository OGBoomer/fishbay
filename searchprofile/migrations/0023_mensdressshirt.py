# Generated by Django 4.1.7 on 2023-07-19 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searchprofile', '0022_rename_menshoodiessweaters_menshoodiessweatshirts'),
    ]

    operations = [
        migrations.CreateModel(
            name='MensDressShirt',
            fields=[
                ('genericmenstop_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='searchprofile.genericmenstop')),
                ('neck_size', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('searchprofile.genericmenstop',),
        ),
    ]