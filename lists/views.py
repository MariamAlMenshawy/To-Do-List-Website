import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,get_object_or_404
from .models import Task
from django.contrib.auth.models import User
from .forms import NewTaskForm, UpdateTaskForm
from django.views.generic import DeleteView, UpdateView
from django.utils.decorators import method_decorator

# Create your views here.

def home(request):
    return render(request,'home.html')

@login_required
def listTodayTasks(request):
    status = request.GET.get('status')
    today = datetime.date.today()
    tasks = Task.objects.filter(user=request.user,due_date__date = today)

    if status == 'done':
        tasks = tasks.filter(is_done=True)
    elif status == 'pending':
        tasks = tasks.filter(is_done=False)

    return render(request,'today_list.html',{'tasks':tasks})

@login_required
def listWeekTasks(request):
    status = request.GET.get('status')
    today = datetime.date.today() 
    days_to_saturday = (today.weekday() + 2) % 7
    start_of_week = today - datetime.timedelta(days = days_to_saturday)
    end_of_week = start_of_week + datetime.timedelta(days=6)

    tasks = Task.objects.filter(user=request.user,due_date__range=[start_of_week, end_of_week])
    
    if status == 'done':
        tasks = tasks.filter(is_done=True)
    elif status == 'pending':
        tasks = tasks.filter(is_done=False)

    return render(request,'week_list.html',{'tasks':tasks})

@login_required
def listMonthTasks(request):
    status = request.GET.get('status')
    today = datetime.date.today()
    start_of_month = today.replace(day=1)
    
    if today.month == 12: #لو تاريخ اليوم الشهر فيه بيساوي 12 
        next_month = today.replace(year=today.year+1, month=1, day=1)  # كده هنكون في اول يوم في السنة الجديدة
    else:
        next_month = today.replace(month=today.month+1, day=1) # الشهور هتمشي عادي 
    
    end_of_month = next_month - datetime.timedelta(days=1) # اخر يوم في الشهر بيساوي اليوم اللي قبل اول يوم في الشهر الجاي
    tasks = Task.objects.filter(user=request.user,due_date__range=[start_of_month, end_of_month])

    if status == 'done':
        tasks = tasks.filter(is_done=True)
    elif status == 'pending':
        tasks = tasks.filter(is_done=False)

    return render(request,'month_list.html',{'tasks':tasks})

@login_required
def listYearTasks(request):
    status = request.GET.get('status')
    today = datetime.date.today()
    start_of_year = today.replace(month=1, day=1) # اول يوم في السنة
    end_of_year = today.replace(month=12, day=31) # اخر يوم في السنة
    
    tasks = Task.objects.filter(user=request.user,due_date__range=[start_of_year, end_of_year])

    if status == 'done':
        tasks = tasks.filter(is_done=True)
    elif status == 'pending':
        tasks = tasks.filter(is_done=False)
    
    return render(request,'year_list.html',{'tasks':tasks})

@login_required
def listNoDeadlineTasks(request):
    status = request.GET.get('status')
    tasks = Task.objects.filter(user=request.user,due_date=None)

    if status == 'done':
        tasks = tasks.filter(is_done=True)
    elif status == 'pending':
        tasks = tasks.filter(is_done=False)

    return render(request,'no_deadline_list.html',{'tasks':tasks})

@login_required
def allTasks(request):
    status = request.GET.get('status')
    tasks = Task.objects.filter(user=request.user)

    if status == 'done':
        tasks = tasks.filter(is_done=True)
    elif status == 'pending':
        tasks = tasks.filter(is_done=False)
        
    return render(request, 'all_tasks.html', {'tasks': tasks})


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

@method_decorator(login_required,name='dispatch')  #لازم يسجل دخول الاول عشان يعرف يعمل ريبلاي
class UpdateTask(UpdateView):
    model = Task
    form_class = UpdateTaskForm
    template_name = 'update_task.html'
    pk_url_kwarg = 'task_id'
    context_object_name = 'task'
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        task = form.save(commit=False)
        task.updated_at = timezone.now()
        task.save()

        next_url = self.request.GET.get('next', '/')
        return redirect(next_url)

@method_decorator(login_required,name='dispatch')  #لازم يسجل دخول الاول عشان يعرف يعمل ريبلاي
class DeleteTask(DeleteView):
    model = Task 
    pk_url_kwarg = 'task_id'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_success_url(self):
        next_url = self.request.GET.get('next', '/')
        return next_url