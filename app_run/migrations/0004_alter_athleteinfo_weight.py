# Generated by Django 5.2 on 2025-07-13 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_run', '0003_athleteinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athleteinfo',
            name='weight',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
