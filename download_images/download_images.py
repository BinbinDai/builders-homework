import os
import requests
import hashlib
from urllib.parse import urlparse

def get_unique_urls(file_path):
    with open(file_path, 'r') as f:
        urls = f.read().splitlines()
    return list(dict.fromkeys(urls))  # Remove duplicates while preserving order

def download_image(url, save_dir):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Create a filename from the URL's path and a hash of the full URL
            parsed_url = urlparse(url)
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            base_name = os.path.basename(parsed_url.path)
            name, ext = os.path.splitext(base_name)
            if not ext:
                ext = '.jpg'  # Default to .jpg if no extension
            filename = f"{url_hash}{ext}"
            
            file_path = os.path.join(save_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Successfully downloaded: {filename}")
            return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
    return False

def main():
    # Create images directory if it doesn't exist
    current_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(current_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    # Get unique URLs
    urls_file = os.path.join(current_dir, 'urls.txt')
    unique_urls = get_unique_urls(urls_file)
    
    print(f"Found {len(unique_urls)} unique URLs")
    
    # Download images
    successful = 0
    for url in unique_urls:
        if download_image(url, images_dir):
            successful += 1
    
    print(f"\nDownload complete!")
    print(f"Successfully downloaded {successful} out of {len(unique_urls)} images")

if __name__ == "__main__":
    main() 