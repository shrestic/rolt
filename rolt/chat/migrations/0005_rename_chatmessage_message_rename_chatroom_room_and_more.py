# Generated by Django 5.1.8 on 2025-05-02 08:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_chatmessage_options_alter_chatroom_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChatMessage',
            new_name='Message',
        ),
        migrations.RenameModel(
            old_name='ChatRoom',
            new_name='Room',
        ),
        migrations.AlterModelOptions(
            name='message',
            options={},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={},
        ),
        migrations.AlterModelTable(
            name='message',
            table=None,
        ),
        migrations.AlterModelTable(
            name='room',
            table=None,
        ),
    ]
