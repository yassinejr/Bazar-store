# Generated by Django 3.1.2 on 2020-12-10 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(null=True, verbose_name='Stock'),
        ),
    ]
