# Generated by Django 4.1.7 on 2023-05-22 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0007_itemtype_identifier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='itemType',
            new_name='item_type',
        ),
    ]