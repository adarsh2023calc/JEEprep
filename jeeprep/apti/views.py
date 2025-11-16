from django.shortcuts import render

# Create your views here.



def main_backend_page(request):

    return render(request,"index.html")

def aptitude_quiz(request):
    return render(request, "aptitude_quiz.html")