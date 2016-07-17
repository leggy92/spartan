import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import *
from django.http import HttpResponse

from .models import *


def index(request):
    if request.user.is_authenticated():
        return redirect('dashboard')
    else:
        return render(request, 'training/index.html', {'users_count': User.objects.all().count()})


@login_required
def dashboard(request):
    previous_workouts = Workout.objects.filter(user=request.user).order_by('-pk')
    return render(request, 'training/dashboard.html', {'previous_workouts': previous_workouts,
                                                       'most_common_excercises': Excercise.most_common()})


@login_required
def start_workout(request):
    s = Workout()
    s.user = request.user
    s.save()
    return redirect('training_session', s.id)


@login_required
def finish_workout(request, training_session_id):
    s = Workout.objects.get(pk=training_session_id)
    s.finish()
    s.save()
    return redirect('training_session', s.id)


@login_required
def training_session(request, training_session_id):
    workout = Workout.objects.get(pk=training_session_id, user=request.user)
    return render(request, 'training/workout.html', {'workout': workout,
                                                     'most_common_reps': Reps.most_common(),
                                                     'most_common_excercises': Excercise.most_common()})


@login_required
def add_excercise(request, training_session_id):
    s = Workout.objects.get(pk=training_session_id, user=request.user)
    s.excercise_set.create(name=request.POST['name'])
    try:
        s.start()
    except:
        pass
    s.save()
    return redirect('training_session', training_session_id)


@login_required
def add_reps(request, excercise_id):
    s = Excercise.objects.get(pk=excercise_id, workout__user=request.user)
    reps = s.reps_set.create(reps=request.POST['reps'])
    reps.time_created = datetime.datetime.now()
    reps.save()
    return redirect('training_session', s.workout.id)
