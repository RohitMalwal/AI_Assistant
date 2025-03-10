''' AI Computer Assistant '''

from win32com.client import Dispatch
# import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import os
import openai
import wikipedia
import requests
import webbrowser
import time
import subprocess
import warnings
import ast
from rich import print as rprint
from files import *

apikey = os.getenv('OpenaiAPI')

def say(text):
    speak = Dispatch('SAPI.SpVoice') 
    voice = speak.GetVoices()
    _ = speak.Voice 
    try:
        speak.SetVoice(voice.Item(1))
    except IndexError:
        print("Default voice being used; no alternate voice found.")
    rprint(f"[bold green]Jarvis[/bold green]: {text}")
    speak.speak(text)

def takeCommand():
    model = Model(r"D:\Vosk Voice english\vosk-model-en-us-0.22")  # Ensure the 'model' folder contains the Vosk model
    recognizer = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
    stream.start_stream()

    try:
        print('Listening...')
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                query = result.get("text", "").strip()

                if query:
                    rprint(f"[bold green]You[/bold green]: {query}")
                    return query
                else:
                    say("Sorry, I didn't catch that. Can you repeat?")
                    return None

    except OSError:
        say("No microphone detected or it's not working. Please check your microphone.")
        return None

conversation_history = []

def chat(conversation_history):
    openai.api_key = apikey
    while True:
        # Get user input
        user_input = (f"You: {query}")
        
        # Break the loop if the user types "exit"
        if "exit" in user_input.lower():
            print("Jarvis: Goodbye!")
            break

        #to clear history
        if "clear history" in user_input.lower():
            say("Okay Sir...")
            conversation_history = []
        
        # Add user message to conversation history
        conversation_history.append({"role": "user", "content": user_input})
        
        # Generate response from AI
        try:
            response = openai.completions.create(
                model="gpt-3.5-turbo",  # Or use gpt-4 if available
                prompt=conversation_history,
                max_tokens=512,  # Limit the length of the response
                n=1,  # Number of responses to generate
                stop=None,  # Define stopping criteria (optional)
                temperature=0.7  # Control the creativity (0.0 = strict, 1.0 = more random)
               )
        except Exception as e:
            error_response = str(e)
            error_dict_string = error_response.split(" - ", 1)[1]
            error_dict = ast.literal_eval(error_dict_string)
            rprint(f"[red]ERROR: {error_dict['error']['message']}[/red]")
            say("There might be a problem with your API, please recheck and try again.")
            break
        
        # Get the chatbot response
        ai_message = response['choices'][0]['message']['content']
        
        # Add AI response to conversation history
        conversation_history.append({"role": "assistant", "content": ai_message})
        
        # Print AI response
        print(f"Jarvis: {ai_message}\n")

def ai(prompt_):
    '''
    query : using ai <prompt>
    '''
    openai.api_key = apikey
    text = f"AI response for prompt: {prompt_} \n****************************************************\n\n"

    try:
        # Call the OpenAI API with a given prompt
        response = openai.completions.create(
            model="gpt-3.5-turbo",  # You can use other engines like "gpt-4" if available
            prompt=prompt_,
            max_tokens=256,  # Limit the length of the response
            n=1,  # Number of responses to generate
            stop=None,  # Define stopping criteria (optional)
            temperature=0.7  # Control the creativity (0.0 = strict, 1.0 = more random)
        )
        
        # Extract and return the generated response
        text += response.choices[0].text.strip()
        # text += response["choices"][0]["text"]
        
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        
        with open(f"Openai/{prompt_.split('AI')[1]}.txt", "w") as f:
            f.write(text)

    except Exception as e:
        say(f"Error: {str(e)}")

def usingWikipedia(query):
    '''
    query : hey jarvis using wikipedia tell me about <search>
    '''
    search = query.split('about ')[1]
    try:
        # Suppress the specific BeautifulSoup warning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            result = wikipedia.summary(search)
            say("Certainly Sir, here is your quick summary...")
            say(result)
            print(wikipedia.page(search).url)
            say("Sir, If you want to read more about it, here's the link of official page")
            time.sleep(2)
    except wikipedia.exceptions.PageError:
        say(f'Sir, Unfortunately there is no page related to {search}. Try an exact match...')
    except wikipedia.exceptions.DisambiguationError as e:
        say(f'Sir, There are multiple results for {search}. Please choose one of the following options:')
        print(e.options)

