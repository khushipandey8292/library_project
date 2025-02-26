from django.shortcuts import render,HttpResponseRedirect
from .forms import SignupForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
def home(request):
    return render(request,'index.html')


def signup(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            messages.success(request,'congratulations!! Account is created successfully!!')
            user=form.save()
            form=SignupForm()
    else:
      form=SignupForm()
    return render(request,'signup.html',{'form':form})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form=LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'logged in successfully') 
                    return HttpResponseRedirect('/dashboard/')        
        else:
            form=LoginForm()
        return render(request,'login.html',{'form':form})   
    else: 
        return HttpResponseRedirect('/dashboard/')
    
def dashboard(request):
    return render(request,'dashboard.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/home/')