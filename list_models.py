#!/usr/bin/env python3

import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
import httpx

def setup_openai():
    """Setup OpenAI client with API key from environment."""
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    try:
        # Create a custom httpx client with proxy settings
        http_client = httpx.Client(
            proxies=os.getenv('HTTPS_PROXY'),
            verify=True
        )
        
        # Create OpenAI client with the custom http client
        return OpenAI(
            api_key=api_key,
            base_url="https://api.openai.com/v1",
            http_client=http_client
        )
    except Exception as e:
        print(f"Debug - OpenAI initialization error: {str(e)}", file=sys.stderr)
        raise

def main():
    try:
        client = setup_openai()
        models = client.models.list()
        
        print("\nAvailable Models:")
        print("----------------")
        # First list vision-related models
        print("\nVision Models:")
        for model in models:
            if "vision" in model.id.lower():
                print(f"- {model.id}")
        
        # Then list GPT-4 models
        print("\nGPT-4 Models:")
        for model in models:
            if "gpt-4" in model.id.lower():
                print(f"- {model.id}")
                
        print("\nAll Other Models:")
        for model in models:
            if "gpt-4" not in model.id.lower() and "vision" not in model.id.lower():
                print(f"- {model.id}")
                
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main() 