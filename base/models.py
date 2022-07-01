from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    bio = models.CharField(max_length=120, default="Hello World!")
    profile_pic = models.ImageField(default='profileicons/avatar.svg')

    class Meta:
        ordering = ['-points']
    def __str__(self):
        return str(self.user)

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Create your models here.
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    # null is True means the field is optional. blank = true is the same thing
    description = models.TextField(null=True, blank=True)
    # participants is a many to many relationship
    # the related_name is because there is already a User as host. 
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    # auto_now automatically takes timestamp when the field is updated.
    updated = models.DateTimeField(auto_now=True)
    # auto_now_add takes timestamp of when the entry is created. 
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # order if no -, the ascending, with -, it is descending
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # on_delete means, if the room is deleted, the CASCADE means this entry gets delete. This is the child of Room
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # order if no -, the ascending, with -, it is descending
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Mathhistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    subject = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    num_of_q = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    completed = models.BooleanField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.subject