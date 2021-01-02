from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
import logging
import os

# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.

start = "Toronto"
end = "Ottawa"

from templates.forms import CreateUserForm

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()


    context = {'form':form}
    return render(request, 'register.html', context)

def login(request):
    context = {}
    return render(request, 'login.html', context)

def homeView(request):
    context = {}
    global start, end
    if(start == None or end == None):
        start = "Toronto"
        end = "Ottawa"
    # logger.warning(start, end)
    context['url'] = f"https://www.google.com/maps/embed/v1/directions?key={os.environ.get('CLIENT_SECRET')}&origin={start}&destination={end}&mode=transit&avoid=tolls|highways"
    return render(request, 'home.html', context)

def search(request):
    global start, end
    start = request.POST['content1'].replace(" ","+")
    end = request.POST['content2'].replace(" ","+")
    return HttpResponseRedirect('/homepage/')

def authenticate():
    pass

