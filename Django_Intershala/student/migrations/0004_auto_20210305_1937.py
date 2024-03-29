# Generated by Django 3.1.7 on 2021-03-05 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_student_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='other_links',
            field=models.URLField(blank=True, max_length=800, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='resume',
            field=models.URLField(default='www.google.com', max_length=800),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
