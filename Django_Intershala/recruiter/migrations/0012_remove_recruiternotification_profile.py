# Generated by Django 3.1.7 on 2021-03-06 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0011_recruiternotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruiternotification',
            name='profile',
        ),
    ]
