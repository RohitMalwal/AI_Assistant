''' AI Computer Assistant '''

from win32com.client import Dispatch
import speech_recognition as sr
import os
import openai
import wikipedia
import requests
import webbrowser
import time
import subprocess
import warnings
from files import *

apikey = os.getenv('OpenaiAPI')

def say(text):
    speak = Dispatch('SAPI.SpVoice') 
    voice = speak.GetVoices()
    speak.Voice 
    speak.SetVoice(voice.Item(1))
    print(f"Jarvis: {text}")
    speak.speak(text)
    

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 0.8
        r.energy_threshold = 4000
        audio = r.listen(source)
        try:
            print('Recognizing...')
            query = r.recognize_google(audio, language="en-in")
            print(f"Rohit : {query}")
            return query
        except:
            return 'Sorry, can you repeat again.'

conversation_history = []

def chat():
    global conversation_history
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
                max_tokens=256,  # Limit the length of the response
                n=1,  # Number of responses to generate
                stop=None,  # Define stopping criteria (optional)
                temperature=0.7  # Control the creativity (0.0 = strict, 1.0 = more random)
               )
        except Exception as e:
            say(f"Error: {str(e)}")
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
        
        if not os.path.exists("D:/Python/AI Assistant/Openai"):
            os.mkdir("D:/Python/AI Assistant/Openai")
        
        with open(f"D:/Python/AI Assistant/Openai/{prompt_.split('AI')[1]}.txt", "w") as f:
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

def install():
    '''
    query: hey jarvis run this command pip install/uninstall <module>
    '''
    command = query.split('command')[1]
    try:
        say('Okay sir')
        os.system(command)
    except Exception as e:   
        say('Somthing went wrong')
        print(e)

def get_weather(location):
    # The base URL for the WeatherAPI current weather endpoint
    base_url = "http://api.weatherapi.com/v1/forecast.json"

    # Define the parameters for the API request
    params = {
        "key": os.getenv('WeatherAPI'),
        "q": location,  # Can be city name, zip code, etc.
        "days": 1, 
        "aqi": "yes",  # Air quality index (optional), 'yes' to include AQI data
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
        print('Listening...')
        query = takeCommand()
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

        elif "pip install" in query.lower() or 'pip uninstall' in query.lower():
            install() 

        elif "weather" in query.lower():
            weather_data = get_weather("chandigarh")
            if isinstance(weather_data, dict):
                # Extract relevant data from the response
                location_name = weather_data["location"]["name"]
                daytimeTemp= weather_data["current"]["temp_c"]
                nighttime_temp = weather_data["forecast"]["forecastday"][0]["day"]["mintemp_c"]
                condition = weather_data["current"]["condition"]["text"]
                chance_of_rain = weather_data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]
                aqi = weather_data["current"]["air_quality"]
                print(f"Jarvis: Location is {location_name}")
                print(f"Jarvis: Chances of rain are {chance_of_rain}%.")
                print(f"Jarvis: Air Quality Index {aqi}.")
                say(f"Should be {condition} today. Daytime temperature will hover around {daytimeTemp:.0f} degrees with overnight drop around {nighttime_temp:.0f}.")
            else:
                print(weather_data)

        elif "rain" in query.lower():
            weather_data = get_weather("chandigarh")
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

        else:
            chat()
