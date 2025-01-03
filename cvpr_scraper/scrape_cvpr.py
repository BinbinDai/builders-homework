import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

def scrape_cvpr_papers():
    url = "https://openaccess.thecvf.com/CVPR2024?day=all"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # List to store paper information
    papers = []

    try:
        # Make request to the website
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # The papers are in dt elements
        paper_elements = soup.find_all('dt')
        
        for paper in paper_elements:
            # Get title (it's the first text before any links)
            title = paper.get_text().split('[')[0].strip()
            
            # Get authors (they're in the next dd element)
            authors_element = paper.find_next_sibling('dd')
            authors = authors_element.get_text().strip() if authors_element else ''
            
            # Get links (pdf, supplementary, arxiv)
            links = paper.find_all('a')
            paper_link = ''
            supp_link = ''
            arxiv_link = ''
            
            for link in links:
                link_text = link.get_text().lower()
                if 'pdf' in link_text:
                    paper_link = 'https://openaccess.thecvf.com/' + link['href']
                elif 'supp' in link_text:
                    supp_link = 'https://openaccess.thecvf.com/' + link['href']
                elif 'arxiv' in link_text:
                    arxiv_link = link['href']
            
            paper_info = {
                'title': title,
                'authors': authors,
                'paper_link': paper_link,
                'supplementary_link': supp_link,
                'arxiv_link': arxiv_link
            }
            papers.append(paper_info)
            
            # Add a small delay to be respectful to the server
            time.sleep(0.5)
            
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None
    except Exception as e:
        print(f"Error during scraping: {e}")
        return None

    # Create DataFrame and save to CSV
    if papers:
        df = pd.DataFrame(papers)
        df.to_csv('cvpr2024_papers.csv', index=False)
        print(f"Successfully scraped {len(papers)} papers and saved to cvpr2024_papers.csv")
    else:
        print("No papers were found to scrape")

if __name__ == "__main__":
    scrape_cvpr_papers() 