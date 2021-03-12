# Generated by Django 3.1.7 on 2021-03-12 15:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intershala_admin', '0026_companyreview'),
    ]

    operations = [
        migrations.RenameField(
            model_name='intershalacompany',
            old_name='rating',
            new_name='overall_rating',
        ),
        migrations.AddField(
            model_name='companyreview',
            name='rating',
            field=models.FloatField(default=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
            preserve_default=False,
        ),
    ]
