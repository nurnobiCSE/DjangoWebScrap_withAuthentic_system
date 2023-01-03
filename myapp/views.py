from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import requests
from bs4 import BeautifulSoup as bs

from .models import *
# Create your views here.

def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request,"incorrect username or password!!")
            return redirect('login')    
    return render(request,'index.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def Signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password == repassword:
            if User.objects.filter(email=email).exists():
                messages.warning(request,"this email already exists!")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.warning(request,"this username already exists! try another!")                    
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)    
                user.save()
                messages.success(request,"registration successful")
                return redirect('login')
        else:
            messages.warning(request,"Password is not matched!")                    
            return redirect('signup')

    return render(request,'signup.html')

@login_required
def Dashboard(request):
    return render(request,'dashboard.html')

@login_required
def AddGitUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        git_user = request.POST['gitusername']
        url = 'https://github.com/'+git_user
        r = requests.get(url)
        soup = bs(r.content)
        profile = soup.find('img',{'alt':'Avatar'})['src']
        if GitUser.objects.filter(githubuser=git_user).exists():
            messages.info(request,"this user already added! try another user")
        else:

            github= GitUser(
                githubuser = git_user,
                githubuserimage = profile,
                username = username
            )
            github.save()
            messages.success(request,"new Github user added successfully!!")
            return redirect('add_username')

    return render(request,'user_github.html')

@login_required
def Profile(request):
    githubData = GitUser.objects.all()
    context={
        "data": githubData
    }
    return render(request,'image_github.html',context)