def get_weather(location):
    # The base URL for the WeatherAPI current weather endpoint
    base_url = "http://api.weatherapi.com/v1/forecast.json"

    # Define the parameters for the API request
    params = {
        "key": os.getenv('WeatherAPI'),
        "q": location,  # city name
        "days": 1, 
        "aqi": "yes", 
        "alerts": "no"  # Optional: disable alerts
    }

    # Make the API request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse and return the weather data
        data = response.json()
        return data
    else:
        return f"Error: Unable to fetch weather data (Status code: {response.status_code})"

if __name__ == '__main__':
    say(greet) #type:ignore
    while True:
        query = takeCommand()
        if query == None:
            pass
        else:
            for site in sites: #type:ignore
                if f"Open {site[0]} website".lower() in query.lower():
                    say(f"Opening {site[0]} Sir...")
                    webbrowser.open(f'{site[1]}')
            for app in apps: #type:ignore
                if f"open {app[0].lower()}" in query.lower():
                    say(f'Opening {app[0]} Sir... ')
                    os.startfile(f'{app[1]}')
            if 'Open Settings'.lower() in query.lower():
                say(f"Opening Settings Sir...")
                subprocess.run(['explorer.exe', 'ms-settings:system'])
            
            if 'time' in query.lower():
                strtime = time.strftime('%I:%M %p')   
                if strtime.startswith('0'):
                    strtime = strtime[1:]                      
                say(f"Sir, the time is {strtime}.")
            
            elif 'using AI' in query:
                say("On it, Sir...")
                ai(prompt_=query)
                say(f"Response wirtten.")

            elif 'Wikipedia'.lower() in query.lower():
                usingWikipedia(query=query)
                

            elif "exit" in query.lower():
                say('Okay Sir, exiting...')
                break

            elif "weather" in query.lower():
                weather_data = get_weather("chandigarh")
                if not isinstance(weather_data, dict):
                    # Handle the error case
                    print(f"Error: Received invalid weather data: {weather_data}")
                    say("Sorry, I couldn't fetch the weather details. Please try again later.")
                else:
                    # Extract relevant data from the response
                    try:
                        location_name = weather_data["location"]["name"]
                        daytime_temp = weather_data["current"]["temp_c"]
                        nighttime_temp = weather_data["forecast"]["forecastday"][0]["day"]["mintemp_c"]
                        condition = weather_data["current"]["condition"]["text"]
                        chance_of_rain = weather_data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]
                        aqi = weather_data["current"]["air_quality"]
                        # Print and speak the weather details
                        print(f"Jarvis: Location is {location_name}")
                        print(f"Jarvis: Chances of rain are {chance_of_rain}%.")
                        print(f"Jarvis: Air Quality Index {aqi}.")
                        say(f"Should be {condition} today. Daytime temperature will hover around {daytime_temp:.0f} degrees with an overnight drop to around {nighttime_temp:.0f}.")
                    except KeyError as e:
                        say("Sorry, I couldn't retrieve all the weather details. There might be an issue with the weather data source.")

            elif "rain" in query.lower():
                weather_data = get_weather("chandigarh")
                if isinstance(weather_data, dict):
                    try:
                        chance_of_rain = weather_data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]
                        print(f"Jarvis: Chances of rain are {chance_of_rain}%.")
                        if 0 <= chance_of_rain <= 10:
                            say(f"It doesn't look like it is going to rain today.")
                        elif 10 < chance_of_rain <= 30:
                            say("There is a slight chance it will rain today.") 
                        elif  30 < chance_of_rain <= 50:
                            say("There are good chances of rain today. You should take your umbrella with you.")
                        elif 50 < chance_of_rain <= 70:
                            say("It will probabily be rain throughout the day. You must take your umbrella with you.")
                        elif 70 < chance_of_rain <= 100:
                            say("There's a certainty of rain today. Make sure you're ready for a rainy day and bring your rain gear.")
                    except KeyError as e:
                            print(f"Error: Missing expected weather data key: {e}")
                            say("Sorry, I couldn't retrieve all the weather details. There might be an issue with the weather data source.")
                else:
                    say("Sorry, I couldn't fetch the weather details. Please try again later.")
            else:
                chat(conversation_history)
