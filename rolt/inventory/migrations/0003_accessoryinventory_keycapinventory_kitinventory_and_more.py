# Generated by Django 5.1.8 on 2025-05-08 03:37

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessories', '0003_alter_accessory_description'),
        ('components', '0003_keycap_description_kit_description_and_more'),
        ('inventory', '0002_rename_inventory_i_content_998fc6_idx_inventory_content_315cba_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessoryInventory',
            fields=[
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('accessory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='accessories.accessory')),
            ],
            options={
                'verbose_name': 'Accessory Inventory',
                'verbose_name_plural': 'Accessory Inventories',
                'db_table': 'accessory_inventory',
                'ordering': ['accessory__name'],
            },
        ),
        migrations.CreateModel(
            name='KeycapInventory',
            fields=[
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('keycap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='components.keycap')),
            ],
            options={
                'verbose_name': 'Keycap Inventory',
                'verbose_name_plural': 'Keycap Inventories',
                'db_table': 'keycap_inventory',
                'ordering': ['keycap__name'],
            },
        ),
        migrations.CreateModel(
            name='KitInventory',
            fields=[
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('kit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='components.kit')),
            ],
            options={
                'verbose_name': 'Kit Inventory',
                'verbose_name_plural': 'Kit Inventories',
                'db_table': 'kit_inventory',
                'ordering': ['kit__name'],
            },
        ),
        migrations.CreateModel(
            name='SwitchInventory',
            fields=[
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('switch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='components.switch')),
            ],
            options={
                'verbose_name': 'Switch Inventory',
                'verbose_name_plural': 'Switch Inventories',
                'db_table': 'switch_inventory',
                'ordering': ['switch__name'],
            },
        ),
        migrations.DeleteModel(
            name='Inventory',
        ),
    ]
