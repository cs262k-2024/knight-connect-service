# Generated by Django 5.1.3 on 2024-11-19 21:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('event', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
    ]
