import os
from dotenv import load_dotenv
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain_groq import ChatGroq

# # Core Pipeline Logic for Parametric Prompting
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
        "You must strictly adhere to the company's official tone of voice: {brand_tone}.\n"
        "CRITICAL REQUIREMENT: You must write the entire post strictly in the following language: {language}."
    )
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    # Formulate User prompt schemas restricting payload topic metrics and required copy lengths
    human_template = (
        "Please generate a tailored post about the following topic: '{topic}'.\n"
        "Target Platform: {platform}\n"
        "Target Audience: {audience}\n"
        "Requested Post Length: {length}\n\n"
        "Ensure the post structure, length, and hashtag strategy match the best practices "
        "of the specified platform, adhering tightly to the requested post length."
    )
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    # Assemble comprehensive prompt layers into unified LangChain message chains
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # Inject UI input arguments inside parameter placeholders
    full_prompt_inputs = {
        "brand_name": brand_name,
        "brand_industry": brand_industry,
        "brand_tone": brand_tone,
        "topic": topic,
        "platform": platform,
        "audience": audience,
        "language": language,
        "length": length
    }

    # Format localized chat strings and trigger LLM generation workflows
    formatted_prompt = chat_prompt.format_prompt(**full_prompt_inputs)
    response = llm.invoke(formatted_prompt.to_messages())
    return response.content

# # Local Execution Test Suite
def main():
    load_dotenv()
    
    # Mocking environment metadata dictionary variables
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
    
    # Invoke the operational production generator logic wrapper
    generated_post = generate_social_media_content(
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
    print("-------------------------------------------------")

if __name__ == "__main__":
    main()