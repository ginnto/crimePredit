from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('about', views.about, name='about'),
    path('user_home',views.user_home,name='user_home'),
    path('police_dashboard',views.police_dashboard,name='police_dashboard'),
    path('complaint',views.complaint,name='complaint'),
    path('forgetpassword', views.forgetpassword, name='forgetpassword'),
    path('logout',views.logout,name='logout'),
    path('police-login', views.police_login, name='police_login'),
    path('police_profile', views.police_profile, name='police_profile'),
    path('register/', views.register, name='register'),
    path('view_complaint', views.view_complaint, name='view_complaint'),
    path('view_complaintuser', views.view_complaintuser, name='view_complaintuser'),
    path('fir', views.fir, name='fir'),
    path('replay', views.replay, name='replay'),
]

