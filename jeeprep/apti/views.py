from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from django.utils.decorators import method_decorator

from .models import QuizSettings
from .serializers import QuizSettingsSerializer
from .api_logic.ai import generate_questions

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
        number = request.data.get("number", 10)
        difficulty = request.data.get("difficulty", "easy")
        topics = request.data.get("topics", {})

        try:
            questions = generate_questions(
                topics=topics,
                number=number,
                difficulty=difficulty
            )
            return Response({"questions": questions}, status=200)
        except Exception as e:
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
