from django.shortcuts import render
import re
from .models import User
import bcrypt
from django.contrib import messages
from django.contrib.messages import error
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'loginReg/index.html')

def login(request):
    user={}
    for key,value in request.POST.items():
        if key!="csrfmiddlewaretoken":
            user[key]=value

    errors = User.objects.validate_login(user)
    if len(errors)>0:
        messages.error(request, errors)
        return redirect('/')
    request.session['email'] = user['email']
    messages.success(request, "Successfully logged in!")
    return redirect('/show')

def register(request):
    new_user={}
    for key,value in request.POST.items():
        if key!="csrfmiddlewaretoken":
            new_user[key]=value
    errors = User.objects.validate_registration(new_user)
    if errors:
        for message in errors:
            messages.error(request, message)
        return redirect('/')


    hashed = bcrypt.hashpw((new_user['password'].encode()), bcrypt.gensalt(5))
    User.objects.create(
        first_name=new_user['first_name'],
        last_name=new_user['last_name'],
        email=new_user['email'],
        password=hashed
        )
    request.session['email'] = new_user['email']
    messages.success(request, "Successfully registered!")
    return redirect('/show')

def show(request):
    context = {
        'user': User.objects.get(email=request.session['email'])
    }
    return render(request, 'loginReg/login.html', context)
