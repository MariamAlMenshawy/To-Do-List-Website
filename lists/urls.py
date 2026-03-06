from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    
    path('today/',views.listTodayTasks,name='today_list'),
    path('week/',views.listWeekTasks,name='week_list'),
    path('month/',views.listMonthTasks,name='month_list'),
    path('year/',views.listYearTasks,name='year_list'),
    path('nodeadline/',views.listNoDeadlineTasks,name='no_deadline_list'),
    path('all_tasks/',views.allTasks,name='all_tasks'),
    
    path('add_task/',views.addTask,name='add_task'),
    path('task/<int:task_id>/task_done/', views.task_done, name='task_done'),
    path('task/<int:task_id>/update/', views.UpdateTask.as_view(), name='update_task'),
    path('task/<int:task_id>/delete/', views.DeleteTask.as_view(), name='delete_task'),
]



