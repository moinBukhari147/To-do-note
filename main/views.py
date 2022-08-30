from cgi import test
from time import time
from tkinter.messagebox import RETRY
from django.shortcuts import render, HttpResponse, redirect
from django.http import request
from django.contrib.auth.models import User
from django.contrib import messages, auth
from . models import profile, note
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
@login_required(login_url='login')
def index (request):
    now_datetime = datetime.now()
    now_time  = now_datetime.strftime('%I: %M %p')
    all_notes = note.objects.filter(user = request.user)
    user_profile = profile.objects.get(username = request.user.username)
    dp_img = str(user_profile.profile_img)[3:]
    contex = {"notes": all_notes, 'profile': user_profile, 'dp_img':dp_img, "time": now_time}
    
    return render(request, 'index.html', contex)
def login (request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password= request.POST.get('password')
        login_user = auth.authenticate(username = username, password = password)
        if login_user is not None:
            auth.login(request, login_user)
            return redirect('/')
        else:
            messages.info(request, 'The username or password is invalid.')
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
@login_required(login_url='login')
def logout (request):
    logout_user = auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def addnote (request):
    if request.method == 'POST':
        title = request.POST.get('title')
        note_content = request.POST.get('notes')
        date = request.POST.get('date')
        add_note = note(title = title,date_time = date, note_content = note_content, user= request.user)
        add_note.save() 
    return redirect('/')

@login_required(login_url='login')
def deletenote (request):
    if request.method =='GET':
        note_id = request.GET.get('note_seq')
        print(note_id)
        delete_note = note.objects.get(id = note_id)
        delete_note.delete()
    return redirect('/')

@login_required(login_url='login')
def shownote (request, noteName):
    now_datetime = datetime.now()
    now_time  = now_datetime.strftime('%I: %M %p')
    all_notes = note.objects.filter(user = request.user)
    user_profile = profile.objects.get(username = request.user.username)
    dp_img = str(user_profile.profile_img)[3:]
    note_id = request.GET.get('note_id')
    requested_note = note.objects.get(id = note_id)
    contex = {"notes": all_notes, 'profile': user_profile, 'dp_img':dp_img, "time": now_time, 'show_note': requested_note}
    
    return render(request, 'shownote.html', contex)


@login_required(login_url='login')
def updateprofile(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        profile_img = request.FILES.get('profilePic')
        update_user_profile = profile.objects.get(user = request.user)
        update_user_profile.fname = fname
        update_user_profile.lname = lname
        update_user_profile.profile_img = profile_img
        update_user_profile.save()
    return redirect('/')

def test(request):
    return render(request, "test.html")