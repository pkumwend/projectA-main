from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from huntSessions.forms import HuntForm
from huntSessions.models import Hunt

from huntSessions.forms import QuestionForm
from huntSessions.models import Question

from huntSessions.forms import HuntSessionForm
from huntSessions.models import HuntSession


from huntSessions.forms import PlayerForm
from huntSessions.models import Player

from huntSessions.forms import JoinCodeForm

from django.contrib import messages

# Create your views here.
def homepage(request):
    return render(request, "home/home.html")


###############player and answers stuff##############################
def homepage(request):
    if request.method == "POST":
        form = JoinCodeForm(request.POST)
        if form.is_valid():
            join_code = form.cleaned_data["join_code"]
            session = HuntSession.objects.filter(join_code=join_code).first()
            #session = get_object_or_404(HuntSession,join_code=join_code)

            if session is None:
                messages.error(request, "Incorrect code, Please check the join code and try again")
                return redirect("homepage")

            request.session["hunt_session_id"] = session.Session_id

            return redirect("join_hunt")
    else:
        form =  JoinCodeForm()
    return render(request, "home/home.html", {"form":form})


def join_hunt(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            session_id = request.session.get("hunt_session_id")
            session = get_object_or_404(HuntSession,Session_id=session_id)
            Player = form.save(commit=False)
            Player.session = session
            Player.save()
            request.session["player_id"] = Player.player_id
            return redirect("start_hunt")
    else:
        form = PlayerForm()
    return render(request, "home/join_hunt.html", {"form":form})

def start_hunt(request):
    player_id = request.session.get("player_id")
    player = get_object_or_404(Player,player_id=player_id)
    session = player.session
    hunt = session.hunt
    questions = hunt.questions.all()

    return render(request, "home/start_hunt.html",{"player":Player,"session":session,"hunt":hunt,"questions":questions})
