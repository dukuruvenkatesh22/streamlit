import os
import pytz
import streamlit as st
from datetime import datetime, timedelta, time as dt_time
import requests
import time
from decouple import config
import requests
import json


api_key = config("OPENAI_API_KEY")
timezones = pytz.all_timezones

st.title("Facebook Post Scheduler")


def generate_content(
    content_goal, target_audience, title, description, sections, word_length
):
    prompt = f"""
    You are a content creator specializing in social media posts. Your goal is to generate effective, engaging content.

    The context of the post is as follows:
    Goal of the Post: {content_goal}
    Target Audience: {target_audience}
    Title: {title}
    Description: {description}
    Sections: {sections}
    Word Length: {word_length}

    Your output should include:
    1. A captivating content.
    2. A clear and engaging content that aligns with the given goal and audience.
    3. Do not add any hash tags.

    Keep the language friendly and accessible, use the right tone for the target audience, and maintain brevity and impact. Ensure the post grabs attention and communicates the key message effective
    """

    # API request payload
    payload = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4095,
    }

    # API request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Send the request to the OpenAI API
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
    )

    if response.status_code == 200:
        response_json = response.json()
        content = response_json["choices"][0]["message"]["content"].strip()
        content_cleaned = content.replace("**", "")
        return content_cleaned
    else:
        print(response.json())
        return None


# Function to generate an image using OpenAI's DALL·E API
def generate_image(content_goal, target_audience, title, description):
    # Construct the prompt dynamically
    prompt = f"""
        You are a creative designer specializing in generating high-quality, visually engaging images for social media posts. Your goal is to create an image that aligns with the following post details:

        Goal of the Post: {content_goal}
        Target Audience: {target_audience}
        Title: {title}
        Description: {description}

        Your output should:
        1. It should not contain any text, labels, borders, measurements nor design elements of any kind.
        2. Visually capture the essence of the image's purpose and appeal to the target audience.
        3. Ensure the image is striking and attention-grabbing while remaining true to the context.
        4. Do not generate any hashtags.
        5. The response should in a format that is ready to be posted without any modification.
        """

    # API request payload for image generation
    payload = {
        "model": "dall-e-3",  # Model specification
        "prompt": prompt.strip(),  # Use the constructed prompt
        "n": 1,  # Number of images to generate
        "size": "1024x1024",  # Image size
    }

    # API request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Send the request to OpenAI's DALL·E API
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=payload,
    )

    # Handle the API response
    if response.status_code == 200:
        response_json = response.json()
        image_urls = [data["url"] for data in response_json["data"]]
        return image_urls  # Return all image URLs generated
    else:
        # Return error details if the request fails
        return None


def facebook_feed(scheduled_datetime, page_id, page_access_token, content):
    published = False

    # Prepare the payload
    payload = {
        "message": content["message"],
        "published": str(published).lower(),
        "scheduled_publish_time": scheduled_datetime,
    }

    # API endpoint
    url = f"https://graph.facebook.com/v21.0/{page_id}/feed"

    # Headers
    headers = {"Content-Type": "application/json"}

    # Make the POST request to the Facebook API
    response = requests.post(
        url,
        headers=headers,
        params={"access_token": page_access_token},
        data=json.dumps(payload),
    )

    response_json = response.json()

    if response.status_code == 200:
        return {"status": 200, "message": "Post scheduled successfully"}
    else:
        return {"status": 500, "message": response_json["error"]["message"]}


def facebook_photos(scheduled_datetime, page_id, page_access_token, content):
    image_response = requests.get(content["image_url"][0])

    # Save the image temporarily
    image_path = "temp_image.png"
    with open(image_path, "wb") as file:
        file.write(image_response.content)

    # Upload the image to Facebook using /photos endpoint
    photo_upload_url = f"https://graph.facebook.com/v21.0/{page_id}/photos"

    published = False

    with open(image_path, "rb") as image_file:
        files = {"source": image_file}

        # Payload with caption and access token
        payload = {
            "caption": content["message"],
            "access_token": page_access_token,
            "published": str(published).lower(),
            "scheduled_publish_time": int(scheduled_datetime),
        }

        # POST request to upload the image
        response = requests.post(photo_upload_url, files=files, data=payload)

        response_json = response.json()

        if response.status_code == 200:
            return {"status": 200, "message": "Post scheduled successfully"}
        else:
            return {"status": 500, "message": response_json["error"]["message"]}


if "page_access_token" not in st.session_state:
    st.session_state.page_access_token = ""
if "page_id" not in st.session_state:
    st.session_state.page_id = ""
if "timezone_selected" not in st.session_state:
    st.session_state.timezone_selected = "Asia/Kolkata"


page_access_token = st.text_input(
    "Facebook Page Access Token",
    type="password",
    value=st.session_state.page_access_token,
)
page_id = st.text_input("Facebook Page ID", value=st.session_state.page_id)
timezone_selected = st.selectbox(
    "Select Timezone",
    timezones,
    index=timezones.index(st.session_state.timezone_selected),
)
settings_button = st.button("Submit")

