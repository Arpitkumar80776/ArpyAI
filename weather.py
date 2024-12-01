import requests
#Defining the function to run

def get_weather(city_name):
    # Your OpenWeatherMap API key
    api_key = "5d70cef5a529e93d79308fb25936d286"  # Replace with your actual API key
    base_url = "https://api.openweathermap.org/data/2.5/weather?"

    # Construct the complete URL
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"  # Using metric for Celsius

    # Send a GET request to the API
    response = requests.get(complete_url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]

        # Extracting relevant information
        temperature = main['temp']
        pressure = main['pressure']
        humidity = main['humidity']
        weather_description = weather['description']

        # Displaying the weather information
        print(f"City: {city_name}")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")
        print(f"Weather Description: {weather_description.capitalize()}")
    else:
        print("City not found or error in the request.")

# Input for city name
city_name = input("Enter city name: ")
get_weather(city_name)