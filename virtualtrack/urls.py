"""virtualtrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web import views

admin.site.site_header = "VirtualTrack Admin"
admin.site.site_title = "Virtual Track Admin"

urlpatterns = [
    path('admin/', admin.site.urls),

    #Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('newrider/', views.newrider, name='newrider'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('log/', views.log, name='log'),


    #Rides
    path('', views.home, name='home'),
    path('riders/', views.riderlist, name='riderlist'),
    path('uploadride/ip/', views.ip, name='ip'),
    path('uploadride/', views.uploadride, name='uploadride'),
    path('uploadride/flying200/', views.flying200, name='flying200'),
    path('uploadride/teamsprint/', views.teamsprint, name='teamsprint'),
    path('uploadride/teampursuit/', views.teampursuit, name='teampursuit'),
    path('uploadride/tt/', views.tt, name='timetrial'),
    path('riders/<int:rider_id>/', views.detail, name='detail'),

    #Results
    path('results/', views.result, name='result'),
    path('results/ip/', views.result_ip, name='result_ip'),
    path('results/tt/', views.result_tt, name='result_tt'),
    path('results/flying200/', views.result_flying200, name='result_flying200'),
    path('results/teampursuit/', views.result_teampursuit, name='result_teampursuit'),
    path('results/teamsprint/', views.result_teamsprint, name='result_teamsprint'),

]
