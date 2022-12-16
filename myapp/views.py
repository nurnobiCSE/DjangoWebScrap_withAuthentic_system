from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('dashboard')
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
                return redirect('index')
        else:
            messages.warning(request,"Password is not matched!")                    
            return redirect('signup')

    return render(request,'signup.html')

@login_required
def Dashboard(request):
    return render(request,'dashboard.html')