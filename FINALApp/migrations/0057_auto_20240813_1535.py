# Generated by Django 3.2.25 on 2024-08-13 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FINALApp', '0056_payment_upi_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.CharField(max_length=255)),
                ('to_user', models.CharField(max_length=255)),
                ('chat', models.TextField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['datetime'],
            },
        ),
        migrations.DeleteModel(
            name='ChatMessage',
        ),
    ]
