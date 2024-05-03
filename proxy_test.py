import csv
import requests

def check_proxy(proxy):
    try:
        response = requests.get('https://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=10)
        if response.status_code == 200:
            print(f"Proxy {proxy} is working")
        else:
            print(f"Proxy {proxy} returned status code {response.status_code}")
    except Exception as e:
        print(f"Error occurred while checking proxy {proxy}: {e}")

def main():
    with open('proxies.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            proxy = row[0]
            if not proxy.startswith('http://') and not proxy.startswith('https://'):
                proxy = 'http://' + proxy  # Assuming all proxies are HTTP proxies
            check_proxy(proxy)

if __name__ == "__main__":
    main()
