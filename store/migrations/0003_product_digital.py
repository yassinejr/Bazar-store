# Generated by Django 3.1.2 on 2020-12-16 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20201210_0138'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='digital',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Digital'),
        ),
    ]