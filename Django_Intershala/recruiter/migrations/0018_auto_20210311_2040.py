# Generated by Django 3.1.7 on 2021-03-11 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intershala_admin', '0024_auto_20210311_2032'),
        ('recruiter', '0017_remove_recruiter_intershala_authorize'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiter',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='recruiter_company', to='intershala_admin.intershalacompany'),
        ),
    ]
