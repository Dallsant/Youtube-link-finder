import asyncio 
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

executor = ThreadPoolExecutor(max_workers=5)
loop = asyncio.get_event_loop()


def get_song_names():
	with open("songnames.txt", 'r') as f:
		data = f.readlines()
	return data

async def make_requests(names):
	responses = []
	futures = [loop.run_in_executor(executor, requests.get,
	 f"https://www.youtube.com/results?search_query={name[:-1]}") for name in names]
	await asyncio.wait(futures)
	for response in futures:
		responses.append(response.result().content)
	return responses

# Finds the first recommendation from the responses and returns a list of links
def filter_resposes(responses):
	links = []
	for response in responses:
		soup = BeautifulSoup(response, 'html.parser')
		for html in soup.find_all('a'):
			href = html.get('href')
			if href.find('watch?v=') == 1:
				links.append(f'https://www.youtube.com{href}')
				break
	return links

# Write down all links in txt file, 
def write_links(links):	
	with open("links.txt", 'w+') as f:
		f.write('')
	for link in links:
		with open("links.txt", 'a') as f:
			f.write(f'{link}\n')

if __name__ == '__main__':
	names = get_song_names()
	responses = loop.run_until_complete(make_requests(names))
	links = filter_resposes(responses)
	write_links(links)