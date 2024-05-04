import googleapiclient.discovery

API_KEY = open('API_KEY').read()
SEARCH_ENGINE_ID = open('SEARCH_ENGINE_ID').read()

# Create a Google Custom Search API client.
custom_search_client = googleapiclient.discovery.build(
    "customsearch", "v1", developerKey=API_KEY
)

# Perform a search.
search_results = custom_search_client.cse().list(
    q="Registered Nurse Jobs New York City, New York", cx=SEARCH_ENGINE_ID, num=5
).execute()

# Get the meta title and meta description of each search result.
for result in search_results["items"]:
    meta_title = result["title"]
    meta_description = result["snippet"]
    link = result["link"]

    # Print the meta title and meta description.
    print("Meta Title:", meta_title)
    print("Meta Description:", meta_description)
    print("Link:", link)
    print()
