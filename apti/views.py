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
from rest_framework import status
from google_auth_oauthlib.flow import InstalledAppFlow

from .models import QuizSettings
from .serializers import QuizSettingsSerializer
from .api_logic.ai import generate_questions,fetch_sql_quiz_ai
from .api_logic.fetch import fetch_questions
from .api_logic.db import (
    save_to_mongodb,
    fetch_from_mongodb,
    save_score_to_mongodb,
    fetch_score_from_mongodb,
    fetch_purpose_pipeline_from_mongodb,
    
)

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
        user_id = request.data.get("user_id")  # Add user_id

        print("Number is",number)
        try:
            # Adaptive learning: if user_id provided, adjust topics based on weak areas
            weak_topics = None
            if user_id:
                weak_topics = self.get_weak_topics(user_id)
                if weak_topics:
                    # Include weak topics in the selected topics
                    topics = list(set(topics + weak_topics))
                    # Adjust difficulty if struggling
                    if difficulty == "easy":
                        pass  # keep easy
                    else:
                        difficulty = "medium"  # lower difficulty for weak topics

            questions = generate_questions(
                topics=topics,
                number=number,
                difficulty=difficulty,
                weak_topics=weak_topics
            )

            return Response({"questions": questions}, status=200)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=500)

    def get_weak_topics(self, user_id):
        # Fetch topic accuracies and return topics with low accuracy
        from .api_logic.db import fetch_purpose_pipeline_from_mongodb
        accuracies = fetch_purpose_pipeline_from_mongodb(user_id)
        weak_topics = [topic for topic, acc in accuracies.items() if acc < 50]
        return weak_topics[:5]  # limit to 5 weak topics
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

def render_sql_quiz_page(request):
    return render(request,"sql_quiz.html")

def render_sql_editor_page(request):
    return render(request,"sql_editor.html")



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
    number= request.data.get("number")

    difficulty = request.data.get("difficulty","Medium")
    company= request.data.get("company")

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
        
        

        user = User.objects.create_user(username=userName,email=email,password=password1)
        user.save()
        messages.success(request,"Message saved successfully")
        return render(request,'landing_page.html')



@api_view(["POST"])
def save_assesment_details(request):
    

    try:
        user_id = request.data.get("user_id")
        assessment_id = request.data.get("assesment_id")  # fixed spelling
        data = request.data.get("body")
        purpose = request.data.get("purpose")

        # Basic validation
        if not all([assessment_id, data, purpose]):
            return Response(
                {"error": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        success = save_to_mongodb(user_id, assessment_id, data, purpose)

        if not success:
            return Response(
                {"error": "Failed to insert into BigQuery"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"status": "ok"}, status=status.HTTP_200_OK)

    except Exception as e:
        print("MongoDB Error:", str(e))
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


    
@api_view(["POST"])
def save_score_details(request):
    print(request)
    try:
        user_id= request.data.get("user_id")
        assessment_id=request.data.get("assessment_id")
        correct = request.data.get("correct")
        incorrect = request.data.get("incorrect")
        unattempted = request.data.get("unattempted")
        purpose = request.data.get("purpose")
        
        save_score_to_mongodb(user_id=user_id,assessment_id=assessment_id,\
                            correct_questions=correct,incorrect_questions=incorrect,\
                                unattempted_questions=unattempted,purpose=purpose)
        
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    except Exception as e:
        print("MongoDB Error:", str(e))
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@api_view(["PUT"])
def update_assesment(request):
    pass



@api_view(["POST"])
def fetch_past_assessments(request):
     try:
        user_id = request.data.get("user_id")
        result =fetch_from_mongodb(user_id)
        return Response(result)
     
     except Exception as e:
        print("Error:", str(e))
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def get_score(request):
    try:
        user_id= request.data.get("user_id")
        result = fetch_score_from_mongodb(user_id)
        return Response(result)
    
    except Exception as e:
        print("MongoDb Error: ",e)
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
def fetch_purpose_pipeline(request):
    try:
        user_id= request.data.get("user_id")
        result = fetch_purpose_pipeline_from_mongodb(user_id)
        return Response(result)
    
    except Exception as e:
        print("MongoDb Error: ",e)
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@api_view(["GET","POST"])
def google_login(request):

    if (request.method=='GET'):
            print("Initiating Google OAuth flow")
            flow = InstalledAppFlow.from_client_secrets_file(
                'secrets.json',
                scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
            )
            flow.redirect_uri = 'https://jeeprep-myl7.onrender.com/dashboard.html'
            return redirect(flow.authorization_url()[0])

    elif (request.method=='POST'):
        code = request.data.get("code")
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
        )
        flow.redirect_uri = 'https://jeeprep-myl7.onrender.com/dashboard.html'
        flow.fetch_token(code=code)
        credentials = flow.credentials
        id_info = credentials.id_token
        email = id_info.get("email")
        name = id_info.get("name")      
        user, created = User.objects.get_or_create(username=email, defaults={'email': email, 'first_name': name})
        login(request, user)
    
    
    return Response({"message": "Google login successful"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def fetch_sql_quiz(request):

    return Response(fetch_sql_quiz_ai(request.data))

