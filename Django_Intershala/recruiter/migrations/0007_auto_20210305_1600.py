# Generated by Django 3.1.7 on 2021-03-05 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0006_auto_20210305_1558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recruiter',
            old_name='Address',
            new_name='company_address',
        ),
    ]
