# Import packages for environment variables
import os
from dotenv import load_dotenv

# Import LangChain core prompt templates
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

# Import LangChain Groq integration
from langchain_groq import ChatGroq

# # Digital Content LLM Connection Pipeline
# This script initializes environmental variables and tests the connection to the Groq API using LangChain.

def main():
    # Load environment variables from the local secure .env file
    load_dotenv()
    
    # Retrieve the API key from the environment to ensure it is properly loaded
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("CRITICAL ERROR: GROQ_API_KEY is missing from the environment configuration.")
        
    # Initialize the LangChain ChatGroq model client with standard configuration
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        groq_api_key=api_key
    )
    
    # Define corporate brand identity context
    brand_context = {
        "brand_name": "Digital Content Marketing S.L.",
        "brand_industry": "Digital Marketing and Social Media Growth",
        "brand_tone": "Professional, engaging, authoritative yet accessible"
    }

    # Construct the system message template with brand boundaries
    system_template = (
        "You are an expert copywriter and content strategist working for {brand_name}, "
        "a company specialized in the {brand_industry} sector.\n\n"
        "Your objective is to generate high-quality, high-converting social media content. "
        "You must strictly adhere to the company's official tone of voice: {brand_tone}.\n"
        "Always respond in the language requested or default to Spanish if not specified."
    )

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    # Construct the human message template with dynamic input variables
    human_template = (
        "Please generate a tailored post about the following topic: '{topic}'.\n"
        "Target Platform: {platform}\n"
        "Target Audience: {audience}\n\n"
        "Ensure the post structure, length, and hashtag strategy match the best practices "
        "of the specified platform."
    )

    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # Combine both templates into a single chat prompt layout
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    
    # Define placeholder variables simulating future frontend user inputs
    user_inputs = {
        "topic": "The importance of automated data pipelines in modern startups",
        "platform": "LinkedIn",
        "audience": "Tech Founders and Chief Technology Officers (CTOs)"
    }

    # Merge brand identity and user selection dictionaries into a single input payload
    # This matches all placeholders defined within both system and human templates
    full_prompt_inputs = {**brand_context, **user_inputs}

    print("Formatting dynamic templates and sending data pipeline payload to Groq...")

    # Format the template with the combined dictionary payload and invoke the LLM
    formatted_prompt = chat_prompt.format_prompt(**full_prompt_inputs)
    response = llm.invoke(formatted_prompt.to_messages())

    # Print the custom AI-generated marketing content delivered by the LLM
    print("\n--- Custom LLM Content Response Received ---")
    print(response.content)
    print("--------------------------------------------")

if __name__ == "__main__":
    main()
