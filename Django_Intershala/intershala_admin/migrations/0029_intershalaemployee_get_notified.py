# Generated by Django 3.1.7 on 2021-03-23 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intershala_admin', '0028_auto_20210314_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='intershalaemployee',
            name='get_notified',
            field=models.BooleanField(default=True),
        ),
    ]
