import aiohttp
import asyncio
import warnings
import sys
import time
import os


# TODO - the idea for better fetching of Lists: fetch the tmdb info separately from the DB info, and then combine to a watchlist
# We could do both async and then the whole website would be much faster

# Redirect stderr to null device
sys.stderr = open(os.devnull, 'w')

# Suppress all warnings
warnings.filterwarnings("ignore")

# Custom exception handler to suppress all exceptions
def custom_exception_handler(loop, context):
    pass  # Do nothing, effectively suppressing the exception

async def fetch_movie(session, movie_id, api_key):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    async with session.get(url) as response:
        movie_data = await response.json()
        print(movie_data)  # Print movie data as soon as it arrives
        return movie_data

async def fetch_movies(movie_ids, api_key):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch_movie(session, movie_id, api_key)) for movie_id in movie_ids]
        await asyncio.gather(*tasks)

async def main():
    movie_ids = [
        95396,
        646097,
        698687,
        945961,
        704239,
        130853,
        473033,
        933260,
        1226578,
        762441
    ]
    api_key = '2e07ce71cc9f7b5a418b824c87bcb76f' # Replace with your actual API key

    start_time = time.time()  # Start timing
    await fetch_movies(movie_ids, api_key)
    end_time = time.time()  # End timing

    print(f"\nTime taken: {end_time - start_time:.2f} seconds")  # Print elapsed time

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(custom_exception_handler)
    asyncio.run(main())