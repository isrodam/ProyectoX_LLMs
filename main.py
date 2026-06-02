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

# # Content Generation Core Engine Pipeline
# This function isolates the LangChain prompt engineering logic from environment orchestrators.
def generate_social_media_content(brand_name, brand_industry, brand_tone, topic, platform, audience):
    """
    Formulates structured templates and orchestrates communication with the Groq API
    to deliver tailored corporate social media copy.
    """
    # Retrieve the API key inside the function scope to handle connections securely
    import os
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("CRITICAL ERROR: GROQ_API_KEY is missing from the environment configuration.")

    # Initialize the LangChain ChatGroq model client with standard configuration
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        groq_api_key=api_key
    )

    # Construct the system message template with brand boundaries
    system_template = (
        "You are an expert copywriter and content strategist working for {brand_name}, "
        "a company operating in the following sector: {brand_industry}.\n"
        "Your sole task is to design high-converting, highly engaging social media content. \n"
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

    # Consolidate all parameters into a unified input payload for template injection
    full_prompt_inputs = {
        "brand_name": brand_name,
        "brand_industry": brand_industry,
        "brand_tone": brand_tone,
        "topic": topic,
        "platform": platform,
        "audience": audience
    }

    # Format the template with the combined payload and invoke the LLM
    formatted_prompt = chat_prompt.format_prompt(**full_prompt_inputs)
    response = llm.invoke(formatted_prompt.to_messages())

    # Return the raw generated string content to the execution coordinator
    return response.content


# # Execution Coordinator
# Main orchestrator acting as a simulated interface to test localized processing pipelines.
def main():
    # Load environment variables from the local secure .env file
    load_dotenv()

    # Define corporate brand identity context
    brand_context = {
        "brand_name": "Digital Content Marketing S.L.",
        "brand_industry": "Digital Marketing and Social Media Growth",
        "brand_tone": "Professional, engaging, authoritative yet accessible"
    }

    # Define placeholder variables simulating future frontend user inputs
    user_inputs = {
        "topic": "The importance of automated data pipelines in modern startups",
        "platform": "LinkedIn",
        "audience": "Tech Founders and Chief Technology Officers (CTOs)"
    }

    print("Formatting parametric arguments and triggering the LangChain pipeline...")

    # Execute the core function passing explicit arguments unpacked from dictionaries
    generated_post = generate_social_media_content(
        brand_name=brand_context["brand_name"],
        brand_industry=brand_context["brand_industry"],
        brand_tone=brand_context["brand_tone"],
        topic=user_inputs["topic"],
        platform=user_inputs["platform"],
        audience=user_inputs["audience"]
    )

    # Print the custom AI-generated marketing content delivered by the core pipeline
    print("\n--- Parametric LLM Content Response Received ---")
    print(generated_post)
    print("-------------------------------------------------")


if __name__ == "__main__":
    main()