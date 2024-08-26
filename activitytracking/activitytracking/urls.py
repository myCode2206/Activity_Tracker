"""
URL configuration for activitytracking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Home.views import *

urlpatterns = [
    path('',Front,name="Front"),
    path('auth/',Auth,name="Auth"),
    path('register/',Signup,name="Signup"),
    path('dashboard/',Dashboard,name="Dashboard"),
    path('activity/',Activity,name="Activity"),
    path('login/',login,name="Login"),
    path('signup/',signup,name="signup"),
    path("start_tracking/",start_tracking,name="start_tracking"),
    path("stop_tracking/",stop_tracking,name="stop_tracking"),
    path("get_applications/",get_applications,name="get_applications"),
    path("show_imgpage/",show_imgpage,name="show_imgpage"),
    path("get_my_images/",get_my_images,name="get_my_images"),
    path('admin/', admin.site.urls),
]
