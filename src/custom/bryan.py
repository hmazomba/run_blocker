import speech_recognition as sr
import pyttsx3
import time

# Create a recognizer object
recognizer = sr.Recognizer()

# Create a voice engine object
engine = pyttsx3.init()
voices = engine.get_voices()
engine.setProperty('voice', voices[0].id)

# Set the name of the voice assistant
name = "Bryan"

def record_audio():
    # Record the audio
    with sr.Microphone() as source:
        print("Say something...")
        audio = recognizer.listen(source)

    # Try to recognize the speech
    try:
        # Get the text from the audio
        text = recognizer.recognize_google(audio)
        print(f"Bryan: You said {text}")
    except sr.UnknownValueError:
        print("Bryan: Sorry, I didn't understand that.")
    except sr.RequestError:
        print("Bryan: Sorry, there was an error with the speech recognition service.")

def speak(text):
    # Speak the text
    engine.say(text)
    engine.runAndWait()

def start_assistant():
    # Start the assistant
    print("Bryan: Hello! How can I help you?")

    while True:
        # Record the audio
        record_audio()

        # If the user said "stop", exit the loop
        if "stop" in text:
            break

        # Do whatever the user asked
        if "play music" in text:
            speak("Playing music...")
            # Play some music
        elif "tell me a joke" in text:
            speak("Here is a joke: What do you call a fish with no eyes? Fsh!")
        else:
            speak("I don't know how to do that.")

# Start the assistant
start_assistant()