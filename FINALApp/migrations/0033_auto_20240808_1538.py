# Generated by Django 3.2.25 on 2024-08-08 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FINALApp', '0032_chat_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
