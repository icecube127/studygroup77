
from django.urls import path
from . import mathlab, views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    
    path('', views.home, name="home"), 
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    
    path('create-room/', views.createRoom, name="create-room"), 
    path('update-room/<str:pk>', views.updateRoom, name="update-room"), 
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    path('mathlab/', mathlab.quizSetup, name='mathlab-setup'),
    path('mathlab-questions/', mathlab.quizTime, name='mathlab-questions'), 
    path('mathlab-history/', mathlab.quizHistory, name='mathlab-history'), 
    path('mathlab-points/', mathlab.pointsGuide, name='mathlab-points')
]