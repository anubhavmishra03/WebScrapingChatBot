import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=gemini_api)
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_website_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.get_text(separator="\n")
        return content.strip()
    else:
        raise Exception(f"Failed to fetch the website. Status code: {response.status_code}")
    
def process_data(raw_content):
    lines = [line.strip() for line in raw_content.split("\n") if line.strip()]
    return " ".join(lines[:50])

def chatbot_response(user_input, context_data):
    response = model.generate_content(f"You are a chatbot with the following website context:\n\n{context_data}\n\nUser: {user_input}\nChatbot:")
    return response.text

def main():
    url = "https://botpenguin.com/"
    print("Extracting website content...")
    website_data = extract_website_content(url)
    context_data = process_data(website_data)
    
    print("\nChatbot is ready! Type 'exit' to end the chat.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        response = chatbot_response(user_input, context_data)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()

