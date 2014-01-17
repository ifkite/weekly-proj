import urllib
import urllib2
from bs4 import BeautifulSoup
import re
class HandleUrl:
	def __init__(self):
		self.page=None
		self.soup=None

	def get_page(self,url):
		# return html page
		req=urllib2.Request(url)
		response=urllib2.urlopen(req)#not take URLError or HTTPError into consideration
		self.page=response.read()
		self.soup=BeautifulSoup(self.page)
		# return page
		# deal with exception

	# def filter(self,link):


	#def add_book_data(self,key_id):
	def parse_book_info(self):
		# pattern='((http://)?(www\.)?book\.douban\.com/([a-zA-Z]+/){1,3}\d+/?$)'	
		# compiled_link=re.compile(pattern)
		# li=[]
		# for link in self.soup.find_all('a'):
		# 	link_str=link.get('href').encode('utf-8','ignore')
		# 	matchobj=compiled_link.match(link_str)
		# 	if matchobj:
		# 		li.append(link_str)
		# print li
		book_info=self.soup.find(id='info')
		# print book_info.get_text().encode('utf-8')
		# book_info_list=book_info.get_text().encode('utf-8').splitlines()
		# junk_str.encode('utf-8')
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
		# print [text for text in data.get_text().encode('utf-8')]

	def fetch_urls(self):
		# patterns=[]
		# patterns.append('(http://)?(www\.)?book\.([a-zA-Z]+/){1,3}\d+/?$')
		# # pattern='(http://)?(www\.)?book\.([a-zA-Z]+/){1,3}\d+/?$'
		# # links=self.soup.find_all('a').get('href').encode('utf-8','ignore')
		# # pattern='(http://)?(www\.)?read\.([a-zA-Z]+/){1,3}\d+/?$'
		# # multi thread
		# urls=[]
		# for link_tag in self.soup.find_all('a'):
		# 	link=link_tag.get('href').encode('utf-8','ignore')
		# 	for pattern in patterns:
		# 		compiled_link=re.compile(pattern)
		# 		matchobj=compiled_link.match(link)
		# 		if matchobj:
		# 			print matchobj.group()
		# 		else:
		# 			print 'not match'
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

			# matchobj=compiled_link.match(self.page)
		# 	if matchobj:
		# 		# urls.append(matchobj.group())
		# 		print matchobj.group()
		# 	else:
		# 		print 'not match'
		# return urls	


def testre():
	# regular, with[]
	pattern='(http://)?(www\.)?book\.([a-zA-Z]+/){1,3}\d+/?$'
	# pattern='(http://)?(www\.)?read\.([a-zA-Z]+/){1,3}\d+/?$'
	compiled_link=re.compile(pattern)
	matchobj=compiled_link.match('http://www.book.com/111')
	if matchobj:
		print 'match'
	else:
		print 'not match'

if __name__=='__main__':
	handle=HandleUrl()
	handle.get_page('http://book.douban.com/subject/1858513/')
	# handle.fetch_urls()
	urls=handle.fetch_urls()
	print urls
	# t=handle.parse_book_info()
	# for v in t:
	# 	print v
	# # testre()
