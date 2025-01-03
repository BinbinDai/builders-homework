from bs4 import BeautifulSoup
import pandas as pd
import re

def extract_authors(dd_element):
    """Extract author names from the dd element containing forms"""
    authors = []
    for form in dd_element.find_all('form', class_='authsearch'):
        author_link = form.find('a')
        if author_link:
            authors.append(author_link.text.strip())
    return ', '.join(authors)

def parse_cvpr_papers():
    # Read the local HTML file
    with open('cvpr_2024.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'lxml')
    papers = []
    
    # Find all paper titles (they're in dt elements with class 'ptitle')
    paper_elements = soup.find_all('dt', class_='ptitle')
    
    for paper in paper_elements:
        # Get title
        title_link = paper.find('a')
        if not title_link:
            continue
        title = title_link.text.strip()
        
        # Get the next dd element for authors
        authors_dd = paper.find_next_sibling('dd')
        authors = extract_authors(authors_dd) if authors_dd else ''
        
        # Get the next dd element for links
        links_dd = authors_dd.find_next_sibling('dd') if authors_dd else None
        paper_link = ''
        supp_link = ''
        
        if links_dd:
            links = links_dd.find_all('a')
            for link in links:
                link_text = link.text.strip().lower()
                if link_text == 'pdf':
                    paper_link = 'https://openaccess.thecvf.com' + link['href']
                elif link_text == 'supp':
                    supp_link = 'https://openaccess.thecvf.com' + link['href']
        
        paper_info = {
            'title': title,
            'authors': authors,
            'paper_link': paper_link,
            'supplementary_link': supp_link
        }
        papers.append(paper_info)
    
    # Create DataFrame and save to CSV
    if papers:
        df = pd.DataFrame(papers)
        df.to_csv('cvpr2024_papers_local.csv', index=False)
        print(f"Successfully parsed {len(papers)} papers and saved to cvpr2024_papers_local.csv")
    else:
        print("No papers were found in the HTML file")

if __name__ == "__main__":
    parse_cvpr_papers() 