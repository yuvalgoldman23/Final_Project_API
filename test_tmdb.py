import asyncio
import aiohttp

# Set up your TMDB API key and base URLs
API_KEY = "YOUR_API_KEY"
BASE_URL = "https://api.themoviedb.org/3"
AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmM2NhNmMxMWVhZjQzNDY1YTE4MTRmYTNhMjQ0MGYzNyIsIm5iZiI6MTcyODczODUxMS4yNDc2OTYsInN1YiI6IjY1YmZiZTE3MDMxZGViMDE4M2YxNjhjYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.hZkDyMAhf2L4PtJ5W8T4bC0M5kojxLj9XEK9oN5qkl0"

headers = {
    "accept": "application/json",
    "Authorization": AUTH_TOKEN
}


async def fetch(session, url):
    async with session.get(url, headers=headers) as response:
        return await response.json() if response.status else None


async def get_available_regions(session):
    # Fetch the list of available regions (country codes) for watch providers
    url = f"{BASE_URL}/watch/providers/regions?api_key={API_KEY}"
    return await fetch(session, url)


async def get_available_providers(session, country_code):
    # Get the list of watch providers available in a given country
    url = f"{BASE_URL}/watch/providers/movie?api_key={API_KEY}&watch_region={country_code}"
    return await fetch(session, url)


async def discover_movies(session, provider_id, country_code, num_pages=1):
    tasks = []
    for page in range(1, num_pages + 1):
        url = f"{BASE_URL}/discover/movie?include_adult=false&include_video=false&language=en-US&sort_by=popularity.desc&with_watch_providers={provider_id}&watch_region={country_code}&page={page}"
        tasks.append(fetch(session, url))
        print("url is " , url)

    results = await asyncio.gather(*tasks)

    for page, movies in enumerate(results, start=1):
        if movies and 'results' in movies:
            print(f"\nPage {page} results:")
            for movie in movies['results']:
                print(f"Title: {movie['title']}, Popularity: {movie['popularity']}")
        else:
            print(f"Failed to fetch movies on page {page}")


async def main():
    async with aiohttp.ClientSession() as session:
        # Get the available regions (country codes)
        regions = await get_available_regions(session)

        if regions and 'results' in regions:
            region_dict = {region['iso_3166_1']: region['english_name'] for region in regions['results']}

            # Show the user available regions
            print("Available regions (countries):")
            for idx, (country_code, country_name) in enumerate(region_dict.items(), 1):
                print(f"{idx}. {country_name} ({country_code})")

            # Ask the user to choose a region
            region_choice = int(input("Choose a region (enter the number): "))
            country_code = list(region_dict.keys())[region_choice - 1]

            # Get the available providers for the chosen region
            providers_response = await get_available_providers(session, country_code)

            if providers_response and 'results' in providers_response:
                providers = {provider['provider_name']: provider['provider_id'] for provider in
                             providers_response['results']}

                # Show the user available streaming providers
                print("Available streaming providers:")
                for idx, provider_name in enumerate(providers.keys(), 1):
                    print(f"{idx}. {provider_name}")

                # Ask the user to choose a provider
                provider_choice = int(input("Choose a provider (enter the number): "))
                provider_name = list(providers.keys())[provider_choice - 1]
                provider_id = providers[provider_name]

                # Ask how many pages of results to fetch
                num_pages = int(input("How many pages of results would you like to fetch (e.g., 2 or 3)? "))

                # Discover movies on the chosen provider and country
                print(f"\nDiscovering movies on {provider_name} in {country_code}...\n")
                await discover_movies(session, provider_id, country_code, num_pages)
            else:
                print("No providers available for the selected country.")
        else:
            print("No regions available.")


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
