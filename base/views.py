from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, Profile
from .forms import RoomForm, UpdateUserForm, SignUpForm, UpdateUserBio
import random

def randomProfilePic():
    file_path = 'profileicons/'
    file_extension = '.png'
    file_name = random.randint(1, 9)

    file = file_path + str(file_name) + file_extension
    return file

# Create your views here.

def loginPage(request):

    page = 'login'

    # send user to home if already logged in
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # .lower() makes the username all lower case. 
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            #messages.error(request, 'User does not exist.')
            error_msg = 'User does not exist.'
            context = {'page': page, 'error':error_msg}
            return render(request, 'base/login_register.html', context)
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_msg = 'Password incorrect.'
            context = {'page': page, 'error':error_msg}
            return render(request, 'base/login_register.html', context)

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

###### REGISTERATION #######
def registerPage(request):
    page = 'register'
    form = SignUpForm()
    context = {'form':form}

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # commit=False means that the current data is accessible without it being committed to db. 
            # this is one way to add entry to db. 
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            new_profile = Profile.objects.create(user=user)
            #random_profile_pic = randomProfilePic()
            #print(random_profile_pic)           
            #new_profile.profile_pic = random_profile_pic
            return redirect('home')
        else:
            error_msg = form.errors
            context = {'form':form, 'page': page, 'error':error_msg}
            return render(request, 'base/login_register.html', context)

    return render(request, 'base/login_register.html', context)

###### UPDATE USER PROFILE #######
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    form1 = UpdateUserForm(instance=user)
    form2 = UpdateUserBio(instance=profile)
    context = {'form1':form1, 'form2':form2}
    
    if request.method == 'POST':
        form1 = UpdateUserForm(request.POST, instance=user)
        form2 = UpdateUserBio(request.POST, request.FILES, instance=profile)
        if form1.is_valid() and form2.is_valid():
            if user.username == 'admin':
                profile.profile_pic = 'profileicons/cap.png'
            else:
                if profile.profile_pic == 'profileicons/avatar.svg':
                    random_profile_pic = randomProfilePic()
                    profile.profile_pic = random_profile_pic
            form1.save()
            form2.save()
            return redirect('user-profile', pk=user.id)
        else:
            error_msg1 = form1.errors
            error_msg2 = form2.errors
            context = {'form1':form1, 'form2':form2, 'error1':error_msg1, 'error2':error_msg2}
            return render(request, 'base/login_register.html', context)
            
    return render(request, 'base/update-user.html', context)

###### UPDATE USER PROFILE PICTURE #######
@login_required(login_url='login')
def updateProfilePic(request):
    user = request.user
    #profile = Profile.objects.get(user=user)
    icon_path = "/static/images/profileicons/"
    extension = ".png"
    #icons = ['profileicons/1.png', 'profileicons/2.png', 'profileicons/3.png',]
    icons_row1 = ['1', '2', '3', '4']
    icons_row2 = ['5', '6', '7', '8']
    icons_row3 = ['cap', 'ironman', 'thor', 'bp']
    context = {'icons1':icons_row1, 'icons2':icons_row2, 'icons3':icons_row3, 'path':icon_path, 'extension':extension}
    
    return render(request, 'base/update_profilepic.html', context)

@login_required(login_url='login')
def updatePic(request, img):
    user = request.user
    profile = Profile.objects.get(user=user)

    icon_path = "profileicons/"
    extension = ".png"
    path = icon_path + img + extension
    profile.profile_pic = path
    profile.save()
    return render(request, 'base/profile.html')

def home(request):
    # statement below gets what's in q value from home.html. Set it to blank if no value
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    # this searchs in Room table for topic_name that contains what's in q. 
    # if ?q=Ma, it'll find Math
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    # query can go up multiple levels with underscore __ 
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    # THIS part gets the People + Points
    profiles = Profile.objects.all()

    context = {'roomsinfo':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages, 'profiles':profiles}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    # get all message related to this instance of room.  The db class is Message but you write message_set.all(). Lower case and underscore _set.all()
    # the order_by('-created') is to sort the result by "created" in descending order. ascending is without dash
    room_messages = room.message_set.all().order_by('-created')

    participants = room.participants.all()

    if request.method=='POST':
        # class.objects.create(parameters) is another way to create new entry to db. 
        new_message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        # this adds the user to the participants list
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    my_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user':user, 'roomsinfo':rooms, 'room_messages':my_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        # the get_or_create method will either get the object or create if it doesn't exist. 
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        
        # run below print for debug purpose
        #print(request.POST)
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        return redirect('home')

    context = {'form': form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
        
    # this checks to see if you are the host of the room. If not, you cannot update/delete it.
    if request.user != room.host:
        return HttpResponse('You are not allowed to update the room.')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        # the get_or_create method will either get the object or create if it doesn't exist. 
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('home')

    context = {'form': form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # this checks to see if you are the host of the room. If not, you cannot update/delete it.
    if request.user != room.host:
        return HttpResponse('You are not allowed to update the room.')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    thisMessage = Message.objects.get(id=pk)

    # this checks to see if you are the host of the room. If not, you cannot update/delete it.
    if request.user != thisMessage.user:
        return HttpResponse('You are not allowed to delete the message.')
    
    if request.method == 'POST':
        thisMessage.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':thisMessage})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)

    context = {'topics':topics}
    return render(request, 'base/topics.html', context)

def activityPage(request):
    #q = request.GET.get('q') if request.GET.get('q') != None else ''
    #topics = Topic.objects.filter(name__icontains=q)
    room_message = Message.objects.all()

    context = {'room_messages':room_message}
    return render(request, 'base/activity.html', context)