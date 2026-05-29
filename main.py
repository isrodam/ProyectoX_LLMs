import os
from dotenv import load_dotenv
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
    # Using llama3-8b-8192 for high-speed performance and low latency during live demos
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        groq_api_key=api_key
    )
    
    # Define a simple prompt execution to test end-to-end data pipeline connectivity
    test_prompt = "Generate a short, 1-sentence welcome message for a professional Data Engineering portfolio."
    
    print("Sending request to Groq API via LangChain...")
    
    # Invoke the model synchronously and capture the structured AI response
    response = llm.invoke(test_prompt)
    
    # Print the resulting content text delivered by the LLM
    print("\n--- LLM Response Received ---")
    print(response.content)
    print("------------------------------")

if __name__ == "__main__":
    # Execute the technical connection test pipeline
    main()