from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm  #عشان نقدر نستخدم الفورم بتاعت دجانجو
from django.contrib.auth import login as auth_login #كده انا سمشتها اسم مختلف 
from .forms import SignUpForm
from django.contrib.auth import logout
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
# Create your views here.

def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)  #بنعمل تسجيل دخول تلقائي بعد التسجيل

            return redirect('home')
    
    return render(request,'signup.html',{'form':form})

def logOut(request):
    logout(request)
    return redirect('home')

class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name','last_name','email')
    template_name = 'my_account.html'
    success_url = reverse_lazy('home')

    def get_object(self):    
        return self.request.user
    
    
