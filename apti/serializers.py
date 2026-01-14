from rest_framework import serializers
from .models import QuizSettings

class QuizSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSettings
        fields = '__all__'
