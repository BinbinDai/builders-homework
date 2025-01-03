import requests
from bs4 import BeautifulSoup
import pandas as pd
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
        
        # Find all paper titles (dt elements with class ptitle)
        paper_elements = soup.find_all('dt', class_='ptitle')
        
        for paper in paper_elements:
            # Get title from the a tag within dt
            title_tag = paper.find('a')
            title = title_tag.get_text().strip() if title_tag else ''
            
            # Get the next two dd elements
            dd_elements = paper.find_next_siblings('dd', limit=2)
            
            if len(dd_elements) >= 2:
                # First dd contains author forms
                authors_dd = dd_elements[0]
                # Extract author names from the forms
                author_links = authors_dd.find_all('a', onclick=True)
                authors = [link.get_text().strip() for link in author_links]
                authors_str = ', '.join(authors)
                
                # Second dd contains links
                links_dd = dd_elements[1]
                links = links_dd.find_all('a')
                
                paper_link = ''
                supp_link = ''
                
                for link in links:
                    if link.get_text().lower() == 'pdf':
                        paper_link = 'https://openaccess.thecvf.com' + link['href']
                    elif link.get_text().lower() == 'supp':
                        supp_link = 'https://openaccess.thecvf.com' + link['href']
            
                paper_info = {
                    'title': title,
                    'authors': authors_str,
                    'paper_link': paper_link,
                    'supplementary_link': supp_link
                }
                papers.append(paper_info)
            
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
        
        # Save to JSON
        with open('cvpr2024_papers.json', 'w') as f:
            json.dump(papers, f, indent=2)
            
        print(f"Successfully scraped {len(papers)} papers and saved to CSV and JSON files")
    else:
        print("No papers were found to scrape")

if __name__ == "__main__":
    scrape_cvpr_papers() 