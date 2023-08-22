import speech_recognition as sr
import os
import time
import litellm

# Set up speech recognition
r = sr.Recognizer()
with sr.Microphone() as source:
    audio = r.record(source)

# Set up the voice model
voice_model = 'slt_kevin'  # Replace with your preferred voice model
engine = 'slt'

# Set up the language model
language_model = 'en-US'

# Define a function to query the LLM API
def completion(model_name, messages):
    # Set the environment variables for the LLM API keys
    os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
    os.environ["COHERE_API_KEY"] = "your_cohere_api_key"

    # Call the LLM API
    response = litellm.completion(model_name, messages)

    return response

# Define a function to recognize speech and synthesize text
def recognize_and_speak(audio):
    try:
        # Recognize speech
        transcript = r.recognize_google(audio, language=language_model)
        
        # Query the LLM API
        response = completion('gpt-3.5-turbo', [transcript])
        
        # Synthesize text
        engine.setProperty('voice', voice_model)
        engine.say(response.choices[0].message.content)
        engine.runAndWait()
    
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")

# Define a function to handle keyboard input
def on_press(event):
    global audio
    
    if event.key == 'space':
        # Start recording
        audio = ''
        recognize_and_speak(audio)
    
    elif event.key == 'space' and audio != '':
        # Stop recording and speak
        recognize_and_speak(audio)
        audio = ''

# Set up the keyboard hook
hook = pyautogui.KeyboardHook(on_press)
hook.start()

# Run the voice assistant until stopped
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

# Clean up
hook.stop()
import speech_recognition as sr
import os
import time
import litellm

# Set up speech recognition
r = sr.Recognizer()
with sr.Microphone() as source:
    audio = r.record(source)

# Set up the voice model
voice_model = 'slt_kevin'  # Replace with your preferred voice model
engine = 'slt'

# Set up the language model
language_model = 'en-US'

# Define a function to query the LLM API
def completion(model_name, messages):
    # Set the environment variables for the LLM API keys
    os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
    os.environ["COHERE_API_KEY"] = "your_cohere_api_key"

    # Call the LLM API
    response = litellm.completion(model_name, messages)

    return response

# Define a function to recognize speech and synthesize text
def recognize_and_speak(audio):
    try:
        # Recognize speech
        transcript = r.recognize_google(audio, language=language_model)
        
        # Query the LLM API
        response = completion('gpt-3.5-turbo', [transcript])
        
        # Synthesize text
        engine.setProperty('voice', voice_model)
        engine.say(response.choices[0].message.content)
        engine.runAndWait()
    
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")

# Define a function to handle keyboard input
def on_press(event):
    global audio
    
    if event.key == 'space':
        # Start recording
        audio = ''
        recognize_and_speak(audio)
    
    elif event.key == 'space' and audio != '':
        # Stop recording and speak
        recognize_and_speak(audio)
        audio = ''

# Set up the keyboard hook
hook = pyautogui.KeyboardHook(on_press)
hook.start()

# Run the voice assistant until stopped
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break

# Clean up
hook.stop()

