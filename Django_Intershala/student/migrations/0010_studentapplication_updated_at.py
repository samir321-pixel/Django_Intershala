# Generated by Django 3.1.7 on 2021-03-06 07:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_student_applied_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentapplication',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 3, 6, 7, 19, 37, 429457, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
