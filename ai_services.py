import os
import requests
import logging
from datetime import datetime
import random

class AIService:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    def fetch_from_gemini(self, query):
        """Fetch response from Gemini AI"""
        # Check for creator/developer related questions
        creator_keywords = ["who developed you", "who's your creator", "who created you", "who made you", "your developer"]
        if any(keyword in query.lower() for keyword in creator_keywords):
            return "I'm a Large Language Model, developed with ❤️, by Arpit Kumar"

        if not self.api_key:
            logging.error("Gemini API key not found")
            return "Error: API key not configured. Please set the GEMINI_API_KEY environment variable."

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "contents": [{
                "parts":[{
                    "text": query
                }]
            }]
        }

        try:
            response = requests.post(
                f"{self.gemini_url}?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=10
            )
            
            response.raise_for_status()  # Raise an exception for bad status codes
            
            response_data = response.json()
            if not response_data.get("candidates"):
                raise ValueError("No candidates in response")
                
            return response_data["candidates"][0]["content"]["parts"][0]["text"]
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {str(e)}")
            return f"I apologize, but I'm having trouble connecting to my AI service. Error: {str(e)}"
        except (KeyError, ValueError, IndexError) as e:
            logging.error(f"Response parsing error: {str(e)}")
            return self.get_fallback_response()
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return self.get_fallback_response()
        except Exception as e:
            logging.error(f"Error calling Gemini API: {str(e)}")
            return self.get_fallback_response()

    def get_fallback_response(self):
        """Get a fallback response when AI service fails"""
        responses = [
            "I apologize, but I'm experiencing technical difficulties. Please try again later.",
            "Hmm, something went wrong. Could you rephrase your question?",
            "I'm currently unable to process your request. Please try again in a moment."
        ]
        return random.choice(responses)

    def tell_joke(self):
        """Return a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "Why did the bicycle fall over? Because it was two-tired!",
            "Why did the cookie go to the doctor? Because it was feeling crumbly!",
            "Why did the math book look sad? Because it had too many problems!",
            "Why did the computer go to the doctor? Because it had a virus!",
            "Why did the banana go to the doctor? Because it wasn't peeling well!",
            "Why did the golfer bring two pairs of pants? In case he got a hole in one!"
        ]
        return random.choice(jokes)

    def get_fact(self):
        """Return a random interesting fact"""
        facts = [
            "The Earth is the third planet from the Sun in our solar system.",
            "The average person spends about 6 months of their life waiting for red lights to turn green.",
            "The Great Wall of China is visible from space.",
            "The human brain has more neurons than stars in the Milky Way.",
            "The world's largest ocean is the Pacific Ocean.",
            "The average person's left hand does 56% of the typing.",
            "The average person walks the equivalent of five times around the world in a lifetime.",
            "A day on Venus is longer than its year."
        ]
        return random.choice(facts)
