from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('today/',views.listTodayTasks,name='today_list'),
    path('week/',views.listWeekTasks,name='week_list'),
    path('month/',views.listMonthTasks,name='month_list'),
    path('year/',views.listYearTasks,name='year_list'),
    path('nodeadline/',views.listNoDeadlineTasks,name='no_deadline_list'),
    path('add_task/',views.addTask,name='add_task'),
    path('all_tasks/',views.allTasks,name='all_tasks'),
    path('task/<int:task_id>/task_done/', views.task_done, name='task_done'),
]