# Generated by Django 3.1.2 on 2020-11-15 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20201115_2201'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='coast',
        ),
    ]