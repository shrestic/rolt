# Generated by Django 5.1.8 on 2025-05-07 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='inventory',
            new_name='inventory_content_315cba_idx',
            old_name='inventory_i_content_998fc6_idx',
        ),
        migrations.AlterModelTable(
            name='inventory',
            table='inventory',
        ),
    ]
