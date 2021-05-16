from __future__ import print_function
from newsapi import NewsApiClient
import datetime
import pickle
import os.path
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import speech_recognition as sr
import pyttsx3
import pytz
import subprocess
import psutil
import pyautogui
import pyjokes
import smtplib
import wikipedia
import webbrowser as wb
from googletrans import Translator
import json
from time import sleep



SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
        r = sr.Recognizer()
        with sr.Microphone() as source:
                audio = r.listen(source)
                said = ""

                try:
                        said = r.recognize_google(audio)
                        print(said)
                except Exception as e:
                        print("Exception" + str(e))
                        speak("Please say that once more!")
                        r = sr.Recognizer()
                        with sr.Microphone() as source:
                            audio = r.listen(source)
                            said = ""
                            speak("I cannot understand what you're saying")
                      
                return said.lower()        

def username():
    speak("What should i call you?")
    username = get_audio()
    speak("Thank you for telling me your name")
    columns = shutil.get_terminal_size().columns

    print("######################".center(columns))
    print("Welcome: ", umame.center(columns))
    print("######################".center(columns))

    speak("Welcome: ")
    speak(username)

def authenticate_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(day, service):
    
    

    date  = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC 
    date = date.astimezone(utc)
    end_date= end_date.astimezone(utc)


    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        start_time = str(start.split("T")[1].split("-")[0])
        
        if int(start_time.split(":")[0]) < 12:
            start_time = start_time + "am"
        else:
            start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
            start_time = start_time + "pm"

        speak(event["summary"] + " at " + start_time)    


def get_date(text):
    text = text
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)        
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass    

    if month < today.month and month != -1:
        year = year + 1

    if day < today.day and month == -1 and day != -1:
        month = month +  1  

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)
            
    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year)    


def cpu():
    usage = str(psutil.cpu_percent())
    speak("Your device is currently running at" + usage + "percent capacity.")
    battery = psutil.sensors_battery()
    speak("Your device currently has")
    speak(battery.percent )
    speak("percent of power left.")

def screenshot():
    img = pyautogui.screenshot()
    img.save("C:\\Users\kayin\Desktop\DINO\L'Fawnda\pics.png")

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('deathgodofwind@gmail.com', 'deadpan-00')
    server.sendmail('deathgodofwind@gmail.com', to, content)
    server.close()    

def jokes():
    speak(pyjokes. get_joke())
    return pyjokes.get_joke()

def time():
    Time = datetime.datetime.now().strftime("%I:%M")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak(month)
    speak(day)
    speak(year)

def Translate():
    speak("what should I translate?")
    sentence = get_audio()
    trans = Translator()
    trans_sen = trans.translate(sentence, dist= 'en')
    print(trans_sen.text)
    speak(trans_sen.text)

def corona_news():
    newsapi = NewsApiClient(api_key = '5dbe0ade12de414ba5d6c57b51d445ac')
    data = newsapi.get_top_headlines(q = 'corona',
                                    country = 'us',
                                    language = 'en',
                                    page_size = 5)

    at = data['articles']

    sources = newsapi.get_sources()

    for x,y in enumerate(at):
        print(f'{x} {y["description"]}')
        speak(f'{x} {y["description"]}')

    speak("how else may I assist you?")    

def weather():
    url = 'api.openweathermap.org/data/2.5/weather?zip={02119},{us}&appid={your api key}'

    res = requests.get(url)

    data = res.json()

    weather = data['weather'] [0] ['main']
    temp = data['main']['temp']
    wind_speed = data['wind']['speed']

    latitude = data['coord']['lat']
    longitude = data['coord']['lon']

    description = data['weather'][0]['description']
    speak('Temperature : {} degree celcius'.format(temp))
    print('Wind Speed : {} m/s'.format(wind_speed))
    print('Latitude : {}'.format(latitude))
    print('Longitude : {}'.format(longitude))
    print('Description : {}'.format(description))
    print('weather is: {} '.format(weather))
    speak('weather is : {} '.format(weather))

def conversation():
    response1 = speak("I am well")
    response2 = speak("I'm okay I guess...")
    response3 = speak("Not very well... I believe a charging is in order.")
    response4 = speak("Thanks for asking!")
    response5 = speak("I am currently in critical condition... please provide assistance")
   
    battery = psutil.sensors_battery()
    

    if battery.percent >= 60 and battery.percent <101:
        speak('response1' + 'response4')
    elif battery.percent >= 25 and battery.percent < 60:
        speak(response2 + response4)
    elif battery.percent >= 5 and battery.percent < 25:
        speak(response4)
    elif battery.percent >= 0 and battery.percent < 5:
        speak(response5)

def your_name():
    speak("What would you like to call me")
    assname = get_audio()
    speak("Thanks for naming me")

def my_name(): 
    text = text.replace("change my name to", "")
    assname = text     

def wishme():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour <12:
        speak("Good Morning")
    elif hour >= 12 and hour <18:
        speak("Good Afternoon")
    elif hour >= 18 and hour <24:
        speak("Good Evening")
    else:
        speak("It is late, it is early")
    speak("Hello... I am your personal M.E. or Matrix Entity. But you may call me: INSERT NAME HERE... How may I be of assistance.")    

