from django.urls import path
from .import views


urlpatterns = [
    path('',views.index,name='login'),
    path('signup-user',views.Signup,name='signup'),
    path('dashboard',views.Dashboard,name='dashboard'),
    path('add-user',views.AddGitUser,name='add_username'),
    path('profile-pictures',views.Profile,name='profile'),
    path('logout',views.logout,name='logout'),

    
]