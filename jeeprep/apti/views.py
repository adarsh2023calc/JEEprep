from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view


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
