from django.shortcuts import render, HttpResponse, redirect
from django.http import request
from django.contrib.auth.models import User
from django.contrib import messages, auth
from . models import profile, note
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index (request):
    return render(request, 'index.html')
def login (request):
    return render(request, 'login.html')
def signup (request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        username = request.POST.get('username').lower()
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password == cpassword:
            userExist = User.objects.filter(username = username).exists()
            emailExist = User.objects.filter(email = email).exists()
            if(userExist):
                messages.info(request, 'This user name is aleary registered.')
            elif(emailExist):
                messages.info(request, 'This email is already registered.')
            else:
                # creating new user
                newUser = User.objects.create_user(username = username, email = email, password = password, first_name = fname)
                newUser.save()
                # Creating profile
                newUserModel = User.objects.get(username = username)
                newProfile = profile(username = username, fname = fname, user = newUserModel, user_seq = newUserModel.id)
                newProfile.save()
                # loging in new user
                login_user = auth.authenticate(username = username, password = password)
                auth.login(request, login_user)
                print('moins')
                return redirect('/')
        else:
            messages.info(request, 'Password is not matching.')

    return render(request, 'signup.html')
def logout (request):
    return redirect('login')
def addnote (request):
    pass
def deletenote (request):
    return HttpResponse('Delteting the note')
def shownote (request, noteName):
    return HttpResponse('Showing the note')

def updateprofile(request):
    return HttpResponse('updating profile')

