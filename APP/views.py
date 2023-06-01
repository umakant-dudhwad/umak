from django.shortcuts import render, HttpResponse, redirect
from django.shortcuts import render
from joblib import load
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from joblib import load
from django.contrib import messages
# Create your views here.

model=load('./model.joblib')

def signupview(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        try:
          my_user = User.objects.create_user(uname, email, password1)
          my_user.first_name = firstname
          my_user.last_name = lastname
          my_user.save()
          return redirect('login')
        except:
            messages.error(request,'This User already exist please Login')
    return render(request, 'signup.html')


def login(request):
    
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = auth.authenticate(request, username=uname, password=pass1)
        if user is not None:
            auth_login(request, user)
            print(user)
            return redirect("home")
        else:
            messages.error(request,'username or password not correct')
            return redirect("login")
    return render(request, 'login.html')


@login_required(login_url='login')
def home(request):
    
    return render(request, "home.html")


def Logoutpage(request):
    logout(request)
    return redirect('login')


def result(request):
    age = request.GET['age']
    glucose = request.GET['glucose']
    totchol = request.GET['totchol']
    sysBP = request.GET['sysBP']
    diaBP = request.GET['diaBP']
    prevalentHyp = request.GET['Prevalenthyp']
    BPMeds = request.GET['BP']
    cigsPerDay = request.GET['cigsPerDay']

    gender = request.GET['gender']
    diabetes = request.GET['diabetes']
    y_pred=model.predict([[sysBP,glucose,age,totchol,cigsPerDay,diaBP,prevalentHyp,diabetes,BPMeds,gender]])
    if y_pred[0]==0:
        y_pred="you have no Probability of getting a heart attack "
    else:
        y_pred="There is a probabilty of a Heart attack"
    print(age, gender, glucose,totchol, sysBP, diaBP, prevalentHyp,
           diabetes, BPMeds,cigsPerDay)

    return render(request, 'results.html',{'result':y_pred})
