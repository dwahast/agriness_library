# Generated by Django 3.2.6 on 2021-08-30 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_book_reserve'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='fees',
            field=models.FloatField(blank=True, null=True, verbose_name='fees'),
        ),
    ]
