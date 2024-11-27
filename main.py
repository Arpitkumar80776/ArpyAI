import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import random
import webbrowser
from instabot import Bot
import requests
from gemini import Gemini
import requests
import os

api_key_gemini_com = "YOUR_GEMINI_API_KEY"  # Replace with your Gemini.com API key 
gemini_chat_url = "https://api.gemini.com/v1/chat"  # Replace with the correct chat endpoint if needed

def fetch_from_gemini(query):
    headers = {
        "Authorization": f"Bearer {api_key_gemini_com}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemini-model-name",  # Replace with the correct Gemini model name
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    }

    try:
        response = requests.post(gemini_chat_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"
        
def get_weather(city, api_key="YOUR_OPENWEATHER_API_KEY"):
    """
    Fetch the current weather for a given city using OpenWeather API.

    Args:
    - city: The name of the city to fetch the weather for.
    - api_key: Your OpenWeather API key.

    Returns:
    - A string with the current weather details or an error message.
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # Fetch temperature in Celsius
    }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            weather_desc = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            return (
                f"Weather in {city}:\n"
                f"- Condition: {weather_desc}\n"
                f"- Temperature: {temp}°C (Feels like {feels_like}°C)\n"
                f"- Humidity: {humidity}%\n"
                f"- Wind Speed: {wind_speed} m/s"
            )
        else:
            return f"Error: Unable to fetch weather data. City not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def Todo_list():
    print("Welcome to your To-Do list!")
    print("1. Add a task")
    print("2. View tasks")
    print("3. Mark a task as completed")
    print("4. Exit")
    todo_list = []
    while True:
        choice = input("Enter your choice (1-4): ")
        if choice == "1":
            task = input("Enter the task: ")
            todo_list.append({"task": task, "completed": False})
            print("Task added successfully!")
        elif choice == "2":
            if not todo_list:
                print("Your To-Do list is empty.")
            else:
                print("Your To-Do list:")
                for index, task in enumerate(todo_list, start=1):
                    status = "Completed" if task["completed"] else "Not Completed"
                    print(f"{index}. {task['task']} - {status}")
        elif choice == "3":
            if not todo_list:
                print("Your To-Do list is empty.")
            else:
                print("Your To-Do list:")
                for index, task in enumerate(todo_list, start=1):
                    print(f"{index}. {task['task']}")
                task_index = int(input("Enter the index of the task to mark as completed: ")) - 1
                if 0 <= task_index < len(todo_list):
                    todo_list[task_index]["completed"] = True
                    print("Task marked as completed!")
                else:
                    print("Invalid task index.")
        elif choice == "4":
            print("Exiting the To-Do list.")
            break
        else:
            print("Invalid choice. Please try again.")

def download_image(url, save_path="downloaded_image.jpg"):
    """
    Download an image from a URL and save it locally.

    Args:
    - url: The URL of the image.
    - save_path: The file path to save the downloaded image.

    Returns:
    - The path of the saved image or an error message if it fails.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            return save_path
        else:
            return "Failed to download the image. Check the URL."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def open_spotify():
    """Function to open Spotify in the default web browser."""
    try:
        webbrowser.open("https://open.spotify.com/")
    except Exception as e:
        return f"An error occurred: {str(e)}"

def open_cai_chat():
    """Function to open CAI Chat in the default web browser."""
    try:
        webbrowser.open("https://character.ai/")
    except Exception as e:
        return f"An error occurred: {str(e)}"
        
def upload_instagram_post(username, password, image_path, caption):
    """
    Upload an image to Instagram with a caption.

    Args:
    - username: Your Instagram username
    - password: Your Instagram password
    - image_path: The file path to the image to upload
    - caption: The caption for the Instagram post
    """
    bot = Bot()
    try:
        # Login to Instagram
        bot.login(username=username, password=password)

        # Upload the post
        bot.upload_photo(image_path, caption=caption)
        return "Post uploaded successfully!"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        bot.logout()

def tell_facts():
    """
    Tell a random fact about a specific topic.

    Args:
    - fact_type: The topic for which to tell a fact.

    Returns:
    - A string with the fact or an error message.
    """
    facts = [
        "The Earth is the third planet from the Sun in our solar system.",
        "The average person spends about 6 months of their life waiting for red lights to turn green.",
        "The Great Wall of China is visible from space.",
        "The human brain has more neurons than stars in the Milky Way.",
        "The average person's left hand does 56% of the typing.",
        "The world's largest ocean is the Pacific Ocean.",
        "The average person walks the equivalent of five times around the world in a lifetime.",
        "The human brain has more neurons than stars in the Milky Way.",
        "The average person's left hand does 56% of the typing.",
        "The world's largest ocean is the Pacific Ocean.",
        "The average person walks the equivalent of five times around the world in a lifetime.",
        "The human brain has more neurons than stars in the Milky Way.",
        "The average person's left hand does 56% of the typing.",
        "The world's largest ocean is the Pacific Ocean.",
        "The average person walks the equivalent of five times around the world in a lifetime.",
        "The human brain has more neurons than stars in the Milky Way.",
    ]

def send_email():
    """Function to send an email."""
    sender_email = input("Enter your email: ")
    sender_password = input("Enter your email password (or app password): ")
    recipient_email = input("Enter the recipient's email: ")
    subject = input("Enter the subject of the email: ")
    body = input("Enter the message: ")

    try:
        # Set up the email
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email. Error: {str(e)}"

def open_google_maps():
    """Function to open Google Maps."""
    try:
        webbrowser.open("https://www.google.com/maps/")
        return "Google Maps opened successfully!"
    except Exception as e:
        return f"Failed to open Google Maps. Error: {str(e)}"
def open_google_drive():
    """Function to open Google Drive."""
    try:
        webbrowser.open("https://drive.google.com/ ")
        return "Google Drive opened successfully!"
    except Exception as e:
        return f"Failed to open Google Drive. Error: {str(e)}"

def open_youtube():
    """Function to open Youtube."""
    try:
        webbrowser.open("https://www.youtube.com/")
        return "YouTube opened successfully!"
    except Exception as e:
        return f"Failed to open YouTube. Error: {str(e)}"

def open_facebook():
    """Function to open Facebook."""
    try:
        webbrowser.open("https://www.facebook.com/")
        return "Facebook opened successfully!"
    except Exception as e:
        return f"Failed to open Facebook. Error: {str(e)}"

def open_instagram():
    """Function to open Instagram."""
    try:
        webbrowser.open("https://www.instagram.com/")
        return "Instagram opened successfully!"
    except Exception as e:
        return f"Failed to open Instagram. Error: {str(e)}"

def open_twitter():
    """Function to open Twitter."""
    try:
        webbrowser.open("https://twitter.com/")
        return "Twitter opened successfully!"
    except Exception as e:
        return f"Failed to open Twitter. Error: {str(e)}"


def open_ytmusic():
    """Function to open YouTube Music."""
    try:
        webbrowser.open("https://music.youtube.com/")
        return "YouTube Music opened successfully!"
    except Exception as e:
        return f"Failed to open YouTube Music. Error: {str(e)}"

def open_whatsapp():
    """Function to open WhatsApp."""
    try:
        webbrowser.open("whatsapp://send")
        return "WhatsApp opened successfully!"
    except Exception as e:
        return f"Failed to open WhatsApp. Error: {str(e)}"

def open_gmail():
    """Function to open Gmail."""
    try:
        webbrowser.open("https://mail.google.com/")
        return "Gmail opened successfully!"
    except Exception as e:
        return f"Failed to open Gmail. Error: {str(e)}"

def open_amazon():
    """Function to open Amazon."""
    try:
        webbrowser.open("https://www.amazon.com/")
        return "Amazon opened successfully!"
    except Exception as e:
        return f"Failed to open Amazon. Error: {str(e)}"

def open_flipkart():
    """Function to open Flipkart."""
    try:
        webbrowser.open("https://www.flipkart.com/")
        return "Flipkart opened successfully!"
    except Exception as e:
        return f"Failed to open Flipkart. Error: {str(e)}"
def assistant():
    print("Hello! I am your assistant. Type 'help' to see what I can do.")
    while True:
        user_input = input("You: ").lower()

        if "email" in user_input:
            print("Assistant:", send_email())
        elif "open c.ai" in user_input:
            print("Assistant:", open_cai_chat())
        elif "Todo List" in user_input or "todo list" in user_input:
            print("Assistant:", Todo_list())
        elif "open amazon" in user_input:
            print("Assistant:", open_amazon()) 
        elif "tell facts" in user_input or "facts" in user_input:
            print("Assistant:", tell_facts())
        
        elif "open flipkart" in user_input:
            print("Assistant:", open_flipkart())
        elif "open youtube" in user_input:
            print("Assistant:", open_youtube())
        elif "open facebook" in user_input:
            print("Assistant:", open_facebook())
        elif "open instagram" in user_input:
            print("Assistant:", open_instagram())
        elif "open twitter" in user_input:
            print("Assistant:", open_twitter())
        elif "open whatsapp" in user_input:
            print("Assistant:", open_whatsapp())
        elif "date" in user_input:
            print("Assistant:", datetime.date.today().strftime("Today is %B %d, %Y."))
        elif "upload instagram post" in user_input:
            username = input("Enter your Instagram username: ")
            password = input("Enter your Instagram password: ")
            image_path = input("Enter the image path (e.g., /path/to/image.jpg): ")
            caption = input("Enter your caption: ")
            print("Assistant:", upload_instagram_post(username, password, image_path, caption))
        elif "open youtube music" in user_input:
            print("Assistant:", open_ytmusic()) 
        elif "time" in user_input:
            print("Assistant:", datetime.datetime.now().strftime("The time is %I:%M %p."))
        elif "joke" in user_input:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "Why did the bicycle fall over? Because it was two-tired!",
                "Why did the tomato turn red? Because it saw the salad dressing!",
                "Why did the chicken cross the playground? To get to the other slide!",
                "Why did the cookie go to the doctor? Because it was feeling crumbly!",
                "Why did the math book look sad? Because it had too many problems!",
                "Why did the computer go to the doctor? Because it had a virus!",
                "Why did the banana go to the doctor? Because it wasn't peeling well!",
                "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
                "Why did the computer go to the doctor? Because it had a virus!",
                "Why did the tomato turn red? Because it saw the salad dressing!",
                "Why did the chicken cross the playground? To get to the other slide!",
                "Why did the cookie go to the doctor? Because it was feeling crumbly!",
                "Why did the math book look sad? Because it had too many problems!",
                "Why did the computer go to the doctor? Because it had a virus!",
                "Why did the banana go to the doctor? Because it wasn't peeling well!",
                "Why did the golfer bring two pairs of pants? In case he got a hole in one!",
                "Why did the computer go to the doctor? Because it had a virus!",
                "Why did the tomato turn red? Because it saw the salad dressing!",
            ]
            print("Assistant:", random.choice(jokes))
        elif "open spotify" in user_input:
            print("Assistant:", open_spotify())
        elif "google" in user_input:
            query = input("What should I search on Google? ")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        elif "help" in user_input:
            print("Assistant: I can send an email, tell the date, time, a joke, or search on Google. Type 'exit' to quit.")
        elif "weather" in user_input:
            city = input("Enter the city name: ")
            print("Assistant:", get_weather(city))
        elif "upload instagram post" in user_input:
            username = input("Enter your Instagram username: ")
            password = input("Enter your Instagram password: ")
            image_url = input("Enter the image URL: ")
            caption = input("Enter your caption: ")

            # Download the image
            print("Downloading image...")
            local_image_path = download_image(image_url)

            if os.path.exists(local_image_path):  # Check if the image was successfully downloaded
                print("Image downloaded. Uploading to Instagram...")
                print("Assistant:", upload_instagram_post(username, password, local_image_path, caption))
            else:
                print(f"Assistant: {local_image_path}")  # Display the error message from download_image
        elif "exit" in user_input:
            print("Assistant: Goodbye! Have a great day!")
            break
        else:
            # For unsupported queries, fetch a response from Gemini AI
            print("Assistant: Let me fetch an answer for you...")
            response = fetch_from_gemini(user_input)
            print(f"Assistant: {response}")

if __name__ == "__main__":
    assistant()
