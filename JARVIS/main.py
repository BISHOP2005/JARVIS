import speech_recognition as sr
import os
import win32com.client
import webbrowser
from playsound import playsound
import requests
import google.generativeai as genai
from config import API_KEY
import random


speaker = win32com.client.Dispatch("SAPI.SpVoice")


def speak(text):
    speaker.Speak(text)
    update_output(text)

def ai(prompt):
    text=f"A.I responce for prompt: {prompt}\n*******************************\n\n"
    genai.configure(api_key=API_KEY)
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        safety_settings=safety_settings,
        generation_config=generation_config,)

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    speak("Your Prompt is Answered and is saved in a text file in Gemini files directory")
    #print(response.text)
    #print(chat_session.history)
    text += response.text
    if not os.path.exists("Gemini files"):
        os.mkdir("Gemini files")
    with open(f"Gemini files/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)
    # with open(f"Prompt- {random.randint(1,999999)}", "w") as f:
    #     f.write(text)




def update_output(text):
    try:
        requests.post('http://127.0.0.1:5000/update', data={'new_output': text})
    except requests.exceptions.RequestException as e:
        print(f"Error updating output: {e}")


def listen_for_wake_word(wake_word="hey jarvis"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for wake word...")
        while True:
            audio = recognizer.listen(source)
            try:
                detected_text = recognizer.recognize_google(audio, language="en-UK").lower()
                print(f"Detected: {detected_text}")
                if wake_word in detected_text:
                    speak("Hello! I am your virtual assistant. I'm here to help you with a variety of tasks,"
                          "such as providing information, opening websites, playing music, and much more. "
                          "I can understand your voice commands and respond accordingly. "
                          "Just say my wake word to get started, and I'll be ready to assist you. "
                          "How can I help you today?")
                    return
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Web Speech service; {e}")
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5
        audio = r.listen(source)
        try:
            print("Recognizing....")
            query = r.recognize_google(audio, language="en-Uk")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "some error occured."
def open_websites(query):
    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
             ["google", "https://www.google.com"], ["stack", "https://www.stackoverflow.com"],
             ["github", "https://www.github.com"], ["mail", "https://www.gmail.com"],
              ["maps", "https://www.google.com/maps?authuser=0 "],
             ["drive", "https://drive.google.com/drive/u/0/home"], ["whatsapp", "https://web.whatsapp.com/"]]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            speak(f"Opening {site[0]} sir")
            return webbrowser.open(site[1])

def play_music(query):
    songs = [["ignite","C:/Users/deval/OneDrive/Desktop/SONGS/ignite.mp3"],
             ["believer","C:/Users/deval/OneDrive/Desktop/SONGS/Y2meta.app - Imagine Dragons - Believer (Lyrics) (256 kbps).mp3"],
             ["funkytown", "C:/Users/deval/OneDrive/Desktop/SONGS/funkytown.mp3"],
             ["roar","C:/Users/deval/OneDrive/Desktop/SONGS/roar.mp3"],
             ["nights","C:/Users/deval/OneDrive/Desktop/SONGS/Y2meta.app - AVICII - THE NIGHTS REMIX (320 kbps).mp3"],
             ["pasoori","C:/Users/deval/OneDrive/Desktop/SONGS/Y2meta.app - Coke Studio _ Season 14 _ Pasoori _ Ali Sethi x Shae Gill (256 kbps).mp3"],
             ["unstoppable","C:/Users/deval/OneDrive/Desktop/SONGS/Y2meta.app - Sia - Unstoppable (Official Video - Live from the Nostalgic For The Present Tour) (320 k.mp3"]
            ]
    for song in songs:
        if f"Play {song[0]} song".lower() in query.lower():
            speak(f"Playing {song[0]} song sir")
            melody = song[1]
            return playsound(melody)

def open_apps(query):
    apps = [["excel","C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk"],
            ["word", "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk"],
            ["powerpoint","C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk"],
            ["solidedge","C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Solid Edge ST5\Solid Edge ST5.lnk"],
            ["link", "https://www.linkedin.com"],
            ["visual","C:/Users/deval/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Visual Studio Code/Visual Studio Code.lnk"]
            ]
    for app in apps:
        if f"Open {app[0]}".lower() in query.lower():
            speak(f"Opening {app[0]} sir")
            return os.startfile(app[1])

def sleep(query):
    if "jarvis sleep" in query.lower():
        speak("Jarvis going to sleep mode,"
              "call the wake word to for my assistance")
        return listen_for_wake_word("hey jarvis")

def Geminiai(query):
    if "Using Artificial Intelligence".lower() in query.lower():
        ai(prompt=query)

def idiot(query):
    if "who is the dumbest person in the world".lower() in query.lower():
        speak(" prathamesh l redekar is the world's dumbest person")

def topper(query):
    if "find toppers".lower() in query.lower():
        speak("4 not 4 TOPPER NOT FOUND")

if __name__ =='__main__':
    #speaker.Speak(text)
    try:
        listen_for_wake_word("hey jarvis")
        while True:
            print("listening For Command.....")
            query = takecommand()
            if query:
                open_websites(query)
                play_music(query)
                open_apps(query)
                sleep(query)
                Geminiai(query)
                idiot(query)
                topper(query)
    except KeyboardInterrupt:
        speak("Have a nice day sir")











