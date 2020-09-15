from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import rider
from .forms import PursuitForm, Flying200Form, TeamSprintForm, TeamPursuitForm, AddRiderForm, TimeTrialForm
from django.contrib.auth.decorators import login_required
from datetime import timedelta,date, datetime
from time import strftime
from time import gmtime
import math


def home(request):
    riderlist = rider.objects.order_by('-last_modified')[:5]
    return render(request, 'web/home.html', {'riders': riderlist})


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
            return redirect('uploadride')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def uploadride(request):
    return render(request, 'web/uploadride.html')

def flying_correction(time_in_sec, temperature_in_celsius, pressure, percentage_humidity):
    return round(
        math.pow((1.17295483302624) / ((pressure * (100.0) - percentage_humidity * ((6.1078) * math.pow(10.0, ((7.5) * temperature_in_celsius) / ((237.7) + temperature_in_celsius)))) / ((temperature_in_celsius + (273.15)) * (287.05)) + (percentage_humidity * ((6.1078) * math.pow(10.0, ((7.5) * temperature_in_celsius) / ((237.7) + temperature_in_celsius)))) / ((temperature_in_celsius + (273.15)) * (461.495))), (0.3277)) * time_in_sec, 3)

@login_required
def ip(request):
    if request.method == 'GET':
        return render(request, 'web/ip.html', {'form': PursuitForm()})
    else:
        if request.user.is_authenticated:
            try:
                instance = get_object_or_404(rider, number=request.POST['number'])
                form = PursuitForm(request.POST, instance=instance)
                if request.POST['ip_time'] == '':
                    ip_time = 0
                else:
                    ip_time = int(request.POST['ip_time'])
                instance.ip_time_total = ip_time * 60 + float(request.POST['ip_time_second'])
                x = flying_correction(ip_time * 60 + float(request.POST['ip_time_second']), float(request.POST['ip_temp']), float(request.POST['ip_bp']), float(request.POST['ip_humdity']))
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
                    return redirect('uploadride')
            except:
                return render(request, 'web/ip.html', {'form': PursuitForm(), 'error': 'User does not exist'})
        else:
            return render(request, 'web/ip.html', {'form': PursuitForm()})

@login_required
def tt(request):
    if request.method == 'GET':
        return render(request, 'web/tt.html', {'form': TimeTrialForm()})
    else:
        if request.user.is_authenticated:
            try:
                instance = get_object_or_404(rider, number=request.POST['number'])
                form = TimeTrialForm(request.POST, instance=instance)
                if request.POST['tt_time'] == '':
                    tt_time = 0
                else:
                    tt_time = int(request.POST['tt_time'])
                instance.tt_time_total = tt_time * 60 + float(request.POST['tt_time_second'])
                x = flying_correction(tt_time * 60 + float(request.POST['tt_time_second']),
                                      float(request.POST['tt_temp']), float(request.POST['tt_bp']),
                                      float(request.POST['tt_humdity']))
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
                    return redirect('uploadride')
            except:
                return render(request, 'web/tt.html', {'form': TimeTrialForm(), 'error': 'User does not exist'})
        else:
            return render(request, 'web/tt.html', {'form': TimeTrialForm()})

@login_required
def flying200(request):
    if request.method == 'GET':
        return render(request, 'web/flying200.html', {'form': Flying200Form()})
    else:
        if request.user.is_authenticated:
            try:
                instance = get_object_or_404(rider, number=request.POST['number'])
                form = PursuitForm(request.POST, instance=instance)
                x = flying_correction(float(request.POST['tt200_time']),
                                      float(request.POST['tt200_temp']), float(request.POST['tt200_bp']),
                                      float(request.POST['tt200_humdity']))
                seconds = float("{:.3f}".format(x))
                instance.tt200_adjusted_time = seconds
                instance.user = request.user
                if form.is_valid():
                    form.save()
                    return redirect('uploadride')
            except:
                return render(request, 'web/flying200.html', {'form': Flying200Form(), 'error': 'User does not exist'})
        else:
            return render(request, 'web/flying200.html', {'form': Flying200Form()})

@login_required
def teampursuit(request):
    if request.method == 'GET':
        return render(request, 'web/teampursuit.html', {'form': TeamPursuitForm()})
    else:
        if request.user.is_authenticated:
            try:
                instance = get_object_or_404(rider, number=request.POST['number'])
                form = TeamPursuitForm(request.POST, instance=instance)
                instance.tp_time_total = int(request.POST['tp_time']) * 60 + float(request.POST['tp_time_second'])
                x = flying_correction(int(request.POST['tp_time']) * 60 + float(request.POST['tp_time_second']),
                                      float(request.POST['tp_temp']), float(request.POST['tp_bp']),
                                      float(request.POST['tp_humdity']))
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
                if form.is_valid():
                    form.save()
                    instance.user = request.user
                    return redirect('uploadride')
            except:
                return render(request, 'web/teampursuit.html',
                              {'form': TeamPursuitForm(), 'error': 'User does not exist'})
        else:
            return render(request, 'web/teampursuit.html', {'form': TeamPursuitForm()})

