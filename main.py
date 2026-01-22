import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 1. Load your secret API keys from the .env file
load_dotenv() 

def test_setup():
    print("--- GenAI Environment Test ---")
    # This check ensures you aren't running as 'root' by accident
    print(f"Working Directory: {os.getcwd()}")
    
    # We won't call the API yet (to save you money/credits), 
    # but we check if the library is ready.
    try:
        model = ChatOpenAI(model="gpt-3.5-turbo")
        print("LangChain & OpenAI libraries: READY ✅")
    except Exception as e:
        print(f"Setup Issue: {e}")

if __name__ == "__main__":
    test_setup()