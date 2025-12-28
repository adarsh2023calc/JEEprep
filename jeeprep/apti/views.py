from django.shortcuts import render,redirect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .models import QuizSettings
from .serializers import QuizSettingsSerializer
from .api_logic.ai import generate_questions
from .api_logic.fetch import fetch_questions

# -----------------------------
# QUIZ SETTINGS LIST VIEW
# -----------------------------
class QuizSettingsListCreateView(generics.ListCreateAPIView):
    queryset = QuizSettings.objects.all()
    serializer_class = QuizSettingsSerializer


class QuizSettingsRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuizSettings.objects.all()
    serializer_class = QuizSettingsSerializer


# -----------------------------
# GENERATE QUIZ API
# -----------------------------

@method_decorator(csrf_exempt, name='dispatch')
class GenerateQuizView(APIView):
    def post(self, request):
        number = int(request.data.get("number", 10))
        difficulty = request.data.get("difficulty", "easy")
        topics = request.data.get("topics", [])
        print("Number is",number)
        try:
            questions = generate_questions(
                topics=topics,
                number=number,
                difficulty=difficulty
            )

            return Response({"questions": questions}, status=200)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=500)
    # -----------------------------
# HTML PAGES — SET CSRF COOKIE HERE
# -----------------------------
@ensure_csrf_cookie
def assesment_quiz(request):
    return render(request, "assesment.html")


def main_backend_page(request):
    return render(request, "index.html")


def aptitude_quiz(request):
    return render(request, "aptitude_quiz.html")


def software_quiz(request):
    return render(request, "software_quiz.html")


def verbals_quiz(request):
    return render(request, "verbals_quiz.html")


def score_view(request):
    return render(request,"score.html")

def leetcode_view(request):
    return render(request,"editor.html")



from .executor import run_python



@api_view(["POST"])

def run_code(request):
    code = request.data.get("code", "")
    lang = request.data.get("language", "python")
    args =  request.data.get("testcases", [])  # ["{...}", "{...}"]

    if lang == "python":
        output = run_python(code,args)
    else:
        return Response({"error": "Unsupported language"}, status=400)

    return Response({"output": output})

@api_view(["POST"])

def fetch_questions_boiler_plate(request):
    number= request.data.get("num",2)
    difficulty = request.data.get("difficulty","Medium")
    company= request.data.get("company","TCS")

    output = fetch_questions(number,difficulty,company)

    return Response({"output": output})



def render_questions_page(request):
    return render(request,"coding_questions.html")


@ensure_csrf_cookie
def render_landing_page(request):
    return render(request,"landing_page.html")



def render_dashboard(request):
    return render(request,"dashboard.html")



def login_view(request):

    if request.method=="POST":
        userName = request.POST['username']
        passWord = request.POST['password']
    
        user = authenticate(request,username=userName,password=passWord)

        if user:
            login(request,user)
            return redirect("dashboard")
        

        else:
            messages.error(request,"invalid_credentials")
            return redirect("/")
        
    return redirect("/?showLogin=true")
    


def logout_view(request):
    logout(request)
    return redirect('/')

    



def signup_view(request):
    if request.method=="POST":
        userName = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')


        if password1 != password2:
            messages.error(request,"Passwords do not match")

        if User.objects.filter(username=userName).exists():
            messages.error(request, "Username already exists")

            return render_dashboard(request)
        

        user = User.objects.create_user(username=userName,email=email,password=password1)
        user.save()
        messages.success(request,"Message saved successfully")

        return render_dashboard(request)
    
    return render(request,'landing_page.html')
