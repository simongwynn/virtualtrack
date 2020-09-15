# Generated by Django 3.0.8 on 2020-08-14 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0006_auto_20200814_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='riders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('team_option', models.CharField(choices=[('Ind', 'Individual'), ('Team', 'Team')], default='Ind', max_length=4)),
                ('state', models.CharField(choices=[('ACT', 'ACT'), ('NSW', 'NSW'), ('NT', 'NT'), ('QLD', 'QLD'), ('SA', 'SA'), ('TAS', 'TAS'), ('VIC', 'VIC'), ('WA', 'WA')], default='NSW', max_length=3)),
                ('velodrome', models.CharField(choices=[('Dunc Gray Velo', 'Dunc Gray Velo'), ('NT Velo', 'NT Velo'), ('Anna Meares Velo', 'Anna Meares Velo'), ('Super-Dome', 'Super-Dome'), ('Silverdome', 'Silverdome'), ('DISC', 'DISC'), ('Speed Dome', 'Speed Dome')], default='Dunc Gray Velo', max_length=20)),
                ('team_member1', models.CharField(blank=True, max_length=50)),
                ('team_member2', models.CharField(blank=True, max_length=50)),
                ('team_member3', models.CharField(blank=True, max_length=50)),
                ('team_member4', models.CharField(blank=True, max_length=50)),
                ('agegroup', models.CharField(choices=[('JM15', 'JM15'), ('JW15', 'JW15'), ('JM17', 'JM17'), ('JW17', 'JW17'), ('JM19', 'JM19'), ('JW19', 'JW19'), ('ELITEM', 'ELITEM'), ('ELITEW', 'ELITEW')], default='JM15', max_length=6)),
                ('ip_time', models.DateTimeField(blank=True, null=True)),
                ('ip_temp', models.FloatField(blank=True, null=True)),
                ('ip_bp', models.FloatField(blank=True, null=True)),
                ('tt200_time', models.DateTimeField(blank=True, null=True)),
                ('tt200_temp', models.FloatField(blank=True, null=True)),
                ('tt200_bp', models.FloatField(blank=True, null=True)),
                ('ts_time', models.DateTimeField(blank=True, null=True)),
                ('ts_temp', models.FloatField(blank=True, null=True)),
                ('ts_bp', models.FloatField(blank=True, null=True)),
                ('tp_time', models.DateTimeField(blank=True, null=True)),
                ('tp_temp', models.FloatField(blank=True, null=True)),
                ('tp_bp', models.FloatField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='web',
        ),
    ]