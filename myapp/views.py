from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import requests
from bs4 import BeautifulSoup as bs
# importing for email verification :
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .token import activation_token
# importing for data query(multiple)
from django.db.models import Q
 

# End importing for email verification :
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
                instance = user.save(commit=False)
                instance.is_active = False
                instance.save()
                site = get_current_site(request)
                mail_subject = "Confirmation messsage for system"
                message = render_to_string('confirmation_email.html',{
                    "user" : instance,
                    'domain': site.domain,
                    'uid': instance.id,
                    "token": activation_token.make_token(instance),
                })
                to_email = email.cleaned_data('email')
                to_list = [to_email]
                from_email = settings.EMAIL_HOST_USER
                send_mail(mail_subject,message,from_email,to_list,fail_silently=True)
                
                return HttpResponse("<h2>Thanks for reagistration.A confirmationlink was sent to your email</h2>")
                 
        else:
            messages.warning(request,"Password is not matched!")                    
            return redirect('signup')

    return render(request,'signup.html')

def activate(request):
    return render_to_string()

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
    if 'query' in request.GET:
        query = request.GET['query']
        githubDataQuery = Q(Q(githubuser__icontains=query) | Q(username__icontains=query))
        githubData = GitUser.objects.filter(githubDataQuery)
    else:    
        githubData = GitUser.objects.all()
    context={
        "data": githubData
    }
    return render(request,'image_github.html',context)

def page_error_404(request,exception):
    return render(request,'notfound/404.html')