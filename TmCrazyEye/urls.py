"""TmCrazyEye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index.html', views.index),
    path('login.html', views.login),
    path('logout.html', views.logout),
    path('batch_cmd.html', views.batch_cmd, name="batch_cmd"),
    path('batch_cmd_mgr.html', views.batch_cmd_mgr, name="batch_cmd_mgr"),
    path('web_ssh.html', views.web_ssh, name="web_ssh"),
]
