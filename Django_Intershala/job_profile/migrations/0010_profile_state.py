# Generated by Django 3.1.7 on 2021-03-05 14:12

from django.db import migrations
import localflavor.in_.models


class Migration(migrations.Migration):

    dependencies = [
        ('job_profile', '0009_auto_20210305_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='state',
            field=localflavor.in_.models.INStateField(blank=True, max_length=2, null=True),
        ),
    ]