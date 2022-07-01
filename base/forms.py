from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Profile
from django.contrib.auth.models import User
from django import forms


class RoomForm(ModelForm):
    class Meta:
        model = Room
        # fields = all means show all fields in the db
        fields = '__all__'
        #exclude will exclude certain fields in db from the form
        exclude = ['host', 'participants']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')
        labels = {
            'first_name':'Name',
        }

class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']
        labels = {
            'first_name':'Name',
        }

class UpdateUserBio(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
        labels = {
            'bio':'About Me', 
        }
