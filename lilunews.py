# lilunews.py

import feedparser
import random
import datetime
import os
from dotenv import load_dotenv
import bitlyshortener


load_dotenv()


feeds = [
	'https://3dnews.ru/games/rss/',
	'http://igromania.ru/rss/rss_news.xml',
	'https://dtf.ru/rss',
	# goha
	'https://www.goha.ru/rss/anime',
	'https://www.goha.ru/rss/mmorpg',
	'https://www.goha.ru/rss/videogames',

	'https://www.noob-club.ru/rss2.xml',

	# англ
	'https://kotaku.com/rss',
	'https://www.rockpapershotgun.com/feed/'
]

# tokens_pool = ["ede3f029d0703d9b29517845a2235e23b6c3d211"]

shortener = bitlyshortener.Shortener(tokens=[os.getenv('BITLY_TOKEN')], max_cache_size=256)

TITLE = 'title'
LINK  = 'link'


class News:

	__slots__ = (
		'sources',
		'feeds',
		'last_update',
	)

	def default():
		return News(feeds)

	def __init__(self, sources):
		self.sources = sources
		self.last_update = datetime.date.min
		self.check_for_update()


	def fetch(self):
		self.feeds = [feedparser.parse(url)['entries'] for url in self.sources]
		self.last_update = datetime.date.today()


	def get_random(self) -> (str, str, str):
		self.check_for_update()

		feed_idx = random.randint(0, len(self.feeds) - 1)
		news_idx = random.randint(0, len(self.feeds[feed_idx]) - 1)

		short = shortener.shorten_urls([self.feeds[feed_idx][news_idx][LINK]])

		return (self.feeds[feed_idx][news_idx][TITLE], short[0], self.feeds[feed_idx][news_idx][LINK])


	def __str__(self) -> str:
		out = ''
		nl = '\n'
		
		out += f'Sources:{nl} {nl.join(self.sources)}'
		out += nl + nl

		for i in range(len(self.feeds)):
			feed = self.feeds[i]
			out += f'Source {self.sources[i]} has {len(feed[i])} news{nl}'
			# out += f'Keys:{nl} {" ,".join(feed[i].keys())}'
			out += nl

		return out or ""

	def check_for_update(self):
		now = datetime.date.today()
		next_update = self.last_update + datetime.timedelta(days=1)

		if now < next_update:
			return

		self.fetch()



def main():
	news = News.default()

	print(news)
	res = news.get_random()
	print(res)

if __name__ == "__main__":
    main()