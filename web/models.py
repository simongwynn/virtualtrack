from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Event(models.Model):
    name = models.CharField(null = True, max_length=100)
    date = models.DateField(null=True)
    finish = models.DateField(null=True)
    image = models.ImageField(upload_to='events/images/', null=True)
    National = 'Nat'
    NJTS = 'NJTS'
    event_option_choices = [
        (National, 'National'),
        (NJTS, 'NJTS')
    ]
    event_option = models.CharField(
        max_length=8,
        choices=event_option_choices,
        default=National
    )

    def __str__(self):
        return self.name

class rider(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=50)
    Individual = 'Ind'
    Team = 'Team'
    team_option_choices = [
        (Individual, 'Individual'),
        (Team, 'Team')
    ]
    team_option = models.CharField(
        max_length=4,
        choices=team_option_choices,
        default=Individual
    )
    ACT = 'ACT'
    NSW = 'NSW'
    NT = 'NT'
    QLD = 'QLD'
    SA = 'SA'
    TAS = 'TAS'
    VIC = 'VIC'
    WA = 'WA'

    state_option_choices = [
        (ACT, 'ACT'),
        (NSW, 'NSW'),
        (NT, 'NT'),
        (QLD, 'QLD'),
        (SA, 'SA'),
        (TAS, 'TAS'),
        (VIC, 'VIC'),
        (WA, 'WA'),
    ]
    state = models.CharField(
        max_length=3,
        choices=state_option_choices,
        default=NSW
    )
    velo1 = 'Dunc Gray Velodrome'
    velo2 = 'NT Velodrome'
    velo3 = 'Anna Meares Velodrome'
    velo4 = 'Super-Dome'
    velo5 = 'Silverdome'
    velo6 = 'DISC'
    velo7 = 'Speed Dome'
    velo_option_choices = [
        (velo1, 'Dunc Gray Velodrome'),
        (velo2, 'NT Velodrome'),
        (velo3, 'Anna Meares Velodrome'),
        (velo4, 'Super-Dome'),
        (velo5, 'Silverdome'),
        (velo6, 'DISC'),
        (velo7, 'Speed Dome'),
    ]
    velodrome = models.CharField(
        max_length=50,
         choices=velo_option_choices,
        default=velo1
    )

    team_member1 = models.CharField(max_length=50, blank=True)
    team_member2 = models.CharField(max_length=50, blank=True)
    team_member3 = models.CharField(max_length=50, blank=True)
    team_member4 = models.CharField(max_length=50, blank=True)


    jm15 = 'JM15'
    jw15 = 'JW15'
    jm17 = 'JM17'
    jw17 = 'JW17'
    jm19 = 'JM19'
    jw19 = 'JW19'
    elitem = 'ELITEM'
    elitew = 'ELITEW'
    parab = "Para-B"
    parac = "Para-C"
    age_option_choices = [
        (jm15, 'JM15'),
        (jw15, 'JW15'),
        (jm17, 'JM17'),
        (jw17, 'JW17'),
        (jm19, 'JM19'),
        (jw19, 'JW19'),
        (elitem, 'ELITEM'),
        (elitew, 'ELITEW'),
        (parab, 'PARA-B'),
        (parac, 'PARA-C'),
    ]
    agegroup = models.CharField(
        max_length=6,
        choices=age_option_choices,
        default=jm15
    )
    ip_time = models.CharField(max_length=2,null=True, blank=True)
    ip_time_second = models.CharField(max_length=6,null=True, blank=True)
    ip_time_total = models.FloatField(max_length=8,null=True, blank=True)
    ip_adjusted_time = models.CharField(max_length=8,null=True, blank=True)
    ip_adjusted_second = models.CharField(max_length=8,null=True, blank=True)
    ip_time_total_adjusted = models.FloatField(max_length=8,null=True, blank=True)
    ip_temp = models.FloatField(null=True, blank=True)
    ip_bp = models.FloatField(null=True, blank=True)
    ip_humdity = models.FloatField(null=True, blank=True)

    tt200_time = models.FloatField(max_length=10,null=True, blank=True)
    tt200_adjusted_time = models.FloatField(max_length=10,null=True, blank=True)
    tt200_temp = models.FloatField(null=True, blank=True)
    tt200_bp = models.FloatField(null=True, blank=True)
    tt200_humdity = models.FloatField(null=True, blank=True)

    ts_time = models.FloatField(max_length=10,null=True, blank=True)
    ts_adjusted_time = models.FloatField(max_length=10,null=True, blank=True)
    ts_temp = models.FloatField(null=True, blank=True)
    ts_bp = models.FloatField(null=True, blank=True)
    ts_humdity = models.FloatField(null=True, blank=True)
    ts_ineligable = models.BooleanField(default=False)

    tp_time = models.CharField(max_length=10,null=True, blank=True)
    tp_temp = models.CharField(max_length=10,null=True, blank=True)
    tp_time_second = models.CharField(max_length=6,null=True, blank=True)
    tp_time_total = models.FloatField(max_length=8, null=True, blank=True)
    tp_adjusted_time = models.CharField(max_length=8,null=True, blank=True)
    tp_adjusted_second = models.CharField(max_length=8,null=True, blank=True)
    tp_time_total_adjusted = models.FloatField(max_length=8,null=True, blank=True)
    tp_bp = models.FloatField(null=True, blank=True)
    tp_humdity = models.FloatField(null=True, blank=True)
    tp_ineligable = models.BooleanField(default=False)

    tt_time = models.CharField(max_length=2, null=True, blank=True)
    tt_time_second = models.CharField(max_length=6, null=True, blank=True)
    tt_time_total = models.FloatField(max_length=8, null=True, blank=True)
    tt_adjusted_time = models.CharField(max_length=8, null=True, blank=True)
    tt_adjusted_second = models.CharField(max_length=8, null=True, blank=True)
    tt_time_total_adjusted = models.FloatField(max_length=8, null=True, blank=True)
    tt_temp = models.FloatField(null=True, blank=True)
    tt_bp = models.FloatField(null=True, blank=True)
    tt_humdity = models.FloatField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    last_modified = models.DateTimeField(auto_now=True, editable=False, null=False, blank=False)
    user = models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event,null=True, on_delete=models.CASCADE, default=3)


    def __str__(self):
        riderdetails = str(self.number) + ' - ' + self.name + ' (' + self.state + ')' + ' - ' + str(self.event)
        return riderdetails

    class Meta(object):
        ordering = ['-event','-id']



