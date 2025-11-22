from django.db import models

# Create your models here.

class QuizSettings(models.Model):
    topic = models.CharField()
    number = models.IntegerField()
    time = models.IntegerField()
    difficulty = models.CharField(max_length=20)
    is_negative = models.BooleanField()

    # store topics like: ["os", "dbms", "aptitude", "verbal"]
    topics = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)




    def __str__(self):
        return f"Quiz Settings #{self.id}"
