# Generated by Django 3.1.7 on 2021-03-06 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intershala_admin', '0003_intershalaemployee_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intershalaemployee',
            name='Address',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='intershalaemployee',
            name='city',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]