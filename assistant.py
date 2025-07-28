import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import pyjokes
import os
import requests
import smtplib

# === Initialize Text to Speech engine ===
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(" Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        print(f" You said: {query}")
        return query.lower()
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I didn't catch that. Please say again.")
        return ""

def wish():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your assistant. How can I help you?")

def get_weather(city):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"The temperature in {city} is {temp}°C with {desc}."
    else:
        return "Sorry, I couldn't find weather info for that location."

def send_email(to_address, subject, body):
    try:
        from_address = "your_email@gmail.com"
        password = "your_password"
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_address, password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(from_address, to_address, message)
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I was unable to send the email.")

def get_news():
    api_key = "YOUR_NEWSAPI_KEY"
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url).json()
    articles = response.get("articles")
    if articles:
        headlines = [article['title'] for article in articles[:5]]
        return "\n".join(headlines)
    else:
        return "Sorry, I couldn't fetch the news right now."

def main():
    wish()

    while True:
        command = listen()

        if "time" in command:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}")

        elif "date" in command:
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {today}")

        elif "open youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "open whatsapp" in command:
            speak("Opening WhatsApp Web")
            webbrowser.open("https://web.whatsapp.com")

        elif "wikipedia" in command or "search wikipedia" in command or "who is" in command or "what is" in command:
            speak("What should I search on Wikipedia?")
            topic = listen()
            try:
                summary = wikipedia.summary(topic, sentences=2)
                speak("According to Wikipedia:")
                speak(summary)
            except:
                speak("Sorry, I couldn't find any information on that.")

        elif "joke" in command:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "weather" in command:
            speak("Which city?")
            city = listen()
            weather_report = get_weather(city)
            speak(weather_report)

        elif "email" in command:
            speak("Who do you want to send the email to?")
            to_addr = listen()
            speak("What is the subject?")
            subject = listen()
            speak("What should I say in the email?")
            body = listen()
            send_email(to_addr, subject, body)

        elif "news" in command:
            speak("Here are the top news headlines.")
            headlines = get_news()
            speak(headlines)

        elif "calculator" in command:
            speak("Please say the math expression like 'two plus two'")
            expr = listen()
            try:
                expr = expr.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided by", "/")
                result = eval(expr)
                speak(f"The result is {result}")
            except:
                speak("Sorry, I couldn't calculate that.")

        elif "open notepad" in command:
            speak("Opening Notepad")
            os.system("notepad.exe")

        elif "open vs code" in command or "open vscode" in command or "open visual studio code" in command:
            speak("Opening Visual Studio Code")
            os.system("code")

        elif "shutdown" in command:
            speak("Shutting down the system.")
            os.system("shutdown /s /t 1")

        elif "restart" in command:
            speak("Restarting the system.")
            os.system("shutdown /r /t 1")

        elif "stop" in command or "exit" in command or "bye" in command or "quit" in command:
            speak("Goodbye! Have a nice day.")
            break

        else:
            speak("Sorry, I don't know that command yet.")

if __name__ == "__main__":
    main()







