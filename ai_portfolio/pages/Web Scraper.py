import streamlit as st
import requests
import io
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from PIL import Image
from decouple import config
import time
import base64

# Load OpenAI API key from environment variables
openai_api_key = config("OPENAI_API_KEY")


# Function to take a screenshot of a website
def take_screenshots_base64(website_url):
    # Automatically download and manage ChromeDriver using webdriver_manager
    chrome_service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver with Chrome and the installed service
    driver = webdriver.Chrome(service=chrome_service, options=options)

    # Open the website
    driver.get(website_url)

    # Get the total page height
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Define the viewport height (window size)
    viewport_height = driver.execute_script("return window.innerHeight")

    # Initialize the list to store Base64-encoded screenshots
    base64_screenshots = []

    # Start scrolling and take screenshots at each scroll step
    current_position = 0
    while current_position < total_height:
        # Scroll to the current position
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(1)  # Wait for the page to load

        # Take a screenshot and store it as a base64 string
        screenshot = driver.get_screenshot_as_png()

        # Convert the screenshot to Base64
        buffered = io.BytesIO(screenshot)
        base64_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
        base64_screenshots.append(base64_string)

        # Move to the next position
        current_position += viewport_height

        # Recalculate total height in case more content is loaded dynamically
        total_height = driver.execute_script("return document.body.scrollHeight")

    # Quit the driver after taking all screenshots
    driver.quit()

    return base64_screenshots


# Function to send extracted content to OpenAI GPT-4
def extract_content_from_image(image):
    api_url = "https://api.openai.com/v1/chat/completions"

    # Set up the request payload and headers
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extract the contents from the image and format it properly. Dont include any additional content in the response",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image}",
                            "detail": "high",
                        },
                    },
                ],
            }
        ],
        "max_tokens": 500,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    }

    # Send the request to OpenAI API
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    else:
        return response.json()


# Streamlit app layout
st.title("AI Website Scraper with Content Extraction")

# Input for website URL
website_url = st.text_input(
    "Enter the URL of the website you want to scrape:", "https://quotes.toscrape.com/"
)

if st.button("Scrape and Extract Content"):
    if website_url:
        st.write(f"Taking screenshot and extracting content for '{website_url}'...")

        # Take screenshot of the website
        screenshot_images = take_screenshots_base64(website_url)

        st.subheader("Extracted Content Summary:")

        for image in screenshot_images:
            extracted_content = extract_content_from_image(image)
            st.write(extracted_content)
