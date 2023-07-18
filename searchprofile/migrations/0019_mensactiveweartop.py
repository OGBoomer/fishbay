# Generated by Django 4.1.7 on 2023-07-18 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searchprofile', '0018_genericmensjacket_alter_genericmenspant_closure_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MensActivewearTop',
            fields=[
                ('genericmenstop_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='searchprofile.genericmenstop')),
                ('place_holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='searchprofile.searchresult')),
            ],
            options={
                'abstract': False,
            },
            bases=('searchprofile.genericmenstop',),
        ),
    ]
