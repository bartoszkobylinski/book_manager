# Generated by Django 3.1.3 on 2020-11-07 20:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_manager', '0002_auto_20201106_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.URLField(blank=True, validators=[django.core.validators.URLValidator]),
        ),
    ]
