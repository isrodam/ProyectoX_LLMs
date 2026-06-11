import os
import requests
from dotenv import load_dotenv
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_groq import ChatGroq

# Core Pipeline Logic for Parametric Prompting
def generate_social_media_content(brand_name, brand_industry, brand_tone, topic, platform, audience, temperature, language, length):
    """
    Formulates structured templates and orchestrates communication with the Groq API
    to deliver tailored corporate social media copy incorporating advanced parameters.
    """
    # Verify environment key validation before model instantiation
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("CRITICAL ERROR: GROQ_API_KEY is missing from the environment configuration.")

    # Initialize ChatGroq client mapping explicit temperature controls from backend args
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=temperature,
        groq_api_key=api_key
    )

    # Formulate System instructions bounding professional identities and mandatory output languages
    system_template = (
        "You are an expert copywriter and content strategist working for {brand_name}, "
        "a company operating in the following sector: {brand_industry}.\n"
        "Your sole task is to design high-converting, highly engaging social media content. \n"
        "You must strictly adhere to the company's brand voice guidelines:\n"
        "{brand_tone}\n\n"
        "Operational Rules:\n"
        "1. Write the content exclusively for the following social platform: {platform}.\n"
        "2. Tailor the message vocabulary, hooks, and call-to-actions specifically for this audience: {audience}.\n"
        "3. You must write the entire output strictly in this language: {language}.\n"
        "4. Enforce this text length constraint: {length}.\n"
        "5. Include highly relevant hashtags at the bottom to maximize organic reach."
    )

    # Formulate Human execution prompt injecting user workspace goals
    human_template = "Generate a post about the following topic: {topic}"

    # Build the combined multi-message conversational prompt template architecture
    chat_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ])

    # Compile variables and format the dynamic chat prompt pipeline input
    formatted_messages = chat_prompt.format_messages(
        brand_name=brand_name,
        brand_industry=brand_industry,
        brand_tone=brand_tone,
        platform=platform,
        audience=audience,
        language=language,
        length=length,
        topic=topic
    )

    # Execute downstream prediction call via ChatGroq interface wrapper
    response = llm.invoke(formatted_messages)
    generated_post = response.content

    # Extract single concrete nouns in English from the generated post text
    keywords = extract_visual_keywords(generated_post)

    # Query third-party multimedia API providers using the optimized keywords
    image_url, photographer = fetch_trending_stock_image(keywords)

    return generated_post, image_url, keywords, photographer


def extract_visual_keywords(post_content):
    """
    Analyzes generated copy to isolate 2 to 3 single concrete nouns in English
    optimized for image asset indexing search loops.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "technology, office"

    # Enforce strict deterministic extraction output via zero temperature parameterization
    extractor_llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.0,
        groq_api_key=api_key
    )

    system_template = (
        "You are a strict data extraction engine.\n"
        "Analyze the provided text and isolate exactly 2 to 3 single, concrete nouns in English "
        "that represent physical objects or business assets (e.g., 'computer', 'server', 'warehouse', 'robot', 'office').\n"
        "Operational Constraints:\n"
        "1. Return ONLY the words separated by a single comma (e.g., 'computer,office').\n"
        "2. Do NOT include explanations, quotes, introduction text, punctuation, or spaces around commas."
    )

    human_template = "Extract visual indexing tags from this text structure:\n\n{post_content}"

    chat_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_template)
    ])

    formatted_messages = chat_prompt.format_messages(post_content=post_content)
    response = extractor_llm.invoke(formatted_messages)
    
    return response.content.strip()


def fetch_trending_stock_image(keywords):
    """
    Executes an authenticated HTTP GET request against the Pexels Image API
    to isolate a single relevant media asset matching the parameter keywords.
    """
    pexels_key = os.getenv("PEXELS_API_KEY")
    if not pexels_key:
        print("WARNING: PEXELS_API_KEY is missing. Skipping asset discovery pipeline loops.")
        return None, "Anónimo"

    url = f"https://api.pexels.com/v1/search?query={keywords}&per_page=1"
    headers = {"Authorization": pexels_key}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("photos") and len(data["photos"]) > 0:
                image_url = data["photos"][0]["src"]["large"]
                photographer = data["photos"][0].get("photographer", "Anónimo")
                return image_url, photographer
        else:
            print(f"Pexels HTTP API Error: Received response status state {response.status_code}")
    except Exception as e:
        print(f"CRITICAL: Failed to execute automated media fetching process: {str(e)}")

    return None, "Anónimo"


if __name__ == "__main__":
    load_dotenv()
    print("Running backend standalone data pipeline query validations...")
    
    brand_context = {
        "brand_name": "Digital Content Marketing S.L.",
        "brand_industry": "Digital Marketing and Social Media Growth",
        "brand_tone": "Professional, engaging, authoritative yet accessible"
    }
    
    user_inputs = {
        "topic": "The importance of automated data pipelines in modern startups",
        "platform": "LinkedIn",
        "audience": "Tech Founders and Chief Technology Officers (CTOs)",
        "temperature": 0.7,
        "language": "Español",
        "length": "Mediano (~150 palabras)"
    }

    generated_post, image_url, keywords, photographer = generate_social_media_content(
        brand_name=brand_context["brand_name"],
        brand_industry=brand_context["brand_industry"],
        brand_tone=brand_context["brand_tone"],
        topic=user_inputs["topic"],
        platform=user_inputs["platform"],
        audience=user_inputs["audience"],
        temperature=user_inputs["temperature"],
        language=user_inputs["language"],
        length=user_inputs["length"]
    )
    
    print("\n--- Content Response Received ---")
    print(generated_post)
    print(f"\nKeywords Extracted: {keywords}")
    print(f"Image Link: {image_url}")
    print(f"Photographer: {photographer}")