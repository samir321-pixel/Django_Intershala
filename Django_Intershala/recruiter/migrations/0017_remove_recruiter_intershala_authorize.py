# Generated by Django 3.1.7 on 2021-03-08 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0016_recruiter_intershala_authorize'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recruiter',
            name='intershala_authorize',
        ),
    ]
