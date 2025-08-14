#AIzaSyBIJBPEO7kc4x_qeCe_NgIafmRi2pEgMNc
#Google API Key
#id d51c54d71d0544094

import requests

def google_search(query, api_key, cse_id):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}"

    response = requests.get(url)

    if response.status_code == 200:
        results = response.json()
       
        if "items" in results:
            top_result = results["items"][0]
            title = top_result["title"]
            snippet = top_result["snippet"]
            link = top_result["link"]

            print(f"Title: {title}")
            print(f"Snippet: {snippet}")
            print(f"Link: {link}")
        else:
            print("No results found.")
    else:
        print("Error in the search request:", response.status_code)

if __name__ == "__main__":
    api_key = "AIzaSyBIJBPEO7kc4x_qeCe_NgIafmRi2pEgMNc"
    cse_id = "d51c54d71d0544094"

    query = input("Enter a search query: ")

    google_search(query, api_key, cse_id)
