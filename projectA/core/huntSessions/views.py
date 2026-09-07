from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import HuntForm
from .models import Hunt

from .forms import QuestionForm
from .models import Question

def is_allowed(user):
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

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, "Login successful.")

            if user.is_superuser:
                return redirect("admin_dashboard")

            return redirect("staff_dashboard")

        messages.error(
            request,
            "Invalid username, password, or staff permission."
        )

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

@login_required(login_url="staff_login")
def manage_hunts(request):
    hunts = Hunt.objects.all()
    return render(request, "hunts/manage_hunts.html", {'hunts' : hunts})



@login_required(login_url="staff_login")
def manage_sessions(request):
    return render(request, "sessions/manage_sessions.html")

def staff_logout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logout successful.")
    return redirect("staff_login")

##################################################################################################

@login_required(login_url="staff_login")
def create_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("question_pool")
    else:
        form = QuestionForm()
    return render (request, "questions/create_question.html", {'form': form})

@login_required(login_url="staff_login")
def question_pool(request):
    questions = Question.objects.all()
    return render(request, "questions/question_pool.html",{"questions":questions})


@login_required(login_url="staff_login")
def edit_question(request,question_id):
    instance = Question.objects.get(question_id=question_id)
    form = QuestionForm(instance= instance)

    if request.method == "POST":
        form = QuestionForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            return redirect("manage_questions")
    return render(request, "questions/edit_question.html", {'form' : form})


@login_required(login_url="staff_login")
def delete_question(request,question_id):
    instance = Question.objects.get(question_id=question_id)
    form = QuestionForm(instance= instance)
    if request.method == "POST":
            form = QuestionForm(request.POST,instance=instance)
            instance.delete()
            return redirect("question_pool")

    return render(request, "questions/delete_question.html", {'question' : instance})

####################################################################
#forms views for getting data from user on 


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
def edit_hunt(request,hunt_id):
    instance = Hunt.objects.get(hunt_id=hunt_id)
    form = HuntForm(instance= instance)
    if request.method == "POST":
        form = HuntForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            return redirect("manage_hunts")
    return render(request, "hunts/edit_hunt.html", {'form' : form})

@login_required(login_url="staff_login")
def delete_hunt(request,hunt_id):

    instance = Hunt.objects.get(hunt_id=hunt_id)

    form = HuntForm(instance= instance)

    if request.method == "POST":
            form = HuntForm(request.POST,instance=instance)
            instance.delete()
            return redirect("manage_hunts")

    return render(request, "hunts/delete_hunt.html", {'hunt' : instance})