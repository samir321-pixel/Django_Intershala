# Generated by Django 3.1.7 on 2021-03-10 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intershala_admin', '0013_auto_20210309_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='intershalaadmin',
            name='email',
            field=models.EmailField(default='admin@gmail.com', max_length=200),
            preserve_default=False,
        ),
    ]
