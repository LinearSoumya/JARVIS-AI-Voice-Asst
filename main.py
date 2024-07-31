import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import pygetwindow as gw
import pyautogui
import shopping
import importlib  # Import the importlib module
import requests
import cv2  # Import OpenCV
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import math
import screen_brightness_control as sbc  # Import the screen-brightness-control library
import google.generativeai as palm
import logging
import os


# Reload the musicLibrary module to reflect any changes made to it
importlib.reload(musicLibrary)

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set voice to female
voices = engine.getProperty('voices')
for voice in voices:
    if 'female' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break 
    
newsapi = "694a7be1e12944f69b4fd905fa31b2c2"  # News api key
# Configure Google PaLM API
palm.configure(api_key="AIzaSyAfOGQ93NTS2YdiTi1x1oANwgF0jZ7LyOM")

# Get the audio interface for controlling the volume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def pause_video():
    try:
        youtube_window = gw.getWindowsWithTitle('YouTube')[0]  # Get the YouTube window
        youtube_window.activate()  # Activate the YouTube window
        pyautogui.press('k')  # Press 'k' to pause/resume the video
        speak("Video paused")
    except IndexError:
        speak("No YouTube window found to pause the video")

def resume_video():
    try:
        youtube_window = gw.getWindowsWithTitle('YouTube')[0]  # Get the YouTube window
        youtube_window.activate()  # Activate the YouTube window
        pyautogui.press('k')  # Press 'k' to pause/resume the video
        speak("Video resumed")
    except IndexError:
        speak("No YouTube window found to resume the video") 
           

def process_command(c):
    # For Build info
    if "what is your name" in c.lower():
        speak("My name is Jarvis an Voice Assistant AI, Build by Soumyadip Roy. Currently i'm in Beta stage")
        
    # For opening Google    
    elif "open google" in c.lower():
        webbrowser.open("https://google.com")
    # For opening LinkedIn
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/")
    # For opening YouTube    
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/") 
    # For opening Gmail
    elif "open gmail" in c.lower():
        webbrowser.open("https://mail.google.com//u/0/#inbox") 
    # For opening Facebook
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")
    # For opening Instagram
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
    
    # Playing songs from YouTube 
    elif c.lower().startswith("play"):
        # Join the words after "play" to get the full song name
        song = " ".join(c.split(" ")[1:]).strip().lower()
        print(f"Looking for song: '{song}'")  # Debugging print statement
        try:
            link = musicLibrary.Music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")
        except KeyError:
            speak(f"Sorry, I couldn't find the song {song} in the library.")
            print(f"Song '{song}' not found in the music library.")
            
    # Pause and resume YouTube video
    elif "pause" in c.lower():
        pause_video()
    elif "resume" in c.lower():
        resume_video()
            
    # Open shopping links
    elif c.lower().startswith("show me"):
        # Get the product category name from the command
        product_name = " ".join(c.split(" ")[2:]).strip().lower()
        print(f"Looking for product: '{product_name}'")  # Debugging print statement
        try:
            link = shopping.Shop[product_name]
            webbrowser.open(link)
            speak(f"Showing {product_name}")
        except KeyError:
            speak(f"Sorry, I couldn't find the product {product_name} in the shopping list.")
            print(f"Product '{product_name}' not found in the shopping dictionary.")
            
    # Open the camera
    elif "open camera" in c.lower():
        cap = cv2.VideoCapture(0)  # Start the webcam (0 is usually the default camera)
        speak("Opening camera.")
        
        while True:
            ret, frame = cap.read()  # Capture frame-by-frame
            if not ret:
                print("Failed to grab frame.")
                break
            
            cv2.imshow('Camera', frame)  # Display the resulting frame
            
            # Press 'e' to exit the camera view
            if cv2.waitKey(1) & 0xFF == ord('e'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
   
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
              
            # Extract the articles
            articles = data.get("articles", [])
              
            # Print the headlines
            for article in articles:
                speak(article["title"])
                
     # Brightness control
    elif "brightness increase" in c.lower():
        current_brightness = sbc.get_brightness()[0]  # Get current brightness
        new_brightness = min(current_brightness + 10, 100)  # Increase brightness by 10%
        sbc.set_brightness(new_brightness)
        speak("Brightness increased")

    elif "brightness decrease" in c.lower():
        current_brightness = sbc.get_brightness()[0]  # Get current brightness
        new_brightness = max(current_brightness - 10, 0)  # Decrease brightness by 10%
        sbc.set_brightness(new_brightness)
        speak("Brightness decreased")            

    # Volume control
    elif "volume up" in c.lower():
        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = min(current_volume + 0.1, 1.0)  # Increase volume by 10%
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        speak("Volume increased")

    elif "volume down" in c.lower():
        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = max(current_volume - 0.1, 0.0)  # Decrease volume by 10%
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        speak("Volume decreased")

    elif "mute" in c.lower():
        volume.SetMute(1, None)  # Mute the volume
        speak("Volume muted")

    elif "unmute" in c.lower():
        volume.SetMute(0, None)  # Unmute the volume
        speak("Volume unmuted")

    else:
        # Use Google PaLM API to answer the question
        try:
            models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
            model = models[0].name

            # Generate response using the PaLM API
            completion = palm.generate_text(
                model=model,
                prompt=c,  # Using the command as a prompt
                temperature=0.7,  # Adjust temperature for creativity
                max_output_tokens=200,  # Limit response length
            )
            # Retrieve and speak the result
            if completion.result:
                response_text = completion.result
                print("Jarvis response:", response_text)
                speak(response_text)
            else:
                speak("Sorry, I couldn't get a response from the PaLM API.")
        except Exception as e:
            speak("Sorry, an error occurred while fetching the response.")

        
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        # Use the microphone
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)

                if word.lower() == "jarvis":
                    speak("Hello Master!")
                    print("Jarvis Activated...!")

                    # Listen for the next command
                    with sr.Microphone() as source:
                        speak("How can I help you?")
                        print("Jarvis Listening...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                        command = recognizer.recognize_google(audio)
                        print(f"Command received: {command}")
                        process_command(command)

        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
