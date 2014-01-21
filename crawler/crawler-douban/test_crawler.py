import unittest
import utils
import mydb
import crawler
class TestCrawlerCase(unittest.TestCase):
	"""
	Actually this class tests many CrawlerDb methods.
	"""
	def setUp(self):
		"""
		Create crawlerdb field at the srart of testing process.
		"""
		self.crawlerdb=mydb.CrawlerDb()
		pass

	def tearDown(self):
		"""
		Close db connection after testing process.
		"""
		self.crawlerdb.close()
		pass

	def test_mydb_check_db_case1(self):
		url='http://book.douban.com/subject/1863930/'
		url_hash=utils.calc_hash(url)
		assert self.crawlerdb.check_db(url, url_hash)==None
		
	def test_mydb_check_db_case2(self):
		url='http://book.douban.com/subject/1863930/'
		url_hash=utils.calc_hash(url)
		self.crawlerdb.add_url(url,url_hash)
		assert self.crawlerdb.check_db(url,url_hash)>0
	
	def test_mydb_add_page_case1(self):
		ext_result_book=('title','isbn','book_id',1)
		self.crawlerdb.add_book_info(ext_result_book)
	
	def test_mydb_get_url_case1(self):
		self.crawlerdb.add_rank_info(12345678,0)
		assert self.crawlerdb.get_url()!=None

if __name__=='__main__':
	unittest.main()