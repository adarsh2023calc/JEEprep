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
        fetch_questions_boiler_plate,render_landing_page,render_dashboard
from apti.views import (
    GenerateQuizView
)



urlpatterns = [
    path("",render_landing_page),
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
    path('dashboard.html',render_dashboard)
]



