import nest_asyncio
nest_asyncio.apply()

import time
import asyncio
import csv
import aiohttp
from bs4 import BeautifulSoup

# global headers to be used for requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

MAX_THREADS = 10


async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            return await response.text()

async def extract_title_data_rank(url):
    html = await fetch_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    movies = soup.findAll('li', class_='ipc-metadata-list-summary-item')[:10]
    movies_list = []
    for movie in movies:
        title_element = movie.find('h3')
        title = title_element.text if title_element else 'N/A'

        date_element = movie.select_one('span.sc-14dd939d-6')
        date = date_element.text if date_element else 'N/A'

        rank_element = movie.select_one('span.ipc-rating-star ')
        rank = rank_element.text if rank_element else 'N/A'

        movies_dict = {
            'title': title,
            'date': date,
            'rank': rank,
        }
        movies_list.append(movies_dict)

    with open(file='movies.csv', mode='w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Date', 'Rank'])
        writer.writerows((movie['title'], movie['date'],movie['rank']) for movie in movies_list)

async def main():
    start_time = time.time()
    URL = 'https://www.imdb.com/chart/top/'
    await extract_title_data_rank(URL)

    end_time = time.time()
    print('Total time taken: ', end_time - start_time)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
