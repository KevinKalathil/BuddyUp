from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
import logging
import os
import urllib.request, json
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
# Get an instance of a logger
logger = logging.getLogger(__name__)
import time
from datetime import datetime
import calendar

# Create your views here.

start = "Toronto"
end = "Ottawa"
arrival_time = int(time.time()+600)
time = arrival_time
userName=""

from templates.forms import CreateUserForm, LoginUserForm

def register(request):
    form = CreateUserForm()
    # profile = ExtraUserForm()
    global userName

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            userName = request.POST['username']
            return HttpResponseRedirect('/homepage/')

    context = {'form': form}
    return render(request, 'register.html', context)

def loginPage(request):
    form = LoginUserForm()
    # profile = ExtraUserForm()

    if request.method == 'POST':

        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        user = authenticate(request, username=username, password = password1)

        if user is not None:
            login(request, user)
            global userName
            userName= username
            return HttpResponseRedirect('/homepage/')

    context = {'form': form}
    return render(request, 'login.html', context)

def homeView(request):
    context = {}
    global start, end
    if(start == None or end == None):
        start = "Toronto"
        end = "Ottawa"

    route = []
    directionsapi = f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&mode=transit&arrival_time={time}&key={os.environ.get('CLIENT_SECRET')}"
    route = getRoute(directionsapi)
    context['url'] = f"https://www.google.com/maps/embed/v1/directions?key={os.environ.get('CLIENT_SECRET')}&origin={start}&destination={end}&mode=transit&avoid=tolls|highways"
    context['start'] = route[0]
    context['end'] = route[1]
    context['transit_items'] = route[2]
    return render(request, 'home.html', context)

def search(request):
    global start, end, arrival_time, time
    start = request.POST['content1'].replace(" ","+")
    end = request.POST['content2'].replace(" ","+")
    arrival_day = request.POST['day']
    arrival_day = calendar.timegm(datetime.strptime(arrival_day, "%Y-%m-%d").timetuple())
    time = request.POST['time']
    times = time.split(":")
    time = ((int)(times[0]) * 60 + (int)(times[1]))*60
    time += arrival_day + 25200
    logger.warning(time)
    return HttpResponseRedirect('/homepage/')

def confirm(request):
    userList = User.objects.values()
    logger.warning(userList)
    index=0
    u1 = None
    u1 = User.objects.get(username = userName)
    # for i in range(len(userList)):
    #     if(userList[i]["username"]==userName):
    #         index = i
    #         u1 = userList[i]
    #         break

    u1.last_name='1'

    u1.save()

    # logger.warning(users)
    # logger.warning(u1)
    # logger.warning(u1.email)

    return HttpResponseRedirect('/homepage/')


def match(request):
    pass

def getRoute(directionurl):
    with urllib.request.urlopen(directionurl) as url:
        data = json.loads(url.read().decode())
        # print(data)

    routes = data["routes"]
    transitlist = []
    finalroutedetails = []
    if(len(routes)>0):
        startpoint = routes[0]["legs"][0]["start_address"]
        endpoint = routes[0]["legs"][0]["end_address"]
        steps = routes[0]["legs"][0]["steps"]

        finalroutedetails.append(startpoint)
        finalroutedetails.append(endpoint)


        for s in steps:
            if(s["travel_mode"]=="TRANSIT"):
                transititem = [s["html_instructions"],
                               s["transit_details"]["departure_stop"]["name"],
                               s["transit_details"]["arrival_stop"]["name"],
                               s["duration"]["text"],
                               s["transit_details"]["arrival_time"]["text"]]
                transitlist.append(transititem)
    else:
        finalroutedetails=[start,end.replace("+", " ")+" NOT FOUND"]
        transitlist = [[0, 0, 0, 0]]
    finalroutedetails.append(transitlist)

    return finalroutedetails
