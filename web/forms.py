from django.forms import ModelForm
from .models import rider


class PursuitForm(ModelForm):
    class Meta:
        model = rider
        fields = ['number','ip_time', 'ip_time_second', 'ip_temp', 'ip_bp','ip_humdity']
        labels = {
            'number': 'Race No.',
            'ip_time': 'Individual Pursuit Minute',
            'ip_time_second': 'Individual Pursuit Seconds/Splitseconds (ss.kkk)',
            'ip_temp': 'Individual Pursuit Temperature',
            'ip_bp': 'Individual Pursuit Barometric Pressure',
            'ip_humdity': 'Individual Pursuit Humidity (Percentage)',
        }

class Flying200Form(ModelForm):
    class Meta:
        model = rider
        fields = ['number','tt200_time', 'tt200_temp', 'tt200_bp', 'tt200_humdity']
        labels = {
            'number': 'Race No.',
            'tt200_time': 'Flying 200m Time(ss.kkk)',
            'tt200_temp': 'Flying 200m Temperature',
            'tt200_bp': 'Flying 200m Barometric Pressure',
            'tt200_humdity': 'Flying 200m Pursuit Humidity (Percentage)',
        }
class TeamSprintForm(ModelForm):
    class Meta:
        model = rider
        fields = ['number', 'ts_time', 'ts_temp', 'ts_bp','ts_humdity']
        labels = {
            'number': 'Race No.',
            'ts_time': 'Team Sprint Time (ss.kkk)',
            'ts_temp': 'Team Sprint Temperature',
            'ts_bp': 'Team Sprint Barometric Pressure',
            'ts_humdity': ' Team Sprint Humidity (Percentage)'
        }

class TeamPursuitForm(ModelForm):
    class Meta:
        model = rider
        fields = ['number', 'tp_time', 'tp_time_second', 'tp_temp', 'tp_bp', 'tp_humdity']
        labels = {
            'number': 'Race No.',
            'tp_time': 'Team Pursuit Minute',
            'tp_time_second': 'Individual Pursuit Seconds/Splitseconds (ss.kkk)',
            'tp_temp': 'Team Pursuit Temperature',
            'tp_bp': 'Team Pursuit Barometric Pressure',
            'tp_humdity': 'Team Pursuit Humidity (Percentage)'
        }

class TimeTrialForm(ModelForm):
    class Meta:
        model = rider
        fields = ['number', 'tt_time', 'tt_time_second', 'tt_temp', 'tt_bp', 'tt_humdity']
        labels = {
            'number': 'Race No.',
            'tt_time': 'Time Trial Minute',
            'tt_time_second': 'Time Trial Seconds/Splitseconds (ss.kkk)',
            'tt_temp': 'Time Trial Temperature',
            'tt_bp': 'Time Trial Barometric Pressure',
            'tt_humdity': 'Time Trial Humidity (Percentage)'
        }

class AddRiderForm(ModelForm):
    class Meta:
        model = rider
        fields = ['number', 'name', 'team_option', 'state','velodrome','team_member1','team_member2','team_member3','team_member4', 'agegroup']