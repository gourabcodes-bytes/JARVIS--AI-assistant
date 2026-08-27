import speech_recognition as sr
import pyttsx3 
import webbrowser
import musicLibrary
import requests
import wikipedia

import pygame
import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6KcdeeuY7MqDe4I2tT4Fibglawngsm_46n-XVMKtj30nw")

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_ai(question):
    try:
        response = model.generate_content(question)
        print(response.text)
        speak(response.text)
    except Exception as e:
        print("Gemini Error:", e)

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        print(result)
        speak(result)
    except:
        speak("Sorry, I couldn't find that.")
    
    

from ddgs import DDGS

def search_web(query):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))

    if results:
        answer = results[0]["body"]
        print(answer)
        speak(answer)
    else:
        speak("Sorry, I couldn't find anything.")

engine = pyttsx3.init()
pygame.mixer.init()
newsapi="fc59b1d2864f43feb2a07c4da0b21427"


def speak(text):
    engine.say(text)
    engine.runAndWait()


    



    # Keep the program running until the song finishes


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open chatgpt" in c.lower():
        webbrowser.open("https://chatgpt.com")

    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musicLibrary.music[song]
        webbrowser.open(link)
    elif c.lower().startswith("search"):
        query = c[7:].strip()   # Remove the word "search"
        print(f"Searching for: {query}")
        speak(f"Searching for {query}")
        search_web(query)
    elif c.lower().startswith("who is"):
        query = c.replace("who is", " ")
        search_wikipedia(query)

    elif c.lower().startswith("what is"):
        query = c.replace("what is", " ")
        search_wikipedia(query)
    elif c.lower().startswith("ask"):
        question = c[4:]
        ask_ai(question)
    elif c.lower().startswith("search"):
        query = c.replace("search", "")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "news" in c.lower():
       response = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey={newsapi}"
    )

    data = response.json()

    print(data)

    if data["status"] == "ok":
        for article in data["articles"][:5]:
            print(article["title"])
            speak(article["title"])



    
        
        



    
    
    pass    

if __name__ == "__main__":
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8


    speak("Initializing Jarvis.....")
    with sr.Microphone() as source:
        print("Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=2)
    import time


    while True:
        try:
            with sr.Microphone() as source:

                print("Listening...")
                audio = r.listen(source,timeout=5,phrase_time_limit=3)

            print("Recognizing...")
            word = r.recognize_google(audio)
            

            print("Recognized:", word)

            import time

            if "jarvis" in word.lower():
                print("Wake word detected")
                speak("Yes")
                time.sleep(0.5)

                print("Listening for command... ")

                #listen for command
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    print("Jarvis active....")
                    audio = r.listen(source,timeout=5)


                command = r.recognize_google(audio)

                processCommand(command)

            
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")

        except sr.RequestError as e:
            print(f"Google API error: {e}")

        except Exception as e:
            print(e)

