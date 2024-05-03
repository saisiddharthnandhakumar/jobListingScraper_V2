import csv
import requests
from bs4 import BeautifulSoup
import time

def scrape_google(query):
    base_url = f'https://www.google.com/search?q={query}&num=5'  # Google search URL
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='tF2Cxc')[:5]  # Limit to first 5 results
            search_results = []
            for result in results:
                title_elem = result.find('h3')
                title = title_elem.text.strip() if title_elem else ''
                snippet_elem = result.find('div', class_='IsZvec')
                snippet = snippet_elem.text.strip() if snippet_elem else ''
                link_elem = result.find('a')
                link = link_elem['href'] if link_elem else ''
                # Get meta description from source page
                meta_desc = get_meta_description(link)
                search_results.append((title, snippet, link, meta_desc))
            return search_results
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_meta_description(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_tag = soup.find('meta', attrs={'name': 'description'})
            if meta_tag:
                return meta_tag['content']
            else:
                return 'Meta description not found'
        else:
            print(f"Error fetching page: {response.status_code}")
            return 'Error fetching page'
    except Exception as e:
        print(f"Error: {e}")
        return 'Error fetching page'

def main():
    with open('search_terms.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            search_term = row[0]
            print(f"Scraping SERP for: {search_term}")
            results = scrape_google(search_term)
            if results:
                for i, result in enumerate(results, 1):
                    print(f"Result {i}:")
                    print(f"  Title on Search Page: {result[0]}")
                    print(f"  Description on Search Page: {result[1]}")
                    print(f"  Link on Search Page: {result[2]}")
                    print(f"  Meta Description: {result[3]}")
            time.sleep(5)  # Introduce a delay between requests to avoid rate limiting

if __name__ == "__main__":
    main()
