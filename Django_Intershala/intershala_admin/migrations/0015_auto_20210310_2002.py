# Generated by Django 3.1.7 on 2021-03-10 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intershala_admin', '0014_intershalaadmin_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intershalaadmin',
            name='active',
            field=models.BooleanField(),
        ),
    ]