@login_required
def teamsprint(request):
    if request.method == 'GET':
        return render(request, 'web/teamsprint.html', {'form': TeamSprintForm()})
    else:
        if request.user.is_authenticated:
            try:
                instance = get_object_or_404(rider, number=request.POST['number'])
                form = TeamSprintForm(request.POST, instance=instance)
                x = flying_correction(float(request.POST['ts_time']),
                                      float(request.POST['ts_temp']), float(request.POST['ts_bp']),
                                      float(request.POST['ts_humdity']))
                seconds = float("{:.3f}".format(x))
                instance.ts_adjusted_time = seconds
                instance.user = request.user
                if form.is_valid():
                    form.save()
                    return redirect('uploadride')
            except:
                return render(request, 'web/teamsprint.html',
                              {'form': TeamPursuitForm(), 'error': 'User does not exist'})
        else:
            return render(request, 'web/teamsprint.html', {'form': TeamPursuitForm()})

@login_required
def newrider(request):
        if request.method == 'GET':
            return render(request, 'web/newrider.html', {'form': AddRiderForm()})
        else:
            if request.user.is_authenticated:
                    form = AddRiderForm(request.POST)
                    form.user = request.user
                    if form.is_valid():
                        form.save()
                        return redirect('uploadride')
                    else:
                        return render(request, 'web/newrider.html', {'form': AddRiderForm(), 'error': 'That number is taken, try again with another number'})
            else:
                return render(request, 'web/newrider.html', {'form': AddRiderForm()})

@login_required
def log(request):
    riderlist = rider.objects.order_by('-last_modified')
    return render(request, 'web/log.html', {'riders': riderlist})


def riderlist(request):
    riderlist = rider.objects.order_by('number')
    return render(request, 'web/riders.html', {'riders': riderlist})


def detail(request, rider_id):
    riders = get_object_or_404(rider, pk=rider_id)
    return render(request, 'web/detail.html', {'riders': riders})


def result(request):
    return render(request, 'web/result.html')


def result_ip(request):
    todaydate= date.today()
    finaldate = date(2020, 10, 14)
    u15m = rider.objects.order_by('ip_time_total_adjusted').filter(ip_time_total__gt=0, agegroup='JM15')
    u15w = rider.objects.order_by('ip_time_total_adjusted').filter(ip_time_total__gt=0, agegroup='JW15')
    u17m = rider.objects.order_by('ip_time_total_adjusted').filter(ip_time_total__gt=0, agegroup='JM17')
    u17w = rider.objects.order_by('ip_time_total_adjusted').filter(ip_time_total__gt=0, agegroup='JW17')
    u19m = rider.objects.order_by('ip_time_total_adjusted').filter(ip_time_total__gt=0, agegroup='JM19')
    u19w = rider.objects.order_by('ip_time_total_adjusted').filter(ip_time_total__gt=0, agegroup='JW19')
    elitem = rider.objects.order_by('ip_time_total_adjusted').filter(ip_time_total__gt=0, agegroup='ELITEM')
    elitew = rider.objects.order_by('ip_time_total_adjusted').filter(ip_time_total__gt=0, agegroup='ELITEW')
    parab = rider.objects.order_by('tt_time_total_adjusted').filter(ip_time_total__gt=0, agegroup='PARA-B')
    parac = rider.objects.order_by('tt_time_total_adjusted').filter(ip_time_total__gt=0, agegroup='PARA-C')
    return render(request, 'web/result_ip.html',
                  {'jm15': u15m, 'jw15': u15w, 'jm17': u17m, 'jw17': u17w, 'jm19': u19m, 'jw19': u19w, 'elitem': elitem,
                   'elitew': elitew, 'parab': parab, 'parac': parac, 'timedate': todaydate,'finaldate': finaldate })

def result_tt(request):
    todaydate = date.today()
    finaldate = date(2020, 10, 14)
    u15m = rider.objects.order_by('tt_time_total_adjusted').filter(tt_time_total__gt=0, agegroup='JM15')
    u15w = rider.objects.order_by('tt_time_total_adjusted').filter(tt_time_total__gt=0, agegroup='JW15')
    u17m = rider.objects.order_by('tt_time_total_adjusted').filter(tt_time_total__gt=0, agegroup='JM17')
    u17w = rider.objects.order_by('tt_time_total_adjusted').filter(tt_time_total__gt=0, agegroup='JW17')
    u19m = rider.objects.order_by('tt_time_total_adjusted').filter(tt_time_total__gt=0, agegroup='JM19')
    u19w = rider.objects.order_by('tt_time_total_adjusted').filter(tt_time_total__gt=0, agegroup='JW19')
    elitem = rider.objects.order_by('tt_time_total_adjusted').filter(tt_time_total__gt=0, agegroup='ELITEM')
    elitew = rider.objects.order_by('tt_time_total_adjusted').filter(tt_time_total__gt=0, agegroup='ELITEW')
    parab = rider.objects.order_by('tt_time_total_adjusted').filter(tt_time_total__gt=0, agegroup='PARA-B')
    parac = rider.objects.order_by('tt_time_total_adjusted').filter(tt_time_total__gt=0, agegroup='PARA-C')
    return render(request, 'web/result_tt.html',
                  {'jm15': u15m, 'jw15': u15w, 'jm17': u17m, 'jw17': u17w, 'jm19': u19m, 'jw19': u19w, 'elitem': elitem,
                   'elitew': elitew, 'parab': parab, 'parac': parac, 'timedate': todaydate, 'finaldate': finaldate})


