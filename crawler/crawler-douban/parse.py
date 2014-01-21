import urllib
import urllib2
from bs4 import BeautifulSoup
import re
class HandleUrl:
	def __init__(self):
		self.page=None
		self.soup=None

	def get_page(self,url):
		"""
		Get page by url.
		This func should call before parse_book_info and fetch_urls called.
		"""
		req=urllib2.Request(url)
		response=urllib2.urlopen(req)#not take URLError or HTTPError into consideration
		self.page=response.read()
		self.soup=BeautifulSoup(self.page)

	def parse_book_info(self):
		"""
		Parse book info from page.
		Return a tuple with six field:title_info,author_info,isbn_info,tag_info,rating_info,votes_info.
		"""
		book_info=self.soup.find(id='info')
		# multi thread is a must
		title_info=self.soup.title.get_text().encode('utf-8').rstrip()
		author_info=book_info.find('a').get_text().encode('utf-8')
		isbn_info=book_info.get_text().encode('utf-8').splitlines()[-1].lstrip('ISBN: ')
		# one-to-multi
		tag_info=self.soup.find(id='db-tags-section').a.get_text().encode('utf-8')
		rating_info=self.soup.find(id='interest_sectl').strong.get_text().encode('utf-8').strip()
		votes=self.soup.find(id='interest_sectl').a.get_text().encode('utf-8')
		matchobj=re.match('\d+',votes)
		votes_info=matchobj.group()
		return (title_info,author_info,isbn_info,tag_info,rating_info,votes_info)

	def fetch_urls(self):
		"""
		Fetch urls that match with specific pattern.
		Return a list of urls.
		"""
		patterns=[]
		patterns.append('((http://)?(www\.)?book\.douban\.com/([a-zA-Z]+/){1,3}\d+/?$)')	
		urls=[]
		for link in self.soup.find_all('a'):
			link_str=link.get('href').encode('utf-8','ignore')
			for pattern in patterns:
				compiled_link=re.compile(pattern)
				matchobj=compiled_link.match(link_str)
				if matchobj:
					urls.append(link_str)
		return urls

if __name__=='__main__':
	handle=HandleUrl()
	handle.get_page('http://book.douban.com/subject/1858513/')
	urls=handle.fetch_urls()
	print urls