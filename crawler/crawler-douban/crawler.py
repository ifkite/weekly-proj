import parse
import settings
import utils
from mydb import CrawlerDb
class Crawler:
	def __init__(self):
		self.crawlerdb=CrawlerDb()
		# if check_url(settings.START_URL):# check if the url is available or not
		self.update_url_data(settings.START_URL)

	def geturl(self):
		"""get an url from data base"""
		#this func determine that the way you crawl websites, depth-first, breadth-first or ohters
		# need database to get url
		return crawlerdb.geturl()

	def update_evaluate(self,key_id):
		pass

	def update_url_data(self,url):
	# put url to datbase
		url_hash=utils.calc_hash(url)
		key_id=check_db(url,url_hash)
		if not key_id:
			add_url(url,url_hash)
			# #IMPROVE(ifkite): use namedtule
			# result_book=parse_page(url)#return tuple
			# ext_result_book=utils.merge_tups(result_book,new_key_id)
			# add_page(ext_result_book)
			# evalu=rank_page()
			# add_evalu(evalu)
		elif key_id>0:
			update_evaluate(key_id)#page has been in db
		else:
			pass# collision

	def update_priority_by_raw_page(self,rating_info,votes_info,key_id):
		# write your rank func here
		# calc rank by rating_info and roves_info
		rank=rating_info
		crawlerdb.add_rank_info(rank,key_id)


	def add_book_data(self,key_id,page):
		title_info,author_info,isbn_info,tag_info,rating_info,votes_info=parse_book_info(page)
		update_priority_by_raw_page(rating_info,votes_info,key_id)
		result_book_info=(title_info,author_info,isbn_info,tag_info)
		final_book_info=utils.merge_tups(result_book_info,key_id)
		add_book_info(final_book_info)# database operation

	def crawl(self):
		# utils.init_condition()
		run_time,begin=utils.init_condition()
		handle=parse.HandleUrl()
		while not utils.stop_condition(run_time,begin):
			key_id,url=geturl()

			page=handle.get_page(url)
			urls=handle.fetch_urls()
			# add_book_data(key_id,page)
			title_info,author_info,isbn_info,tag_info,rating_info,votes_info=handle.parse_book_info()

			update_priority_by_raw_page(rating_info,votes_info,key_id)
			result_book_info=(title_info,author_info,isbn_info,tag_info)
			final_book_info=utils.merge_tups(result_book_info,key_id)
			add_book_info(final_book_info)# database operation
			
			for url in urls:
				update_url_data(url)
			
			run_time,begin=utils.update_flag(run_time,begin)

if __name__=='__main__':
	crawler=Crawler()
	crawler.crawl()