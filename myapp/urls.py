from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('signup-user',views.Signup,name='signup'),
    path('dashboard',views.Dashboard,name='dashboard'),
    path('logout',views.logout,name='logout'),
]