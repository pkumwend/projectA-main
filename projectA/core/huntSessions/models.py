from django.db import models

# Create your models here.

question_types = [("multiple choice","Multiple Choice"),
                  ("short answer","Short Answer"),
                  ("picture","Picture Submission"),]

status_types = [("draft","Draft"),
                ("active","Active"),
                ("finished","Finished")]

locations = [("Joondalup","Joondalup"),
             ("Bunburry","Bunbury"),
             ("City Campus","City Campus")]

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000)
    question_type = models.CharField(max_length=25,choices=question_types)
    def __str__(self):
        return self.description
    
class Hunt(models.Model):
    hunt_id = models.AutoField(primary_key=True)
    hunt_name = models.CharField(max_length=200)
    location = models.CharField(max_length=50,choices=locations)
    questions = models.ManyToManyField(Question)
    def __str__(self):
        return self.hunt_name

 
class HuntSession(models.Model):
    Session_id = models.AutoField(primary_key=True)
    hunt = models.ForeignKey(Hunt,on_delete=models.CASCADE, related_name="huntSessions")
    status = models.CharField(max_length=20,choices=status_types)
    join_code = models.CharField(max_length=6,unique=True)
    def __str__(self):
        return self.Session_id

'''
#habdle after  finishing the sessions stuff

class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=35)
    sessions = models.ForeignKey(HuntSession,on_delete=models.CASCADE,related_name="playerSessions")

class Answer(models.Model):
    players_id = models.ForeignKey(Player, on_delete=models.CASCADE,related_name="playersId")
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name="question")
    answer = CharField


'''