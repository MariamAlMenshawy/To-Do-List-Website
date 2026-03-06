from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from to_do_list import settings
urlpatterns = [
   path('signup/',views.signup,name='signup'),
   path('logout/',views.logOut,name = 'logout'),
   path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
   path('settings/change_passsword/',auth_views.PasswordChangeView.as_view(template_name='change_password.html'),name='password_change'),
   path('settings/change_passsword/done/',auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'),name='password_change_done'),
   path('account/',views.UserUpdateView.as_view(),name='my_account'),
]