if "settings_button_clicked" in st.session_state:
    settings_button = True

if settings_button:

    if "settings_button_clicked" not in st.session_state:
        st.session_state["settings_button_clicked"] = True

    try:
        content_goal = st.text_input("Enter the goal of the post")
        target_audience = st.text_input("Enter the target audience")
        title = st.text_input("Enter the title of the post:")
        description = st.text_area("Enter a brief description of the post:")
        sections = st.text_area("Enter the section to be added in the post")
        word_length = st.number_input("Word Length", value=200)
        post_type = st.selectbox("Select post type", ["Feed", "Photos"])

        generate_button = st.button("Generate Content")

        if "generate_button_clicked" in st.session_state:
            generate_button = True

        if generate_button:

            if "generate_button_clicked" not in st.session_state:
                st.session_state["generate_button_clicked"] = True

            if "generated_content" not in st.session_state:
                with st.spinner("Generating content..."):
                    social_media_content = generate_content(
                        content_goal,
                        target_audience,
                        title,
                        description,
                        sections,
                        word_length,
                    )

                image_url_1 = ""
                if post_type == "Photos":
                    with st.spinner("Generating image..."):
                        image_url_1 = generate_image(
                            content_goal, target_audience, title, description
                        )

                st.session_state["generated_content"] = (
                    social_media_content,
                    image_url_1,
                )
            else:
                social_media_content = st.session_state["generated_content"][0]
                image_url_1 = st.session_state["generated_content"][1]

            st.subheader("Generated Social Media Content")
            st.write(social_media_content)
            if image_url_1:
                st.image(image_url_1, caption="Generated Image 1")

            schedule_button = st.button("Schedule Post")

            if "schedule_button_clicked" in st.session_state:
                schedule_button = True

            if schedule_button:

                if "schedule_button_clicked" not in st.session_state:
                    st.session_state["schedule_button_clicked"] = True

                # Specify the timezone
                pytz_timezone = pytz.timezone(timezone_selected)

                post_date = st.date_input("Schedule Date", datetime.now().date())
                post_hour = st.slider("Schedule Hour", 0, 23, datetime.now().hour)
                post_minute = st.slider("Schedule Minute", 0, 59, datetime.now().minute)

                post_button = st.button("Confirm Post")

                if "post_button_clicked" in st.session_state:
                    post_button = True

                if post_button:

                    if "post_button_clicked" not in st.session_state:
                        st.session_state["post_button_clicked"] = True

                    combined_datetime = datetime.combine(
                        post_date, dt_time(post_hour, post_minute)
                    )
                    localized_datetime = pytz_timezone.localize(combined_datetime)
                    iso_timestamp = localized_datetime.isoformat()

                    if localized_datetime > datetime.now(pytz_timezone) + timedelta(
                        minutes=10
                    ):
                        if "current_user_scheduled" not in st.session_state:
                            content = {
                                "message": social_media_content,
                                "image_url": image_url_1,
                            }

                            if post_type == "Feed":
                                posting_result = facebook_feed(
                                    iso_timestamp,
                                    page_id,
                                    page_access_token,
                                    content,
                                )
                            else:
                                posting_result = facebook_photos(
                                    localized_datetime.timestamp(),
                                    page_id,
                                    page_access_token,
                                    content,
                                )

                            st.session_state["current_user_scheduled"] = True
                    else:
                        st.error(
                            "Please choose a future date and time, at least more than 10 minutes from now."
                        )

                    if posting_result["status"] == 200:
                        st.success(f"Post scheduled for {localized_datetime}")

                        with st.spinner(
                            "Your post has been scheduled successfully. The flow will restart in a few seconds to schedule another post..."
                        ):
                            time.sleep(15)

                            st.session_state.clear()

                            if "page_access_token" not in st.session_state:
                                st.session_state.page_access_token = page_access_token
                            if "page_id" not in st.session_state:
                                st.session_state.page_id = page_id
                            if "timezone_selected" not in st.session_state:
                                st.session_state.timezone_selected = timezone_selected

                            st.experimental_rerun()
                    else:
                        st.error(f"Error: {posting_result['message']}")

                        with st.spinner(
                            "Failed to schedule the post. Please check if the Page Access Token or Page ID is correct. The flow will restart in a few seconds to schedule another post..."
                        ):
                            time.sleep(10)

                            st.session_state.clear()

                            if "page_access_token" not in st.session_state:
                                st.session_state.page_access_token = page_access_token
                            if "page_id" not in st.session_state:
                                st.session_state.page_id = page_id
                            if "timezone_selected" not in st.session_state:
                                st.session_state.timezone_selected = timezone_selected

                            st.experimental_rerun()

    except Exception as e:
        st.error(f"Error: {e}")
