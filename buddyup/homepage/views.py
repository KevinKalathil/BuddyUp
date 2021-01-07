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
confirmedRoute = []
matches = [None]*1

from templates.forms import CreateUserForm, LoginUserForm

def register(request):
    form = CreateUserForm()
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

    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        user = authenticate(request, username=username, password = password1)
        logger.warning(user);

        if user is not None:
            login(request, user)
            global userName, matches
            matches = [None] * 1
            userName= username
            logger.warning(userName)
            return HttpResponseRedirect('/homepage/')

    context = {'form': form}
    return render(request, 'login.html', context)

def homeView(request):
    context = {}
    global start, end, confirmedRoute
    if(start == None or end == None):
        start = "Toronto"
        end = "Ottawa"

    route = []
    directionsapi = f"https://maps.googleapis.com/maps/api/directions/json?origin={start}&destination={end}&mode=transit&arrival_time={time}&key={str(os.environ.get('CLIENT_SECRET'))}"
    logger.warning(os.environ.get('CLIENT_SECRET'))
    route = getRoute(directionsapi)
    context['url'] = f"https://www.google.com/maps/embed/v1/directions?key={os.environ.get('CLIENT_SECRET')}&origin={start}&destination={end}&mode=transit&avoid=tolls|highways"
    context['start'] = route[0]
    context['end'] = route[1]
    context['USER'] = userName
    context['transit_items'] = route[2]
    logger.warning(route)
    context['transit_items'] = addMatches(context['transit_items'])
    confirmedRoute = getTransitStrings(context['transit_items'])
    return render(request, 'home.html', context)

def addMatches(transit_items):
    for i in range(len(transit_items)):
        if(matches and i<len(matches)):
            transit_items[i].append(matches[i])
        else:
            transit_items[i].append("NO MATCH")

    return transit_items

def getTransitStrings(transit_items):
    transitString = ""
    for i in transit_items:
        logger.warning(i)
        transitString+= str(i[1])+str('_')+str(i[2])+'_'+str(i[4])
        transitString+='$'

    transitString = transitString[:-1]
    return transitString

def search(request):
    global start, end, arrival_time, time, matches
    start = request.POST['content1'].replace(" ","+")
    end = request.POST['content2'].replace(" ","+")
    arrival_day = request.POST['day']
    arrival_day = calendar.timegm(datetime.strptime(arrival_day, "%Y-%m-%d").timetuple())
    time = request.POST['time']
    times = time.split(":")
    time = ((int)(times[0]) * 60 + (int)(times[1]))*60
    time += arrival_day + 25200 # Convert to EST
    matches = [None]* len(matches)

    return HttpResponseRedirect('/homepage/')

def confirm(request):
    userList = User.objects.values()
    logger.warning(userList)
    u1 = User.objects.get(username = userName)
    if(u1.last_name==''):
        u1.last_name = confirmedRoute
    else:
        u1.last_name += '$'+confirmedRoute
    u1.save()
    return HttpResponseRedirect('/homepage/')


def match(request):
    global matches
    splitconfirmedRoute = confirmedRoute.split("$")
    userList = User.objects.values()
    matches = [None]*len(splitconfirmedRoute)

    for i in range(len(userList)):
        logger.warning(userList[i]['username'])
        if(userList[i]['username']==userName):
            continue
        routes = userList[i]['last_name'].split("$")
        for j in range(len(routes)):
            for k in range(len(splitconfirmedRoute)):
                if routes[j]==splitconfirmedRoute[k] and matches[k]==None:
                    matches[k] = userList[i]['username']
                    logger.warning(routes)
                    logger.warning(splitconfirmedRoute)

    logger.warning(matches)

    return HttpResponseRedirect('/homepage/')

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
