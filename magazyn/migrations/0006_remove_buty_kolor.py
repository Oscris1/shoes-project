# Generated by Django 3.1.5 on 2021-01-15 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magazyn', '0005_auto_20210113_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buty',
            name='kolor',
        ),
    ]