def result_flying200(request):
    todaydate = date.today()
    finaldate = date(2020, 10, 14)
    u15m = rider.objects.order_by('tt200_time').filter(tt200_time__gt=0, agegroup='JM15')
    u15w = rider.objects.order_by('tt200_time').filter(tt200_time__gt=0, agegroup='JW15')
    u17m = rider.objects.order_by('tt200_time').filter(tt200_time__gt=0, agegroup='JM17')
    u17w = rider.objects.order_by('tt200_time').filter(tt200_time__gt=0, agegroup='JW17')
    u19m = rider.objects.order_by('tt200_time').filter(tt200_time__gt=0, agegroup='JM19')
    u19w = rider.objects.order_by('tt200_time').filter(tt200_time__gt=0, agegroup='JW19')
    elitem = rider.objects.order_by('tt200_time').filter(tt200_time__gt=0, agegroup='ELITEM')
    elitew = rider.objects.order_by('tt200_time').filter(tt200_time__gt=0, agegroup='ELITEW')
    parab = rider.objects.order_by('tt200_time').filter(tt200_time__gt=0, agegroup='PARA-B')
    parac = rider.objects.order_by('tt200_time').filter(tt200_time__gt=0, agegroup='PARA-C')
    return render(request, 'web/result_flying200.html',
                  {'jm15': u15m, 'jw15': u15w, 'jm17': u17m, 'jw17': u17w, 'jm19': u19m, 'jw19': u19w, 'elitem': elitem,
                   'elitew': elitew, 'parab': parab, 'parac': parac, 'timedate': todaydate, 'finaldate': finaldate})

    return render(request, 'web/result_flying200.html')


def result_teampursuit(request):
    todaydate = date.today()
    finaldate = date(2020, 10, 14)
    u15m = rider.objects.order_by('tp_time_total').filter(tp_time_total__gt=0, agegroup='JM15')
    u15w = rider.objects.order_by('tp_time_total').filter(tp_time_total__gt=0, agegroup='JW15')
    u17m = rider.objects.order_by('tp_time_total').filter(tp_time_total__gt=0, agegroup='JM17')
    u17w = rider.objects.order_by('tp_time_total').filter(tp_time_total__gt=0, agegroup='JW17')
    u19m = rider.objects.order_by('tp_time_total').filter(tp_time_total__gt=0, agegroup='JM19')
    u19w = rider.objects.order_by('tp_time_total').filter(tp_time_total__gt=0, agegroup='JW19')
    elitem = rider.objects.order_by('tp_time_total').filter(tp_time_total__gt=0, agegroup='ELITEM')
    elitew = rider.objects.order_by('tp_time_total').filter(tp_time_total__gt=0, agegroup='ELITEW')
    return render(request, 'web/result_teampursuit.html',
                  {'jm15': u15m, 'jw15': u15w, 'jm17': u17m, 'jw17': u17w, 'jm19': u19m, 'jw19': u19w, 'elitem': elitem,
                   'elitew': elitew, 'timedate': todaydate, 'finaldate': finaldate})


def result_teamsprint(request):
    todaydate = date.today()
    finaldate = date(2020, 10, 14)
    u15m = rider.objects.order_by('ts_time').filter(ts_time__gt=0, agegroup='JM15')
    u15w = rider.objects.order_by('ts_time').filter(ts_time__gt=0, agegroup='JW15')
    u17m = rider.objects.order_by('ts_time').filter(ts_time__gt=0, agegroup='JM17')
    u17w = rider.objects.order_by('ts_time').filter(ts_time__gt=0, agegroup='JW17')
    u19m = rider.objects.order_by('ts_time').filter(ts_time__gt=0, agegroup='JM19')
    u19w = rider.objects.order_by('ts_time').filter(ts_time__gt=0, agegroup='JW19')
    elitem = rider.objects.order_by('ts_time').filter(ts_time__gt=0, agegroup='ELITEM')
    elitew = rider.objects.order_by('ts_time').filter(ts_time__gt=0, agegroup='ELITEW')
    return render(request, 'web/result_teamsprint.html',
                  {'jm15': u15m, 'jw15': u15w, 'jm17': u17m, 'jw17': u17w, 'jm19': u19m, 'jw19': u19w, 'elitem': elitem,
                   'elitew': elitew, 'timedate': todaydate, 'finaldate': finaldate})
