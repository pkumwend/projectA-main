from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404

from django.db import transaction
from django.utils import timezone

from .forms import HuntForm
from .models import Hunt

from .forms import QuestionForm,QuestionFormSet,EditQuestionFormSet
from .models import Question

from .forms import HuntSessionForm
from .models import HuntSession


from .forms import PlayerForm,ShortAnswerForm,MultipleChoiceForm,PictureForm
from .models import Player,Answer

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
        formset = QuestionFormSet(request.POST)
        
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
    
    if request.method == "POST":
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

    if request.method == "POST":
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
    return render(request, "sessions/manage_sessions.html", {"Sessions":Sessions})


@login_required(login_url="staff_login")
def session_detail(request,Session_id):
    Session = get_object_or_404(HuntSession,Session_id=Session_id)
    playing = Session.players.filter(submitted_at__isnull=True).count()
    done = Session.players.filter(submitted_at__isnull=False).count()
    return render(request, "sessions/session_detail.html", {"Session":Session,"playing":playing,"done":done}) 

@login_required(login_url="staff_login")
def delete_session(request,Session_id):
    instance = get_object_or_404(HuntSession,Session_id=Session_id)
    
    if request.method == "POST":
            instance.delete()
            return redirect("manage_sessions")
    return render(request, "sessions/delete_session.html", {'Session' : instance})

#########################  home and quiz ################################################
def homepage(request):
    if request.method == "POST":
        form = JoinCodeForm(request.POST)
        if form.is_valid():
            join_code = form.cleaned_data["join_code"].strip()
            hunt_session = HuntSession.objects.filter(join_code__iexact=join_code).first()

            #check if the session is active else redirect back to the the homepahge again

            if hunt_session is None:
                form.add_error("join_code","No code matches any sessions on site, check and try again")
            elif hunt_session.status != "active":
                form.add_error("join_code","Session is not active, check with your teacher")
            else:
                request.session["hunt_session_id"] = hunt_session.pk
                return redirect("join_hunt")
    else:
        form =  JoinCodeForm()
    return render(request, "home/home.html", {"form":form})


def join_hunt(request):
    session_id = request.session.get("hunt_session_id")
    if not session_id:
        return redirect("homepage")

    hunt_session = get_object_or_404(HuntSession,Session_id=session_id,status="active") 

    #maybe check if the player has an active session or a session in porgress un submitted and redirect to that session from before

    
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.session = hunt_session
            player.save()

            request.session["player_id"] = player.player_id
            return redirect("start_hunt")
    else:
        form = PlayerForm()
    return render(request, "home/join_hunt.html", {"form":form})


def get_player(request):
    #if a player hasnt finished a hunt, redirect them back to the hunt to continue
    player_id = request.session.get("player_id")
    if not player_id: 
        return None
    else:
        return (Player.objects.filter(player_id=player_id).select_related("session__hunt").first())

form_type = {"multiple choice":MultipleChoiceForm, "short answer":ShortAnswerForm,"picture":PictureForm}

def make_answer_forms(player,questions,data=None,files=None):
    #to apply the correct anser form for each question according to the type
    saved_answers = {answer.question_id:answer for answer in player.answers.all()}
    hunt_data = []

    for question in questions:
        form_class =  form_type.get(question.question_type)
        if form_class == None:
            continue
        kwargs = { "prefix":f"question_{question.question_id}","instance":saved_answers.get(question.question_id)}

        if form_class is MultipleChoiceForm:
            kwargs["question"] = question

        hunt_data.append({"question":question,"form":form_class(data,files,**kwargs)})

    return hunt_data


def start_hunt(request):
    #creating player instance and display questions
    player = get_player(request)
    if player is None:
        messages.error(request,"Enter a code to get started")
        return redirect("homepage")
    
    session = player.session
    hunt = session.hunt

    # check if the player has already completed the hunt and condition of sessions if joinable
    
    if player.submitted_at is not None:
        return redirect("thank_you")

    if session.status != "active":
        messages.error(request,"The session has ended")
        return redirect("homepage")
    
    questions = hunt.questions.order_by("question_id")

    if request.method == "POST":
        hunt_data = make_answer_forms(player,questions,request.POST,request.FILES)
        results = [item["form"].is_valid() for item in hunt_data]

        #create forms for player to enter answers as a transaction 
        #transfer to submission page where they can review answers before saving evrything
        if all(results):
            with transaction.atomic():
                for item in hunt_data:
                    #
                    answer =item["form"].save(commit=False)
                    answer.player = player 
                    answer.question = item["question"]
                    answer.save()
            return redirect("submission")
    else:
        hunt_data = make_answer_forms(player,questions)


    return render(request, "home/start_hunt.html",{"hunt_data":hunt_data,"player":player,"session":session,"hunt":hunt})

def has_response(answer):
    if answer is None:
        return False
    return bool(answer.choice_id or answer.answer.strip() or answer.picture)

def submission(request):
    #
    #find player data and load results, else redirect to home page
    player = get_player(request)

    if player is None:
        messages.error(request,"Enter a code to get started")
        return redirect("homepage")
    if player.submitted_at is not None:
        return redirect("thank_you")

    session = player.session
    hunt = session.hunt

    if session.status != "active":
        messages.error(request,"session has ended")
        return redirect("homepage")
    
    #for two button perform actions to confirm closure of quiz for specific player or return them to the hunt to continue answering
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "confirm":
            player.submitted_at = timezone.now()
            player.save(update_fields=["submitted_at"])
            return redirect("thank_you")
        if action == "review":
            return redirect("start_hunt")

    #loop throught the players answers and collcet data for questions that have not been answered
    questions = hunt.questions.order_by("question_id")
    saved_answers = {ans.question_id: ans for ans in player.answers.select_related("choice")}
    rows =[]
    unanswered = 0
    for question in questions:
        answer = saved_answers.get(question.question_id)
        answered = has_response(answer)
        if not answered:
            unanswered += 1
        rows.append({ "question":question,"answer":answer, "answered":answered })

    return render(request, "home/submission.html",{"rows":rows,"unanswered":unanswered,"player":player,"session":session,"hunt":hunt})

def thank_you(request):
    return render(request, "home/thank_you.html")

############################### marking related ##################################################

def view_submissions(request):
    #a simple view to display all the session and how many hunts students ahve submitted, 
    #each entry for a quiz should show the sessioin, total participants, submitted hunts and how manyhave been marked
    #the process will be split into 3 pages,
    #resue the manage session page, add a display for the submitted hunts as well
    #add a link to the marking review page, it will take that hunt and display a list of all the players
    #last page will be for individually marking each answer the player gave
    #end of notes
    return render (request,"marking/view_submissions.html")

def mark_player(request,player_id):
    #similar to the edit pages, take the player id and display all the answers they have given
    #add a boolean for marking if the question is correct or not,
    #later add a leader board that takes the completed marking players and puts them into a leader board for that quiz
    return render(request, "marking/mark_player.html")
