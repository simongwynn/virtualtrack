# Generated by Django 3.0.8 on 2020-08-14 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20200814_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rider',
            name='ip_time',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
