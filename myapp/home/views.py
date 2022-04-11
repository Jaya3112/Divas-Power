from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
import pyttsx3
import speech_recognition as sr
import json
import requests
import gtts
from playsound import playsound
# Create your views here.
def index(request):
    context = {
        'variable': "This is sent"}
    return render(request, 'index.html', context)
def about(request):
    return render(request, 'about.html')
def categories(request):
    return render(request, 'categories.html')
def features(request):
    return render(request, 'features.html')
def EyeMovement(request):
    return render(request, 'EyeMovement.html')
def HandGesture(request):
    return render(request, 'HandGesture.html')
def speak(str, request):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source2:

            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText= r.recognize_google(audio2)
            MyText  = MyText.lower()
            messages.success(request,MyText)

    except sr.RequestError as e:
        messages.warning(request, "Could not request results")
        tts = gtts.gTTS(
           "Could not request your results",
           lang="en")
        tts.save("hello_1.mp3")
        playsound("hello_1.mp3")

    except sr.UnknownValueError:
        messages.error(request, "Unable to hear your voice")
       # tts = gtts.gTTS(
       #    "Unable to hear you, To start again please say start",
       #     lang="en")
       #  tts.save("hello_2.mp3")
        playsound("hello_2.mp3")

    return redirect('SpeechToText')
def SpeechToText(request):
    # tts = gtts.gTTS(
     #   "Hello and welcome to our website, this is feature for visually impaired persons , You can start speaking by saying start and it will convert your voice messages into text format then say submit to submit your messages",
     #   lang="en")
    # tts.save("hello.mp3")
    # playsound("hello.mp3")
    if request.method == "POST":
        speak("", request)
    return render(request, 'SpeechToText.html')
def TextToSpeech(request):
    return render(request, 'TextToSpeech.html')
def inter(request):
    value = request.GET['input_text']
    obj = pyttsx3.init()
    obj.say(value)
    obj.runAndWait()
    return redirect('TextToSpeech')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        pload = {'email': email, 'password': password}
        newHeaders = {'Content-Type': 'application/json', 'Accept': '*/*'}
        response = requests.post("https://dca-wapp-api.herokuapp.com/api/users/login", data=json.dumps(pload),
                                 headers=newHeaders)
        jobj = response.json();
        if 'token' in jobj.keys():
            return render(request, 'categories.html')
        else:
            messages.error(request,'Incorrect Email/Password or combination')
    return render(request, 'login.html')
def SignUp(request):
    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cp = request.POST.get("cp")
        if cp != password:
            messages.warning(request,'confirm password does not match with your password')
            return render(request, 'SignUp.html')
        pload = {'username': name, 'email': email, 'password': password}
        newHeaders = {'Content-Type': 'application/json', 'Accept': '*/*'}
        response = requests.post("https://dca-wapp-api.herokuapp.com/api/users/signUp", data=json.dumps(pload),
                                 headers=newHeaders)
        jobj = response.json()
        if 'token' in jobj.keys():
            return render(request, 'login.html')
        else:
            messages.error(request, "Username/Email already used")
    return render(request, 'SignUp.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Your queries has been submitted Successfully!')
    return render(request, 'contact.html')
