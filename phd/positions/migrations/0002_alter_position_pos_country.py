# Generated by Django 4.1.5 on 2023-01-25 19:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('positions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='pos_country',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), null=True, size=None),
        ),
    ]
