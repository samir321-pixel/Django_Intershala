# Generated by Django 3.1.7 on 2021-03-06 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intershala_admin', '0004_auto_20210306_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intershalaemployee',
            name='image',
            field=models.ImageField(upload_to='Employee/Image'),
        ),
        migrations.AlterField(
            model_name='intershalaemployee',
            name='resume',
            field=models.FileField(upload_to='Employee/Resume'),
        ),
    ]
