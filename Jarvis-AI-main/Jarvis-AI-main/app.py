from flask import Flask, render_template, request, jsonify
import pyttsx3
import datetime
import webbrowser
import os
import platform

app = Flask(__name__)

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id)

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

def open_calculator():
    system = platform.system()
    try:
        if system == "Windows":
            os.system('start calc')
        elif system == "Darwin":
            os.system('open -a Calculator')
        elif system == "Linux":
            os.system('gnome-calculator')
        speak("Opening Calculator")
    except:
        speak("Sorry, I couldn't open the calculator.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    query = data.get("text", "").lower()
    response = ""

    if not query:
        response = "Sorry, I did not get that. Please try again."
    elif 'exit' in query or 'stop' in query:
        response = "Goodbye Sir!"
    elif 'hello' in query or 'hey' in query:
        response = "Hello Sir, How may I help you?"
    elif 'open google' in query:
        webbrowser.open("https://google.com")
        response = "Opening Google..."
    elif 'open youtube' in query:
        webbrowser.open("https://youtube.com")
        response = "Opening YouTube..."
    elif 'open facebook' in query:
        webbrowser.open("https://facebook.com")
        response = "Opening Facebook..."
    elif 'what is' in query or 'who is' in query or 'what are' in query:
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        response = f"This is what I found regarding {query}."
    elif 'wikipedia' in query:
        topic = query.replace("wikipedia", "").strip()
        webbrowser.open(f"https://en.wikipedia.org/wiki/{topic}")
        response = f"This is what I found on Wikipedia about {topic}."
    elif 'time' in query:
        response = "The current time is " + datetime.datetime.now().strftime("%I:%M %p")
    elif 'date' in query:
        response = "Today's date is " + datetime.datetime.now().strftime("%B %d")
    elif 'calculator' in query:
        open_calculator()
        response = "Opening Calculator"
    else:
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        response = f"I found some results for {query} on Google."

    speak(response)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
