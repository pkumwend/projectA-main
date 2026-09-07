from django.db import models

# Create your models here.

question_types = [("multiple choice","Multiple Choice"),
                  ("short answer","Short Answer"),
                  ("picture","Picture Submission"),]

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000)
    question_type = models.CharField(max_length=50,choices=question_types)
    def __str__(self):
        return self.description
    
class Hunt(models.Model):
    hunt_id = models.AutoField(primary_key=True)
    hunt_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question)
