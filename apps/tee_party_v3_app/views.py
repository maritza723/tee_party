from django.shortcuts import render, redirect, HttpResponse
from apps.tee_party_v3_app.models import *
from django.contrib import messages
import datetime
import bcrypt

def index(request):
    return render(request, "tee_party_v3_app/index.html")

def register(request):
        
    error = Golfer.objects.validate(request.POST)

    if len(error) > 0:
    
        for key, value in error.items():
            messages.error(request, value)

        return redirect("/")

    else:
        hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        Golfer.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], handicap=request.POST['handicap'], best_scorecard=request.POST['best_scorecard'], email=request.POST['email'], password=hash, user_status="user")

    request.session["golfer_id"] = Golfer.objects.last().id
    return redirect("/dashboard")

def validate_login(request):
    golfer = Golfer.objects.filter(email=request.POST['email'])
    if golfer:
        logged_golfer = golfer[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_golfer.password.encode()):
            request.session["golfer_id"]=logged_golfer.id
            return redirect("/dashboard")
        else:       
            messages.success(request, "Password incorrect")
            return redirect("/")
    else:       
        messages.success(request, "Email address is unregistered")
        return redirect("/")


def dashboard(request):
    golfer = Golfer.objects.get(id=request.session["golfer_id"])

    golfer_tee_times = []
    for i in golfer.golfer_playing.all():
        golfer_tee_times.append(i.id)

    tee_time_courses = []
    for i in TeeTime.objects.filter(id__in=golfer_tee_times):
        tee_time_courses.append(i.id)


    list_with = []
    list_without = []
    courses = Course.objects.all()
    for i in courses:
        myboolean = False
        for j in i.tee_time_at_course.values():
            if j in golfer.golfer_playing.values():
                list_with.append(i)
                myboolean = True
                break
        if myboolean == False:
            list_without.append(i)

    
    context = {
        "golfer": golfer,
        "courses": Course.objects.all(),
        "tee_time_courses": tee_time_courses,
        "golfer_tee_times": golfer_tee_times,
        "teeTime": TeeTime.objects.filter(id__in=tee_time_courses),
        "allTeeTimes": TeeTime.objects.all(),
        "list_with" : list_with,
        "list_without": list_without,
    }

    return render(request, "tee_party_v3_app/dashboard.html", context)


def edit(request, golfer_id):

    context = {
        'golfer': Golfer.objects.get(id=request.session["golfer_id"]),
        'revise': Golfer.objects.get(id=golfer_id), 
        
    }
    return render(request, "tee_party_v3_app/update_golfer.html", context)

def update(request, golfer_id):

    error = Golfer.objects.update_validation(request.POST)

    if len(error) > 0:

        for key, value in error.items():
            messages.error(request, value)

        return redirect("/edit/" + str(golfer_id))
    else:

        revise = Golfer.objects.get(id=golfer_id)
        revise.handicap = request.POST['handicap']
        revise.best_scorecard = request.POST['best_scorecard']     
        revise.save()

    return redirect("/dashboard")


def new(request):
    context = {
        "golfer": Golfer.objects.get(id=request.session["golfer_id"]),
        "golfers": Golfer.objects.all(),
        "courses": Course.objects.all()
    }
    return render(request, "tee_party_v3_app/new_course.html", context)

def create(request):
    
    error = Course.objects.basic_validate(request.POST)

    if len(error) > 0:
        

        for key, value in error.items():
            messages.error(request, value)

        return redirect("/new_course")

    else:
        Course.objects.create(name=request.POST['name'], address=request.POST['address'], par=request.POST['par'], rating=request.POST['rating'], slope=request.POST['slope'])


    return redirect("/dashboard")


def allCourses(request):
    context = {
        "golfer": Golfer.objects.get(id=request.session["golfer_id"]),
        "course": Course.objects.all()
    }
    return render(request, "tee_party_v3_app/all_courses.html", context)


def course(request, course_id):
    context = {
        "golfer": Golfer.objects.get(id=request.session["golfer_id"]),
        "course": Course.objects.get(id=course_id),
        "courses": Course.objects.all()
    }
    return render(request, "tee_party_v3_app/course.html", context)

def teeTime(request, course_id):

    context = {
        "course": Course.objects.get(id=course_id),
        "courses": Course.objects.all(),
        "golfer": Golfer.objects.get(id=request.session["golfer_id"]),
        "golfers": Golfer.objects.all(),
        "tee": TeeTime.objects.all()         
    }
    return render(request, "tee_party_v3_app/tee_time.html", context)

def schedule(request, course_id):
    course = Course.objects.get(id=course_id)
    golfer = Golfer.objects.get(id=request.session["golfer_id"])


    TeeTime.objects.create(tee_time=request.POST['tee_time'], location=course, player=golfer)



    return redirect("/dashboard")


def delete(request, tee_time_id):
    bye = TeeTime.objects.get(id=tee_time_id)
    bye.delete()
    return redirect("/dashboard")

