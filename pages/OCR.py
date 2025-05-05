import streamlit as st
import requests
import json
import base64
from PIL import Image
import io
from decouple import config

# OpenAI API Key
api_key = config("OPENAI_API_KEY")


# Function to encode the image in base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Streamlit app
st.title("Image-to-Text Extractor with OpenAI")

# Upload image (local or URL)
upload_option = st.radio("Upload an image from:", ("Local file", "URL"))

image_data = None
if upload_option == "Local file":
    uploaded_file = st.file_uploader("Choose an image file")
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        # Convert the uploaded image to base64
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_data = base64.b64encode(image_bytes.getvalue()).decode("utf-8")

elif upload_option == "URL":
    image_url = st.text_input("Enter image URL")
    if image_url:
        st.image(image_url, caption="Image from URL", use_column_width=True)
        image_data = image_url  # URL will be sent as is

additional_instructions = st.text_area("Additional Instructions (optional)", value="")

# Make API call to OpenAI if image data is available
if image_data and st.button("Extract Text from Image"):
    if upload_option == "Local file":
        # Local file image encoded as base64
        image_payload = {"url": f"data:image/png;base64,{image_data}"}
    elif upload_option == "URL":
        # For URL-based image
        image_payload = {"url": image_data}

    # Prepare the request headers
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    # Prepare the request data (payload)
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Extract the text from the image. Additional instructions: {additional_instructions}",
                    },
                    {"type": "image_url", "image_url": image_payload},
                ],
            }
        ],
        "max_tokens": 300,
    }

    # Make the API request
    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    # Display the response
    if response.status_code == 200:
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()
        st.subheader("Extracted Text:")
        st.write(content)
    else:
        st.error(f"Failed to get a response from OpenAI: {response.status_code}")
