import streamlit as st
import requests
from bs4 import BeautifulSoup
from decouple import config

# Load OpenAI API key from environment variables
openai_api_key = config("OPENAI_API_KEY")


# Function to retrieve and parse HTML source code from a given website
def get_source_code(website_url):
    response = requests.get(website_url)
    if response.status_code != 200:
        return None, "Failed to retrieve the website's source code."

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # Extract title tag
    title_tag = soup.title.string if soup.title else "No title tag found"

    # Extract meta description
    meta_description = soup.find("meta", {"name": "description"})
    meta_description = (
        meta_description["content"] if meta_description else "No meta description found"
    )

    # Extract header tags (H1, H2, H3, etc.)
    header_tags = [
        tag.text for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    ]

    # Extract internal and external links
    internal_links = [
        link.get("href")
        for link in soup.find_all("a", href=True)
        if website_url in link.get("href")
    ]
    external_links = [
        link.get("href")
        for link in soup.find_all("a", href=True)
        if website_url not in link.get("href")
    ]

    # Extract text content for keyword analysis
    text_content = soup.get_text()

    return {
        "title_tag": title_tag,
        "meta_description": meta_description,
        "header_tags": header_tags,
        "internal_links": internal_links,
        "external_links": external_links,
        "text_content": text_content,
    }, None


# Function to provide basic SEO suggestions
def provide_seo_suggestions(website_data):
    suggestions = []

    # Title tag optimization suggestion
    if website_data["title_tag"] == "No title tag found":
        suggestions.append(
            "The webpage is missing a title tag. Add a descriptive title tag including target keywords."
        )

    # Meta description optimization suggestion
    if website_data["meta_description"] == "No meta description found":
        suggestions.append(
            "The webpage is missing a meta description. Add a relevant meta description with target keywords."
        )

    # Header tags suggestion
    if not website_data["header_tags"]:
        suggestions.append(
            "No header tags (H1, H2, etc.) found. Use header tags to structure the content."
        )

    # Link structure suggestion
    if not website_data["internal_links"]:
        suggestions.append(
            "No internal links found. Add internal links to improve SEO and user navigation."
        )

    # Content suggestion
    if len(website_data["text_content"].split()) < 100:
        suggestions.append(
            "The page content seems too short. Consider adding more high-quality, keyword-rich content."
        )

    return suggestions


# Function to summarize the text content using OpenAI
def summarize_content(text_content):
    api_url = "https://api.openai.com/v1/chat/completions"

    # Prepare the prompt for the API
    prompt = f"""
    Summarize the following website content:\n\n{text_content}\n\nSummary:
    """

    # Set up the request payload and headers
    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
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
        return "Failed to summarize the content."


# Streamlit app layout
st.title("Basic SEO Analyzer with Content Summary")

# Input for website URL
website_url = st.text_input(
    "Enter the URL of the website you want to analyze:", "https://quotes.toscrape.com/"
)

if st.button("Analyze SEO"):
    if website_url:
        st.write(f"Analyzing SEO for '{website_url}'...")

        # Fetch website source code and SEO data
        website_data, error = get_source_code(website_url)
        if error:
            st.error(error)
        else:
            # Display the extracted data
            st.subheader("Extracted SEO Data:")
            st.write(f"**Title Tag:** {website_data['title_tag']}")
            st.write(f"**Meta Description:** {website_data['meta_description']}")
            st.write(
                f"**Header Tags:** {', '.join(website_data['header_tags']) if website_data['header_tags'] else 'None'}"
            )
            st.write(f"**Internal Links:** {len(website_data['internal_links'])} found")
            st.write(f"**External Links:** {len(website_data['external_links'])} found")

            # Provide basic SEO suggestions
            st.subheader("SEO Suggestions:")
            suggestions = provide_seo_suggestions(website_data)
            if suggestions:
                for i, suggestion in enumerate(suggestions, 1):
                    st.write(f"{i}. {suggestion}")
            else:
                st.write("The SEO looks good! No major issues found.")

            # Summarize the website content using OpenAI
            st.subheader("Content Summary:")
            summary = summarize_content(website_data["text_content"])
            st.write(summary)
