from django.shortcuts import render

# Create your views here.



def main_backend_page(request):
    return render(request,"index.html")

def aptitude_quiz(request):
    return render(request, "aptitude_quiz.html")

def software_quiz(request):
    return render(request, "software_quiz.html")

def verbals_quiz(request):
    return render(request, "verbals_quiz.html")


def assesment_quiz(request):
    return render(request,"assesment.html")

def gotojs(request):
    return render(request,"goto.js")


