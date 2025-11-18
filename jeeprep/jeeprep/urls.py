"""
URL configuration for jeeprep project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from apti.views import main_backend_page,aptitude_quiz,software_quiz,verbals_quiz,assesment_quiz

urlpatterns = [
    path("", main_backend_page),
    path("aptitude_quiz.html", aptitude_quiz),
    path("software_quiz.html",software_quiz),
    path("verbals_quiz.html",verbals_quiz),
    path("assesment.html",assesment_quiz),
    
]



