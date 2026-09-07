from django.db import models

# Create your models here.


class Hunt(models.Model):
    hunt_id = models.AutoField(primary_key=True)
    hunt_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

'''
class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000)
    question_type = models.CharField(max_length=50)
    answer = models.CharField(max_length=250)
'''