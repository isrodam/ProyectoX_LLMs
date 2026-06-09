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
        "You must strictly adhere to the company's brand tone of voice: {brand_tone}.\n"
        "CRITICAL RULE: The final output MUST be written entirely and exclusively in {language}. "
        "Do not mix languages under any circumstance."
    )
    
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    # Formulate Human dynamic content specifications and explicit text lengths
    human_template = (
        "Generate a piece of social media content tailored for the following platform: {platform}.\n"
        "Target Audience: {audience}.\n"
        "Topic of the Post: {topic}.\n"
        "Desired Text Length: {length}.\n"
        "Requirements:\n"
        "1. Write compelling copy tailored to the audience's pain points and interests.\n"
        "2. Include appropriate, professional emojis to maximize visual engagement.\n"
        "3. Provide 3 to 5 highly relevant, strategic hashtags at the very end of the post."
    )
    
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # Combine both templates into a single chat prompt layout array
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Format the messages injecting the contextual parameters safely
    formatted_messages = chat_prompt.format_prompt(
        brand_name=brand_name,
        brand_industry=brand_industry,
        brand_tone=brand_tone,
        topic=topic,
        platform=platform,
        audience=audience,
        language=language,
        length=length
    ).to_messages()

    # Invoke the model synchronously and capture the structured AI response
    response = llm.invoke(formatted_messages)
    post_content = response.content.strip()

    # Trigger the downstream pipeline to extract relevant visual keywords from the generated text
    visual_keywords = extract_visual_keywords(post_content)
    
    # Query the external Pexels API using the keywords to capture a matching image asset URL
    image_url = fetch_trending_stock_image(visual_keywords)

    # Return a structured tuple containing both the copywriting text and the media resource link
    return post_content, image_url


# This function uses a low temperature LLM instance to extract clean visual keywords from a post
def extract_visual_keywords(post_content):
    """
    Analyzes the generated post content and extracts 2-3 specific English keywords
    suitable for querying a professional stock imagery API.
    """
    # Initialize a strict, low-creativity ChatGroq instance for precise data extraction
    llm_extractor = ChatGroq(
        temperature=0.0,
        model_name="llama-3.1-8b-instant"
    )
    
    # Define a strict system prompt focusing on single visual concepts to optimize external search rates
    system_template = (
        "You are a strict visual data extraction assistant.\n"
        "Your sole task is to analyze the provided text and extract 2 to 3 single, concrete nouns for image indexing.\n"
        "Rules:\n"
        "1. The keywords MUST be single words in English (e.g., 'warehouse', 'robot', 'office', 'computer', 'truck').\n"
        "2. The keywords MUST be highly visual, tangible objects representing the core business or context.\n"
        "3. Output ONLY the keywords separated by commas, with no punctuation other than commas.\n"
        "4. Do NOT include any introductory text, quotes, explanations, or compound sentences."
    )
    
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    
    # Define the human prompt placeholder to ingest the generated copywriting post
    human_template = "Extract visual keywords from the following text:\n\n{post_content}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    
    # Orchestrate the LangChain prompt layout array
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    
    # Format the prompts with the actual content received by the function
    formatted_messages = chat_prompt.format_prompt(post_content=post_content).to_messages()
    
    # Invoke the model synchronously and extract the raw string response
    response = llm_extractor.invoke(formatted_messages)
    raw_keywords = response.content.strip()
    
    # Process the comma-separated string into a clean Python list of keywords
    keyword_list = [kw.strip() for kw in raw_keywords.split(",") if kw.strip()]
    
    return keyword_list


# This function queries the Pexels API using the extracted keywords to find a relevant image URL
def fetch_trending_stock_image(keywords):
    """
    Iterates through a list of visual keywords, performs an HTTP GET request to the Pexels API,
    and extracts the direct URL of the first high-quality matching image asset.
    """
    # Retrieve the secure API credentials from the environment space
    pexels_api_key = os.getenv("PEXELS_API_KEY")
    
    # If the key is missing, log a warning and exit early to prevent pipeline crashes
    if not pexels_api_key:
        print("Warning: PEXELS_API_KEY environment variable is missing or empty.")
        return None
        
    url = "https://api.pexels.com/v1/search"
    
    # Configure secure authorization headers according to Pexels documentation guidelines
    headers = {
        "Authorization": pexels_api_key
    }
    
    # Loop through keywords to find the first valid image matching our conceptual framework
    for query in keywords:
        params = {
            "query": query,
            "per_page": 1  # We only need one precise top-matching resource
        }
        
        try:
            # Perform the synchronous HTTP request out to the external endpoint
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            # Validate that the server handshake returned an optimal success code (200 OK)
            if response.status_code == 200:
                data = response.json()
                
                # Verify that the search actually found available image objects inside the payload
                if data.get("photos") and len(data["photos"]) > 0:
                    # Drill down into the JSON dictionary architecture to capture the target media URL
                    target_image_url = data["photos"][0]["src"]["large"]
                    return target_image_url
                    
        except Exception as e:
            # Silently log network or connection faults without halting backend processing
            print(f"Network exception encountered while searching for '{query}': {e}")
            
    return None


# Orchestrate local script environment loading and runtime diagnostics execution
if __name__ == "__main__":
    load_dotenv()
    
    # Initialize global environment metadata dictionary variables
    brand_context = {
        "brand_name": "Digital Content Marketing S.L.",
        "brand_industry": "Digital Marketing and Social Media Growth",
        "brand_tone": "Professional, engaging, authoritative yet accessible"
    }
    
    # Mocking localized application interface parameter states
    user_inputs = {
        "topic": "The importance of automated data pipelines in modern startups",
        "platform": "LinkedIn",
        "audience": "Tech Founders and Chief Technology Officers (CTOs)",
        "temperature": 0.7,
        "language": "Español",
        "length": "Mediano (~150 palabras)"
    }

    print("Formatting parametric arguments and triggering the LangChain pipeline...")
    
    # Invoke the operational production generator logic wrapper (unpacking the resulting tuple)
    generated_post, image_url = generate_social_media_content(
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
    
    print("\n--- Parametric LLM Content Response Received ---")
    print(generated_post)
    print("\n--- Automated Matching Asset URL Captured ---")
    print(f"Image Link: {image_url}")
    print("-------------------------------------------------")