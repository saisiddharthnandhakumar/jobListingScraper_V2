import csv
import requests
from bs4 import BeautifulSoup
import time

def scrape_google(query):
    base_url = f'https://www.google.com/search?q={query}&num=5'  # Google search URL
    headers = {'User-Agent': 'Your User Agent'}  # Replace with your user agent

    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='tF2Cxc')
            search_results = []
            for result in results:
                title = result.find('h3').text.strip()
                snippet = result.find('div', class_='IsZvec').text.strip()
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
    with open('search_terms.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            search_term = row[0]
            print(f"Scraping SERP for: {search_term}")
            results = scrape_google(search_term)
            if results:
                print(results)  # Print the results for demonstration
            time.sleep(5)  # Introduce a delay between requests to avoid rate limiting

if __name__ == "__main__":
    main()
