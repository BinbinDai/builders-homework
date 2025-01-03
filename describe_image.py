#!/usr/bin/env python3

import os
import sys
import base64
import argparse
from pathlib import Path
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

def describe_image(image_path: str) -> str:
    """
    Analyze the image using GPT-4V and return a description.
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        str: Description of the image content
    """
    try:
        client = setup_openai()
        
        # Ensure the image exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")
        
        # Open and analyze the image
        with open(image_path, "rb") as image_file:
            print(f"Debug - Using OpenAI API with model: gpt-4o-mini")
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Please describe what you see in this image in detail."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=500
                )
                return response.choices[0].message.content
            except Exception as api_error:
                print(f"Debug - API Error details: {str(api_error)}", file=sys.stderr)
                if hasattr(api_error, 'response'):
                    print(f"Debug - Response status: {api_error.response.status_code}", file=sys.stderr)
                    print(f"Debug - Response headers: {api_error.response.headers}", file=sys.stderr)
                raise
    except Exception as e:
        raise Exception(f"Error in image analysis: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Describe the content of an image using GPT-4V')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    args = parser.parse_args()
    
    try:
        description = describe_image(args.image_path)
        print("\nImage Description:")
        print("-----------------")
        print(description)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 