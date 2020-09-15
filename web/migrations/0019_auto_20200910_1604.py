# Generated by Django 3.0.8 on 2020-09-10 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0018_auto_20200910_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='rider',
            name='ip_adjusted_second',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='rider',
            name='ip_adjusted_time',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='rider',
            name='ip_time_total_adjusted',
            field=models.FloatField(blank=True, max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='rider',
            name='tp_adjusted_second',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='rider',
            name='tp_adjusted_time',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='rider',
            name='tp_time_total_adjusted',
            field=models.FloatField(blank=True, max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='rider',
            name='ts_adjusted_time',
            field=models.FloatField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='rider',
            name='tt200_adjusted_time',
            field=models.FloatField(blank=True, max_length=10, null=True),
        ),
    ]