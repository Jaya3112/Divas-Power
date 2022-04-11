from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index,name='home'),
    path("about", views.about,name='about'),
    path("categories", views.categories,name='categories'),
    path("EyeMovement", views.EyeMovement,name='EyeMovement'),
    path("HandGesture", views.HandGesture,name='Hand Gesture'),
    path("SpeechToText", views.SpeechToText,name='SpeechToText'),
    path("TextToSpeech",views.TextToSpeech,name='TextToSpeech'),
    path("inter",views.inter,name='inter'),
    # path("Speech_Text",views.Speech_Text,name='Speech_Text'),
    path("features",views.features,name='features'),
    path("login",views.login,name='login'),
    path("SignUp", views.SignUp,name='SignUp'),
    path("contact", views.contact,name='contact'),

]