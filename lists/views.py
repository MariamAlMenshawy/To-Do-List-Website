import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from .models import Task
from django.contrib.auth.models import User
from .forms import NewTaskForm
# Create your views here.

def home(request):
    return render(request,'home.html')

def listTodayTasks(request):
    today = datetime.date.today()
    tasks = Task.objects.filter(due_date = today)
    return render(request,'today_list.html',{'tasks':tasks})

def listWeekTasks(request):
    today = datetime.date.today() 
    days_to_saturday = (today.weekday() + 2) % 7
    start_of_week = today - datetime.timedelta(days = days_to_saturday)
    end_of_week = start_of_week + datetime.timedelta(days=6)
    tasks = Task.objects.filter(due_date__range=[start_of_week, end_of_week])
    return render(request,'week_list.html',{'tasks':tasks})

def listMonthTasks(request):
    today = datetime.date.today()
    start_of_month = today.replace(day=1)
    
    if today.month == 12: #لو تاريخ اليوم الشهر فيه بيساوي 12 
        next_month = today.replace(year=today.year+1, month=1, day=1)  # كده هنكون في اول يوم في السنة الجديدة
    else:
        next_month = today.replace(month=today.month+1, day=1) # الشهور هتمشي عادي 
    
    end_of_month = next_month - datetime.timedelta(days=1) # اخر يوم في الشهر بيساوي اليوم اللي قبل اول يوم في الشهر الجاي
    tasks = Task.objects.filter(due_date__range=[start_of_month, end_of_month])
    return render(request,'month_list.html',{'tasks':tasks})

def listYearTasks(request):
    today = datetime.date.today()
    start_of_year = today.replace(month=1, day=1) # اول يوم في السنة
    end_of_year = today.replace(month=12, day=31) # اخر يوم في السنة
    tasks = Task.objects.filter(due_date__range=[start_of_year, end_of_year])
    return render(request,'year_list.html',{'tasks':tasks})

def listNoDeadlineTasks(request):
    tasks = Task.objects.filter(due_date=None)
    return render(request,'no_deadline_list.html',{'tasks':tasks})

def allTasks(request):
    tasks = Task.objects.all()
    return render(request,'all_tasks.html',{'tasks':tasks})

def task_done(request, task_id):
    next_url = request.GET.get('next', '/')
    task = get_object_or_404(Task, id=task_id)

    task.is_done = not task.is_done
    task.save()
    return redirect(request.POST.get('next', next_url)) # عشان يرجع للصفحة اللي كان فيها


@login_required
def addTask(request):
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = NewTaskForm(request.POST) #بنملى الفورم بالبيانات اللي المستخدم دخلها
        if form.is_valid():   #نتأكد إن البيانات سليمة
            task = form.save(commit=False)  #بنحفظ مؤقتًا من غير ما يتسجل في الداتا بيز
            task.user = request.user
            task.save()

            return redirect(request.POST.get('next', next_url)) # عشان يرجع للصفحة اللي كان فيها
    else:
        form = NewTaskForm()

    return render(request,'add_task.html',{'form':form, 'next': next_url})

