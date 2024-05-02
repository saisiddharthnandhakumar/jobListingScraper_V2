import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_google(query):
    base_url = f'https://www.google.com/search?q={query}&num=5'  # Google search URL
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}

    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='tF2Cxc')
            search_results = []
            for result in results:
                title = result.find('h3').text.strip()
                snippet_elem = result.find('div', class_='IsZvec')
                snippet = snippet_elem.text.strip() if snippet_elem else ''
                link = result.find('a')['href']
                search_results.append((title, snippet, link))
                if len(search_results) >= 5:
                    break  # Limit to first 5 results
            return search_results
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    data = []
    with open('search_terms.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            search_term = row[0]
            print(f"Scraping SERP for: {search_term}")
            results = scrape_google(search_term)
            if results:
                for result in results:
                    data.append([search_term] + list(result))
            time.sleep(5)  # Introduce a delay between requests to avoid rate limiting
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=['Search Term', 'Title on Search Page', 'Description on Search Page', 'Link on Search Page'])
    print(df)

if __name__ == "__main__":
    main()
