# Generated by Django 3.0.8 on 2020-08-14 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20200814_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='web',
            name='created',
        ),
        migrations.RemoveField(
            model_name='web',
            name='ip_bp',
        ),
        migrations.RemoveField(
            model_name='web',
            name='ip_temp',
        ),
        migrations.RemoveField(
            model_name='web',
            name='ip_time',
        ),
        migrations.RemoveField(
            model_name='web',
            name='last_modified',
        ),
        migrations.RemoveField(
            model_name='web',
            name='tp_bp',
        ),
        migrations.RemoveField(
            model_name='web',
            name='tp_temp',
        ),
        migrations.RemoveField(
            model_name='web',
            name='tp_time',
        ),
        migrations.RemoveField(
            model_name='web',
            name='ts_bp',
        ),
        migrations.RemoveField(
            model_name='web',
            name='ts_temp',
        ),
        migrations.RemoveField(
            model_name='web',
            name='ts_time',
        ),
        migrations.RemoveField(
            model_name='web',
            name='tt200_bp',
        ),
        migrations.RemoveField(
            model_name='web',
            name='tt200_temp',
        ),
        migrations.RemoveField(
            model_name='web',
            name='tt200_time',
        ),
    ]