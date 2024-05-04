import googleapiclient.discovery

# Create a Google Custom Search API client.
custom_search_client = googleapiclient.discovery.build(
    "customsearch", "v1", developerKey="YOUR_API_KEY"
)

# Perform a search.
search_results = custom_search_client.cse().list(
    q="YOUR_SEARCH_QUERY", cx="YOUR_SEARCH_ENGINE_ID"
).execute()

# Get the meta title and meta description of each search result.
for result in search_results["items"]:
    meta_title = result["title"]
    meta_description = result["snippet"]

    # Print the meta title and meta description.
    print("Meta Title:", meta_title)
    print("Meta Description:", meta_description)
    print()