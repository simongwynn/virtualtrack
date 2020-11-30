from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import rider, Event
from .forms import PursuitForm, Flying200Form, TeamSprintForm, TeamPursuitForm, AddRiderForm, TimeTrialForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta,date, datetime
from django.urls import include, path
from time import strftime
from time import gmtime
import math


def home(request):
    eventlist = Event.objects.order_by('-date')[:10]
    return render(request, 'web/home.html', {'eventlist': eventlist})

def event(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    riderlist = rider.objects.filter(event=Event_id).order_by('-last_modified')[:5]
    return render(request, 'web/event.html', {'events': events, 'riders': riderlist})

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'web/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('uploadride')
            except IntegrityError:
                return render(request, 'web/signupuser.html', {'form': UserCreationForm(),
                                                               'error': 'Username has already been used please choice a new username'})
        else:
            return render(request, 'web/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'web/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'web/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password are incorrect'})
        else:
            login(request, user)
            return redirect('uploadoptions')


def uploadoptions(request):
    eventlist = Event.objects.order_by('-date')[:10]
    return render(request, 'web/choice.html', {'eventlist': eventlist})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def uploadride(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    return render(request, 'web/uploadride.html', {'events':events})

def flying_correction(time_in_sec, temperature_in_celsius, pressure, percentage_humidity):
    return round(
        math.pow((1.17295483302624) / ((pressure * (100.0) - percentage_humidity * ((6.1078) * math.pow(10.0, ((7.5) * temperature_in_celsius) / ((237.7) + temperature_in_celsius)))) / ((temperature_in_celsius + (273.15)) * (287.05)) + (percentage_humidity * ((6.1078) * math.pow(10.0, ((7.5) * temperature_in_celsius) / ((237.7) + temperature_in_celsius)))) / ((temperature_in_celsius + (273.15)) * (461.495))), (0.3277)) * time_in_sec, 3)

@login_required
def ip(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    if request.method == 'GET':
        return render(request, 'web/ip.html', {'form': PursuitForm(), 'events':events})
    else:
        if request.user.is_authenticated:
            try:
                item2 = rider.objects.filter(number=request.POST['number'],                                             event=Event_id)  # how we work out the person to change
                id = item2[0].id  # how we work out the person to change
                instance = get_object_or_404(rider, pk=id)
                form = PursuitForm(request.POST, instance=instance)
                if request.POST['ip_time'] == '':
                    ip_time = 0
                else:
                    ip_time = int(request.POST['ip_time'])
                instance.ip_time_total = ip_time * 60 + float(request.POST['ip_time_second'])
                x = flying_correction(ip_time * 60 + float(request.POST['ip_time_second']), float(request.POST['ip_temp']), float(request.POST['ip_bp']), float(request.POST['ip_humdity']))
                if instance.velodrome == 'NT Velodrome':
                    if instance.agegroup == 'ELITEM':
                        x = x -12
                    elif instance.agegroup == 'JM19' or instance.agegroup == 'ELITEW':
                        x = x -9
                    else:
                        x = x - 6
                instance.ip_time_total_adjusted = x
                min = int(x/60)
                seconds = x - (min*60)
                seconds = float("{:.3f}".format(seconds))
                if seconds < 10:
                    seconds ='0'+str(seconds)
                if float(request.POST['ip_time_second']) <10:
                    currentseconds = float(request.POST['ip_time_second'])
                    instance.ip_time_second = '0' + str(currentseconds)
                instance.ip_adjusted_time = min
                instance.ip_adjusted_second = seconds
                instance.user = request.user
                if form.is_valid():
                    form.save()
                    return render(request, 'web/ip.html', {'form': PursuitForm(), 'error': 'Successfully Uploaded', 'events':events})
            except:
                return render(request, 'web/ip.html', {'form': PursuitForm(), 'error': 'User does not exist', 'events':events})
        else:
            return render(request, 'web/ip.html', {'form': PursuitForm(), 'events':events})

@login_required
def tt(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    if request.method == 'GET':
        return render(request, 'web/tt.html', {'form': TimeTrialForm(), 'events':events})
    else:
        if request.user.is_authenticated:
            try:
                item2 = rider.objects.filter(number=request.POST['number'],
                                             event=Event_id)  # how we work out the person to change
                id = item2[0].id  # how we work out the person to change
                instance = get_object_or_404(rider, pk=id)
                form = TimeTrialForm(request.POST, instance=instance)
                if request.POST['tt_time'] == '':
                    tt_time = 0
                else:
                    tt_time = int(request.POST['tt_time'])
                instance.tt_time_total = tt_time * 60 + float(request.POST['tt_time_second'])
                x = flying_correction(tt_time * 60 + float(request.POST['tt_time_second']),
                                      float(request.POST['tt_temp']), float(request.POST['tt_bp']),
                                      float(request.POST['tt_humdity']))
                if instance.velodrome == 'NT Velodrome':
                    if instance.agegroup == 'ELITEM' or instance.agegroup == 'JM19':
                        x = x - 2
                    else:
                        x = x - 1
                instance.tt_time_total_adjusted = x
                min = int(x / 60)
                seconds = x - (min * 60)
                seconds = float("{:.3f}".format(seconds))
                if seconds < 10:
                    seconds = '0' + str(seconds)
                if float(request.POST['tt_time_second']) < 10:
                    currentseconds = float(request.POST['tt_time_second'])
                    instance.tt_time_second = '0' + str(currentseconds)
                instance.tt_adjusted_time = min
                instance.tt_adjusted_second = seconds
                instance.user = request.user
                if form.is_valid():
                    form.save()
                    return render(request, 'web/tt.html', {'form': TimeTrialForm(), 'error': 'Successfully Uploaded', 'events':events})
            except:
                return render(request, 'web/tt.html', {'form': TimeTrialForm(), 'error': 'User does not exist', 'events':events})
        else:
            return render(request, 'web/tt.html', {'form': TimeTrialForm(), 'events':events})

@login_required
def flying200(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    if request.method == 'GET':
        return render(request, 'web/flying200.html', {'form': Flying200Form(), 'events':events})
    else:
        if request.user.is_authenticated:
            try:
                item2 = rider.objects.filter(number=request.POST['number'],
                                             event=Event_id)  # how we work out the person to change
                id = item2[0].id  # how we work out the person to change
                instance = get_object_or_404(rider, pk=id)
                form = PursuitForm(request.POST, instance=instance)
                x = flying_correction(float(request.POST['tt200_time']),
                                      float(request.POST['tt200_temp']), float(request.POST['tt200_bp']),
                                      float(request.POST['tt200_humdity']))
                if instance.velodrome == 'NT Velodrome':
                    if instance.agegroup == 'ELITEM' or instance.agegroup == 'ELITEW':
                        x = x -1
                seconds = float("{:.3f}".format(x))
                instance.tt200_time = float(request.POST['tt200_time'])
                instance.tt200_temp = float(request.POST['tt200_temp'])
                instance.tt200_bp = float(request.POST['tt200_bp'])
                instance.tt200_humdity = float(request.POST['tt200_humdity'])
                instance.tt200_adjusted_time = seconds
                instance.user = request.user
                if form.is_valid():
                    form.save()
                    return render(request, 'web/flying200.html', {'form': Flying200Form(), 'error': 'Successfully Uploaded', 'events':events})
            except:
                return render(request, 'web/flying200.html', {'form': Flying200Form(), 'error': 'User does not exist', 'events':events})
        else:
            return render(request, 'web/flying200.html', {'form': Flying200Form(), 'events':events})

@login_required
def teampursuit(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    if request.method == 'GET':
        return render(request, 'web/teampursuit.html', {'form': TeamPursuitForm(), 'events':events})
    else:
        if request.user.is_authenticated:
            try:
                item2 = rider.objects.filter(number=request.POST['number'],
                                             event=Event_id)  # how we work out the person to change
                id = item2[0].id  # how we work out the person to change
                instance = get_object_or_404(rider, pk=id)
                form = TeamPursuitForm(request.POST, instance=instance)
                instance.tp_time_total = int(request.POST['tp_time']) * 60 + float(request.POST['tp_time_second'])
                x = flying_correction(int(request.POST['tp_time']) * 60 + float(request.POST['tp_time_second']),
                                      float(request.POST['tp_temp']), float(request.POST['tp_bp']),
                                      float(request.POST['tp_humdity']))
                if instance.velodrome == 'NT Velodrome':
                    if instance.agegroup == 'ELITEM' or instance.agegroup == 'ELITEW':
                        x = x -13
                    else:
                        x = x -10
                instance.tp_time_total_adjusted = x
                min = int(x / 60)
                seconds = x - (min * 60)
                seconds = float("{:.3f}".format(seconds))
                if seconds < 10:
                    seconds = '0' + str(seconds)
                if float(request.POST['tp_time_second']) < 10:
                    currentseconds = float(request.POST['tp_time_second'])
                    instance.tp_time_second = '0' + str(currentseconds)
                instance.tp_adjusted_time = min
                instance.tp_adjusted_second = seconds
                instance.user = request.user
                if form.is_valid():
                    form.save()
                    instance.user = request.user
                    return render(request, 'web/teampursuit.html',
                                  {'form': TeamPursuitForm(), 'error': 'Successfully Uploaded', 'events':events})
            except:
                return render(request, 'web/teampursuit.html',
                              {'form': TeamPursuitForm(), 'error': 'User does not exist', 'events':events})
        else:
            return render(request, 'web/teampursuit.html', {'form': TeamPursuitForm(), 'events':events})

@login_required
def teamsprint(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    if request.method == 'GET':
        return render(request, 'web/teamsprint.html', {'form': TeamSprintForm(), 'events':events})
    else:
        if request.user.is_authenticated:
            try:
                item2 = rider.objects.filter(number=request.POST['number'],
                                             event=Event_id)  # how we work out the person to change
                id = item2[0].id  # how we work out the person to change
                instance = get_object_or_404(rider, pk=id)
                form = TeamSprintForm(request.POST, instance=instance)
                x = flying_correction(float(request.POST['ts_time']),
                                      float(request.POST['ts_temp']), float(request.POST['ts_bp']),
                                      float(request.POST['ts_humdity']))
                if instance.velodrome == 'NT Velodrome':
                    x = x -3
                if instance.velodrome == 'Silverdome':
                    x = x -1
                seconds = float("{:.3f}".format(x))
                instance.ts_adjusted_time = seconds
                instance.user = request.user
                if form.is_valid():
                    form.save()
                    return render(request, 'web/teamsprint.html',
                                  {'form': TeamSprintForm(), 'error': 'Successfully Uploaded', 'events':events})
            except:
                return render(request, 'web/teamsprint.html',
                              {'form': TeamSprintForm(), 'error': 'User does not exist', 'events':events})
        else:
            return render(request, 'web/teamsprint.html', {'form': TeamPursuitForm(), 'events':events})

@login_required
def newrider(request, Event_id):
        events = get_object_or_404(Event, pk=Event_id)
        riders = rider.objects.filter(event=Event_id)
        if request.method == 'GET':
            return render(request, 'web/newrider.html', {'form': AddRiderForm(), 'events':events})
        else:
            if request.user.is_authenticated:
                item = rider.objects.filter(number=request.POST['number'], event=Event_id).count()
                if item == 0:
                    form = AddRiderForm(request.POST)
                    if form.is_valid():
                        form.save()
                        return render(request, 'web/newrider.html', {'form': AddRiderForm(), 'error': 'Successfully Uploaded', 'events':events})
                    else:
                        return render(request, 'web/newrider.html', {'form': AddRiderForm(), 'error': 'That number is taken, try again with another number', 'events':events})
                else:
                    return render(request, 'web/newrider.html',
                                  {'form': AddRiderForm(), 'error': 'That number is taken, try again with another number', 'events':events})
            else:
                return render(request, 'web/newrider.html', {'form': AddRiderForm(), 'events':events})

@login_required
def log(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    riderlist = rider.objects.filter(event=Event_id).order_by('-last_modified')
    return render(request, 'web/log.html', {'riders': riderlist, 'events':events})


def riderlist(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    riderlist = rider.objects.filter(event=Event_id).order_by('number')
    return render(request, 'web/riders.html', {'riders': riderlist, 'events':events})


def detail(request, rider_id, Event_id):
    riders = get_object_or_404(rider, pk=rider_id)
    events = get_object_or_404(Event, pk=Event_id)

    return render(request, 'web/detail.html', {'riders': riders, 'events':events})


def result(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    return render(request, 'web/result.html', {'events':events})


def result_ip(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    todaydate= date.today()
    finaldate = events.finish
    u15m = rider.objects.order_by('ip_time_total_adjusted').filter(event = events.id, ip_time_total__gt=0, agegroup='JM15')
    u15w = rider.objects.order_by('ip_time_total_adjusted').filter(event = events.id, ip_time_total__gt=0, agegroup='JW15')
    u17m = rider.objects.order_by('ip_time_total_adjusted').filter(event = events.id, ip_time_total__gt=0, agegroup='JM17')
    u17w = rider.objects.order_by('ip_time_total_adjusted').filter(event = events.id, ip_time_total__gt=0, agegroup='JW17')
    u19m = rider.objects.order_by('ip_time_total_adjusted').filter(event = events.id, ip_time_total__gt=0, agegroup='JM19')
    u19w = rider.objects.order_by('ip_time_total_adjusted').filter(event = events.id, ip_time_total__gt=0, agegroup='JW19')
    elitem = rider.objects.order_by('ip_time_total_adjusted').filter(event = events.id, ip_time_total__gt=0, agegroup='ELITEM')
    elitew = rider.objects.order_by('ip_time_total_adjusted').filter(event = events.id, ip_time_total__gt=0, agegroup='ELITEW')
    parab = rider.objects.order_by('ip_time_total_adjusted').filter(event = events.id, ip_time_total__gt=0, agegroup='Para-B')
    parac = rider.objects.order_by('ip_time_total_adjusted').filter(event = events.id, ip_time_total__gt=0, agegroup='Para-C')
    return render(request, 'web/result_ip.html',
                  {'jm15': u15m, 'jw15': u15w, 'jm17': u17m, 'jw17': u17w, 'jm19': u19m, 'jw19': u19w, 'elitem': elitem,
                   'elitew': elitew, 'parab': parab, 'parac': parac, 'timedate': todaydate,'finaldate': finaldate, 'event':events })

def result_tt(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    todaydate = date.today()
    finaldate = events.finish
    u15m = rider.objects.order_by('tt_time_total_adjusted').filter(event = events.id, tt_time_total__gt=0, agegroup='JM15')
    u15w = rider.objects.order_by('tt_time_total_adjusted').filter(event = events.id, tt_time_total__gt=0, agegroup='JW15')
    u17m = rider.objects.order_by('tt_time_total_adjusted').filter(event = events.id, tt_time_total__gt=0, agegroup='JM17')
    u17w = rider.objects.order_by('tt_time_total_adjusted').filter(event = events.id, tt_time_total__gt=0, agegroup='JW17')
    u19m = rider.objects.order_by('tt_time_total_adjusted').filter(event = events.id, tt_time_total__gt=0, agegroup='JM19')
    u19w = rider.objects.order_by('tt_time_total_adjusted').filter(event = events.id, tt_time_total__gt=0, agegroup='JW19')
    elitem = rider.objects.order_by('tt_time_total_adjusted').filter(event = events.id, tt_time_total__gt=0, agegroup='ELITEM')
    elitew = rider.objects.order_by('tt_time_total_adjusted').filter(event = events.id, tt_time_total__gt=0, agegroup='ELITEW')
    parab = rider.objects.order_by('tt_time_total_adjusted').filter(event = events.id, tt_time_total__gt=0, agegroup='Para-B')
    parac = rider.objects.order_by('tt_time_total_adjusted').filter(event = events.id, tt_time_total__gt=0, agegroup='Para-C')
    return render(request, 'web/result_tt.html',
                  {'jm15': u15m, 'jw15': u15w, 'jm17': u17m, 'jw17': u17w, 'jm19': u19m, 'jw19': u19w, 'elitem': elitem,
                   'elitew': elitew, 'parab': parab, 'parac': parac, 'timedate': todaydate, 'finaldate': finaldate, 'event':events})


def result_flying200(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    todaydate = date.today()
    finaldate = events.finish
    u15m = rider.objects.order_by('tt200_adjusted_time').filter(event = events.id, tt200_time__gt=0, agegroup='JM15')
    u15w = rider.objects.order_by('tt200_adjusted_time').filter(event = events.id, tt200_time__gt=0, agegroup='JW15')
    u17m = rider.objects.order_by('tt200_adjusted_time').filter(event = events.id, tt200_time__gt=0, agegroup='JM17')
    u17w = rider.objects.order_by('tt200_adjusted_time').filter(event = events.id, tt200_time__gt=0, agegroup='JW17')
    u19m = rider.objects.order_by('tt200_adjusted_time').filter(event = events.id, tt200_time__gt=0, agegroup='JM19')
    u19w = rider.objects.order_by('tt200_adjusted_time').filter(event = events.id, tt200_time__gt=0, agegroup='JW19')
    elitem = rider.objects.order_by('tt200_adjusted_time').filter(event = events.id, tt200_time__gt=0, agegroup='ELITEM')
    elitew = rider.objects.order_by('tt200_adjusted_time').filter(event = events.id, tt200_time__gt=0, agegroup='ELITEW')
    parab = rider.objects.order_by('tt200_adjusted_time').filter(event = events.id, tt200_time__gt=0, agegroup='Para-B')
    parac = rider.objects.order_by('tt200_adjusted_time').filter(event = events.id, tt200_time__gt=0, agegroup='Para-C')
    return render(request, 'web/result_flying200.html',
                  {'jm15': u15m, 'jw15': u15w, 'jm17': u17m, 'jw17': u17w, 'jm19': u19m, 'jw19': u19w, 'elitem': elitem,
                   'elitew': elitew, 'parab': parab, 'parac': parac, 'timedate': todaydate, 'finaldate': finaldate, 'event':events})



def result_teampursuit(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    todaydate = date.today()
    finaldate = events.finish
    mixed = rider.objects.order_by('tp_ineligable', 'tp_time_total_adjusted').filter(event = events.id, tp_time_total__gt=0)
    u15m = rider.objects.order_by('tp_ineligable', 'tp_time_total_adjusted').filter(event = events.id, tp_time_total__gt=0, agegroup='JM15')
    u15w = rider.objects.order_by('tp_ineligable', 'tp_time_total_adjusted').filter(event = events.id, tp_time_total__gt=0, agegroup='JW15')
    u17m = rider.objects.order_by('tp_ineligable', 'tp_time_total_adjusted').filter(event = events.id, tp_time_total__gt=0, agegroup='JM17')
    u17w = rider.objects.order_by('tp_ineligable', 'tp_time_total_adjusted').filter(event = events.id, tp_time_total__gt=0, agegroup='JW17')
    u19m = rider.objects.order_by('tp_ineligable', 'tp_time_total_adjusted').filter(event = events.id, tp_time_total__gt=0, agegroup='JM19')
    u19w = rider.objects.order_by('tp_ineligable', 'tp_time_total_adjusted').filter(event = events.id, tp_time_total__gt=0, agegroup='JW19')
    elitem = rider.objects.order_by('tp_ineligable', 'tp_time_total_adjusted').filter(event = events.id, tp_time_total__gt=0, agegroup='ELITEM')
    elitew = rider.objects.order_by('tp_ineligable', 'tp_time_total_adjusted').filter(event = events.id, tp_time_total__gt=0, agegroup='ELITEW')
    return render(request, 'web/result_teampursuit.html',
                  {'jm15': u15m, 'jw15': u15w, 'jm17': u17m, 'jw17': u17w, 'jm19': u19m, 'jw19': u19w, 'elitem': elitem,
                   'elitew': elitew, 'timedate': todaydate, 'finaldate': finaldate, 'mixed':mixed, 'event':events})


def result_teamsprint(request, Event_id):
    events = get_object_or_404(Event, pk=Event_id)
    todaydate = date.today()
    finaldate = events.finish
    mixed = rider.objects.order_by('ts_ineligable', 'ts_adjusted_time').filter(event = events.id, ts_time__gt=0, )
    u15m = rider.objects.order_by('ts_ineligable', 'ts_adjusted_time').filter(event = events.id, ts_time__gt=0, agegroup='JM15')
    u15w = rider.objects.order_by('ts_ineligable', 'ts_adjusted_time').filter(event = events.id, ts_time__gt=0, agegroup='JW15')
    u17m = rider.objects.order_by('ts_ineligable', 'ts_adjusted_time').filter(event = events.id, ts_time__gt=0, agegroup='JM17')
    u17w = rider.objects.order_by('ts_ineligable', 'ts_adjusted_time').filter(event = events.id, ts_time__gt=0, agegroup='JW17')
    u19m = rider.objects.order_by('ts_ineligable', 'ts_adjusted_time').filter(event = events.id, ts_time__gt=0, agegroup='JM19')
    u19w = rider.objects.order_by('ts_ineligable', 'ts_adjusted_time').filter(event = events.id, ts_time__gt=0, agegroup='JW19')
    elitem = rider.objects.order_by('ts_ineligable', 'ts_adjusted_time').filter(event = events.id, ts_time__gt=0, agegroup='ELITEM')
    elitew = rider.objects.order_by('ts_ineligable', 'ts_adjusted_time').filter(event = events.id, ts_time__gt=0, agegroup='ELITEW')
    return render(request, 'web/result_teamsprint.html',
                  {'jm15': u15m, 'jw15': u15w, 'jm17': u17m, 'jw17': u17w, 'jm19': u19m, 'jw19': u19w, 'elitem': elitem,
                   'elitew': elitew, 'timedate': todaydate, 'finaldate': finaldate, 'mixed':mixed, 'event':events})
