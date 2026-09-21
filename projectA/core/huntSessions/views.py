from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404

from .forms import HuntForm
from .models import Hunt

from .forms import QuestionForm,QuestionFormSet,EditQuestionFormSet
from .models import Question

from .forms import HuntSessionForm
from .models import HuntSession


from .forms import PlayerForm
from .models import Player

from .forms import JoinCodeForm

################################################################################
#Admin and staff login section

def is_admin(user):
    return user.is_superuser
 
def staff_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin_dashboard")

        if request.user.is_staff:
            return redirect("staff_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request,username=username,password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, "Login successful.")
            if user.is_superuser:
                return redirect("admin_dashboard")
            return redirect("staff_dashboard")
        messages.error(request,"Invalid username, password, or staff permission.")

    return render(request, "login/staff_login.html")


@login_required(login_url="staff_login")
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("staff_dashboard")
    return render(request, "login/admin_welcome.html")


@login_required(login_url="staff_login")
def staff_dashboard(request):
    if request.user.is_superuser:
        return redirect("admin_dashboard")
    return render(request, "login/staff_welcome.html")


def staff_logout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logout successful.")
    return redirect("staff_login")

##################################################################################################
#questions related

@login_required(login_url="staff_login")
def create_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        
        if form.is_valid():
            question = form.save()
            formset = QuestionFormSet(request.POST,instance=question)
            if formset.is_valid():
                formset.save()
                return redirect("question_pool")
    else:
        form = QuestionForm()
        formset = QuestionFormSet()

    return render (request, "questions/create_question.html", {'form':form,'formset': formset})

@login_required(login_url="staff_login")
def question_pool(request):
    questions = Question.objects.all()
    return render(request, "questions/question_pool.html",{"questions":questions})


@login_required(login_url="staff_login")
def edit_question(request,question_id):
    instance =get_object_or_404(Question,question_id=question_id)
    form = QuestionForm(instance= instance)
    formset = EditQuestionFormSet(instance= instance)

    if request.method == "POST":
        form = QuestionForm(request.POST,instance=instance)
        formset = EditQuestionFormSet(request.POST,instance=instance)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("question_pool")
    return render(request, "questions/edit_question.html", {'form' : form,'formset':formset})


@login_required(login_url="staff_login")
def delete_question(request,question_id):
    instance = get_object_or_404(Question,question_id=question_id)
    form = QuestionForm(instance= instance)
    if request.method == "POST":
            form = QuestionForm(request.POST,instance=instance)
            instance.delete()
            return redirect("question_pool")

    return render(request, "questions/delete_question.html", {'question' : instance})

################################################################################################
#hunts related


@login_required(login_url="staff_login")
def create_hunt(request):
    if request.method == "POST":
        form = HuntForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage_hunts")
    else:
        form = HuntForm()
    return render(request, "hunts/create_hunt.html",{'form': form}) 

@login_required(login_url="staff_login")
def manage_hunts(request):
    hunts = Hunt.objects.all()
    return render(request, "hunts/manage_hunts.html", {'hunts' : hunts})

@login_required(login_url="staff_login")
def edit_hunt(request,hunt_id):
    instance = get_object_or_404(Hunt,hunt_id=hunt_id)
    form = HuntForm(instance= instance)
    if request.method == "POST":
        form = HuntForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            return redirect("manage_hunts")
    return render(request, "hunts/edit_hunt.html", {'form' : form})

@login_required(login_url="staff_login")
def delete_hunt(request,hunt_id):

    instance = get_object_or_404(Hunt,hunt_id=hunt_id)

    form = HuntForm(instance= instance)

    if request.method == "POST":
            form = HuntForm(request.POST,instance=instance)
            instance.delete()
            return redirect("manage_hunts")

    return render(request, "hunts/delete_hunt.html", {'hunt' : instance})


###############################################################################################
#sessions related

@login_required(login_url="staff_login")
def create_session(request):
    if request.method == "POST":
        form = HuntSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("manage_sessions")
    else:
        form = HuntSessionForm()
    return render(request, "sessions/create_session.html",{'form': form})     


@login_required(login_url="staff_login")
def edit_session(request,Session_id):
    instance = get_object_or_404(HuntSession,Session_id=Session_id)
    form = HuntSessionForm(instance= instance)
    if request.method == "POST":
        form = HuntSessionForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            return redirect("manage_sessions")
    return render(request, "sessions/edit_session.html", {'form' : form})

@login_required(login_url="staff_login")
def manage_sessions(request):
    Sessions = HuntSession.objects.all()
    hunts = Hunt.objects.all()
    return render(request, "sessions/manage_sessions.html", {"Sessions":Sessions})


@login_required(login_url="staff_login")
def session_detail(request,Session_id):
    Session = get_object_or_404(HuntSession,Session_id=Session_id)
    return render(request, "sessions/session_detail.html", {"Session":Session}) 

@login_required(login_url="staff_login")
def delete_session(request,Session_id):
    instance = get_object_or_404(HuntSession,Session_id=Session_id)
    form = HuntSessionForm(instance= instance)
    if request.method == "POST":
            form = HuntSessionForm(request.POST,instance=instance)
            instance.delete()
            return redirect("manage_sessions")
    return render(request, "sessions/delete_session.html", {'Session' : instance})

#########################  home and quiz ################################################
def homepage(request):
    if request.method == "POST":
        form = JoicCodeForm(request.POST)
        if form.is_valid():
            join_code = form.cleaned_data["join_code"]
            session = get_object_or_404(HuntSession,join_code=join_code)

            request.session["hunt_session_id"] = session.Session_id

            return redirect("join_hunt")
    else:
        form =  JoinCodeForm()
    return render(request, "home/home.html", {"form":form})


def join_hunt(request):
    if request.Method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            session_id = request.session.get("hunt_session_id")
            session = get_object_or_404(HuntSession,join_code=join_code)
            Player = form.save(commit=False)
            player.session = session
            player.save()
            request.session["player_id"] = Player.player_id
            return redirect("start_hunt")
    else:
        form = PlayerForm()
    return render(request, "home/join_hunt.html", {"form":form})

def start_hunt(request):
    palyer_id = request.sesssion.get("player_id")
    player = get_object_or_404(Player,player_id=player_id)
    session = player.session
    hunt = session.hunt
    questions = hunt.questions.all()

    return render(request, "home/questions.html",{"player":player,"session":session,"hunt":hunt,"questions":questions})
