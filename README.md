# AI Computer Assistant

A Python-based AI assistant, designed to interact with users via voice commands. It integrates with OpenAI's GPT models for conversational abilities, uses speech recognition for user input, and provides various functionalities such as Wikipedia search, weather updates, and more. It also allows the installation of Python packages via pip and provides access to a wide range of system commands.

## Features

- **Voice Interaction**: The assistant responds to voice commands and speaks back to the user.
- **AI Chat**: Powered by OpenAI's GPT-3.5/4, it can engage in conversations and respond intelligently.
- **Weather Updates**: Fetches current weather information using WeatherAPI.
- **Wikipedia Search**: Retrieves information from Wikipedia based on user queries.
- **Open Websites and Applications**: Can open websites and applications with voice commands.
- **Pip Package Installation**: Installs or uninstalls Python packages via `pip`.
- **Time Reporting**: Provides the current time when requested.
- **Rain Forecast**: Offers rain forecasts based on weather data.

## Prerequisites

Before using the AI assistant, ensure the following dependencies are installed:

- Python 3.x
- Required Python libraries (listed below)
- An API key for OpenAI and WeatherAPI

### Required Libraries

- `win32com.client` (For text-to-speech)
- `speech_recognition` (For voice recognition)
- `openai` (For GPT interaction)
- `wikipedia` (For Wikipedia search)
- `requests` (For weather data)
- `webbrowser` (For opening websites)
- `time` (For time functionality)
- `subprocess` (For opening settings and system-related tasks)
- `warnings` (For suppressing warnings)

## Setup

1. Clone the repository or download the script.
2. Install the required dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
## Add API keys as environment variables

Get your API keys from here:

- OpenAI : [Get API key](https://beta.openai.com/signup/)
- WeatherAPI : [Get API key](https://www.weatherapi.com/)

## Usage

- "Open Google website": Opens Google's website.
- "Using Wikipedia tell me about Python programming": Fetches a Wikipedia summary of Python programming.
- "What's the weather like today?": Provides the current weather report.
- "Tell me the time": States the current time.
- "Install numpy": Installs the `numpy` package.
- "Rain forecast": Provides the forecast for rain based on current weather data.
- "Exit": Exits the assistant.

## Limitations

- The weather functionality is currently limited to a fixed location (`Chandigarh`). You can modify the script to support dynamic location input.
- The assistant requires an active internet connection for Wikipedia search, weather data and API-based features.
- The assistant may not always correctly interpret speech, especially in noisy environments.
- Currently designed for Windows systems only (due to dependencies like `pywin32`).

## Contributing

Contributions are welcome! If you'd like to contribute to this project, feel free to fork the repository, make changes, and submit a pull request. Here are some ways you can contribute:

- Add more functionalities or improve existing ones.
- Help with debugging and testing.

## License

This project is open-source and available under the MIT License.

## Feedback

If you encounter any issues or have suggestions, feel free to open an issue or contact me directly.


## This `README.md` includes:

1. **Project Overview**: A short description of the project and its features.
2. **Prerequisites**: Instructions on what is needed to run the assistant.
3. **Setup**: Instructions for installing the required dependencies and setting up API keys.
4. **Usage**: How to use the assistant, including some example commands.
5. **Limitations**: Some known limitations of the assistant.
6. **Contributing**: How others can contribute to the project.
7. **License**: Information about the license (MIT in this case).


Created by Rohit Malwal. Feel free to reach out for any issues or queries.