WAKE = "are you ready?"
SLEEP ="goodbye"
CONFIRM = "yes"
DENY = "no"
SERVICE = authenticate_google()
wishme()


while True:
    print("listening")
    text = get_audio()

    if text.count(WAKE) > 0:
        speak("i am ready")
        text = get_audio()

    elif text.count(SLEEP) > 0:
        speak("is that all?")
        r = sr.Recognizer()
        with sr.Microphone() as source:
                audio = r.listen(source)
                said = CONFIRM
                speak("It was a pleasure to assist you.")
                quit()      
                          
    CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]
    for phrase in CALENDAR_STRS:
        if phrase in text:
            date = get_date(text)
            if date:
                    get_events(date, SERVICE)
            else:
                speak("i don't understand")       

    NOTE_STRS = ["make a note","write this down", "remember this"]
    for phrase in NOTE_STRS:
        if phrase in text:
            speak("What would you like me to write down?")
            note_text = get_audio()
            speak("so you said to remember" + note_text)
            remember = open('Notes.txt', 'w')
            remember.write(note_text)
            remember.close()

    REMIND_STRS = ["remind me", "what did i just tell you to note"]
    for phrase in REMIND_STRS:
        if phrase in text:
            remember = open('Notes.txt', 'r')
            speak("you just told me to note that" + remember.read())        

    CPU_STRS = ["status report", "diagnostics"]
    for phrase in CPU_STRS:
        if phrase in text:
            speak("Running diagnostics...")
            cpu()
    
    MUSIC_STRS = ["play music", "play my jams", "play my shit", "what music do I have"]
    for phrase in MUSIC_STRS:
       if phrase in text:
           speak("let's see what we've got")
           songs_dir = "C:\\Users\kayin\Music" 
           songs = os.listdir(songs_dir)
           speak("oooo looks tasty from here!")
           os.startfile(os.path.join(songs_dir, songs[1]))

    TIME_STR = ["what time is it", "what's the time"]
    for phrase in TIME_STR:
        if phrase in text:
            speak("The time is")
            time()

    DATE_STR = ["what day is it", "what's today"]
    for phrase in DATE_STR:
        if phrase in text:
            speak("Today's date is")
            date()

    WIKI_STR = ["wiki search", "search wikipedia for"] 
    for phrase in WIKI_STR:
        if phrase in text:
            speak("searching...")
            wiki_text = get_audio()
            wiki_text = wiki_text.replace("Wikipedia","")
            result = wikipedia.summary(wiki_text, sentences=2)
            print(result)
            speak(result)
            
    EMAIL_STR = ["send a letter"]
    for phrase in EMAIL_STR:
        if phrase in text:
            try:
                speak("What would you like me to say?")
                content = get_audio()
                to = input()
                sendEmail(to, content)
                speak(content)

            except Exception as e:
                print(e)
                speak("Message was not sent")    

    WEB_STR = ["search the web for", "google search", "check the internet for"]
    for phrase in WEB_STR:
        if phrase in text:
            speak("searching...")
            chromepath = 'C://Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            search = get_audio()
            wb.get(chromepath).open_new_tab(search +'.com')


    LOGOUT_STR = ["log out", "chill out"]
    for phrase in LOGOUT_STR:
        if phrase in text:
            os.system("shutdown -l")

    SHUTDOWN_STR = ["shut down", "lights out", "goodnight"]
    for phrase in SHUTDOWN_STR:
        if phrase in text:
            os.system("shutdown /s /t 1")

    RESTART_STR = ["restart", "reset", "redo","mulligan"]
    for phrase in RESTART_STR:
        if phrase in text:
            os.system("shutdown /r /t 1")

    SCNSHR_STR = ["screenshot this", "shoot the screen", "take a picture"]
    for phrase in SCNSHR_STR:
        if phrase in text:
            screenshot()
            speak("Screenshot Taken")

    JOKE_STRS = ["be funny", "tell me a joke", "clown"]
    for phrase in JOKE_STRS:
        if phrase in text:
            speak("Ha ha ha, you must think I'm some sort of clown")
            jokes()        

    TRANSLATE_STRS = ["translate"]
    for phrase in TRANSLATE_STRS:
        if phrase in text:
            speak("Good thing I am a polyglot")
            Translate()        

    CORONA_NEWS_STRS = ["corona"]
    for phrase in CORONA_NEWS_STRS:
        if phrase in text:
             speak("I have the latest news on the Covid-19 Pandemic...")
             corona_news()

    WEATHER_STRS = ["what's the weather", "tell me the weather"]
    for phrase in WEATHER_STRS:
        if phrase in text:
            speak("Here's your weather update.")
            weather()         

    CONVERSATION_STRS = ["how are you"]
    for phrase in CONVERSATION_STRS:
        if phrase in text:
            conversation()

    CHANGING_STRS = ["name change", "your new name"]
    for phrase in CHANGING_STRS:
        if phrase in text:
            your_name()

    NAMECHANGE_STRS = ["change my name", "my new name"]
    for phrase in NAMECHANGE_STRS:
        if phrase in text:
            my_name()

    

                            
