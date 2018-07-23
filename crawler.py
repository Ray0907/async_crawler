import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

res = requests.get('https://www.rottentomatoes.com/top/')
soup = BeautifulSoup(res.text,'lxml')
movie_list=[]

for link in soup.select('section li a[href]'):
    movie_list.append('https://www.rottentomatoes.com'+link.get('href'))
async def request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text(encoding='utf-8')
            soup = BeautifulSoup(body,'lxml')
            movie = []
            # no need to call async for here!
            for link in soup.select('section#top_movies_main table a'):
                movie.append('https://www.rottentomatoes.com'+link['href'])

        return  movie

async def parse(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text(encoding='utf-8')
            soup = BeautifulSoup(body, 'lxml')

            data={
                'Title' : soup.select('div h1')[0].text.strip(),
                'TOMATOMETER': soup.select('#tomato_meter_link  span span')[0].text,
                'AUDIENCE SCORE' : soup.select('div.meter-value span')[0].text,
            }
        return data



async def main():
    results = await asyncio.gather(*[request(url) for url in movie_list])


    movie = []
    for  i in range(len(results)):
        data = await asyncio.gather(*[parse(url) for url in results[i]])
        movie.append(data)
    print(movie)

#print(movie_list)

loop = asyncio.get_event_loop()
results = loop.run_until_complete(main())