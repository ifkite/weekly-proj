import unittest
import utils
import mydb
import crawler
class TestCrawlerCase(unittest.TestCase):
	def setUp(self):
		# self.crawlerdb=mydb.CrawlerDb()
		pass

	def tearDown(self):
		# self.crawlerdb.close()
		pass

	# def test_mydb_check_db_case1(self):
	# 	url='http://book.douban.com/subject/1863930/'
	# 	url_hash=utils.calc_hash(url)
	# 	assert self.crawlerdb.check_db(url, url_hash)==None
		
	# def test_mydb_check_db_case2(self):
	# 	url='http://book.douban.com/subject/1863930/'
	# 	url_hash=utils.calc_hash(url)
	# 	self.crawlerdb.add_url(url,url_hash)
	# 	assert self.crawlerdb.check_db(url,url_hash)>0
	
	# def test_mydb_add_page_case1(self):
	# 	ext_result_book=('title','isbn','book_id',1)
	# 	self.crawlerdb.add_book_info(ext_result_book)
	
	# def test_mydb_get_url_case1(self):
	# 	self.crawlerdb.add_rank_info(12345678,0)
	# 	assert self.crawlerdb.get_url()!=None
	
	# def test_crawler_update_url_data(self):
	# 	craw_obj=crawler.Crawler()
	# 	urls=['http://book.douban.com/subject/3227098/','http://book.douban.com/subject/4854123/','http://book.douban.com/subject/4065258/']
	# 	craw_obj.update_url_data(urls[0])
	# 	# craw_obj.add_rank(rating_info=1234,key_id=0)	
	# 	# print craw_obj.get_url()
	# 	craw_obj.update_url_data(urls[1])
	# 	# craw_obj.add_rank(rating_info=12345,key_id=1)
	# 	# print craw_obj.get_url()
	# 	craw_obj.update_url_data(urls[2])

if __name__=='__main__':
	unittest.main()