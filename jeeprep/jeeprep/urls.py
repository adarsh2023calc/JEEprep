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
from apti.views import main_backend_page,aptitude_quiz,software_quiz,verbals_quiz,\
    assesment_quiz,score_view , leetcode_view,run_code,render_questions_page,\
        fetch_questions_boiler_plate,render_landing_page,render_dashboard,login_view,logout_view,\
       signup_view,save_assesment_details,save_score_details,update_assesment,\
       fetch_past_assessments
       
from apti.views import (
    GenerateQuizView
)



urlpatterns = [
    path("",render_landing_page,name="landing"),
    path("index.html", main_backend_page),
    path("aptitude_quiz.html", aptitude_quiz),
    path("software_quiz.html",software_quiz),
    path("verbals_quiz.html",verbals_quiz),
    path("assesment.html",assesment_quiz),
    path("api/generate_quiz/", GenerateQuizView.as_view(), name="generate_quiz"),
    path("score.html",score_view),
    path("editor.html",leetcode_view),
    path('api/run/', run_code),
    path('api/get_questions/',fetch_questions_boiler_plate),
    path('coding_questions.html',render_questions_page),
    path('dashboard.html',render_dashboard,name="dashboard"),
    path('signup',signup_view,name="signup"),
    path('logout',logout_view,name="logout"),
    path('login',login_view,name="login"),
    path('api/save_details/',save_assesment_details),
    path('api/save_score/',save_score_details),
    path('api/update_assesment/',update_assesment),
    path('api/get_details/',fetch_past_assessments)
]



