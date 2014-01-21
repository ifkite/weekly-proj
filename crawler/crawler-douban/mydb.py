import parse
import sqlite3
import utils
import settings
class CrawlerDb:
	def __init__(self):
		# connect
		"""
		Initlize db app:connect to db and create tables if not exists in db.
		"""
		db_name='crawler.db'
		self.cont=sqlite3.connect(db_name)
		self.cont.text_factory=str
		self.cur=self.cont.cursor()
		self.cur.execute('''CREATE TABLE IF NOT EXISTS url_info (key_id INTEGER primary key autoincrement,url text,url_hash text)''')		
		self.cur.execute('''CREATE TABLE IF NOT EXISTS book_info (title text,author text,isbn text,tags text,book_id INTEGER,foreign key (book_id) references url_info(key_id))''')
		self.cur.execute('''CREATE TABLE IF NOT EXISTS evalu_info (rank INTEGER,depth INTEGER,reverse_link INTEGER,score INTEGER,comments INTEGER,visited INTEGER default(0),eva_id INTEGER,foreign key (eva_id) references url_info(key_id))''')
		
	def check_db(self,url,url_hash):
		# TODO(ifkite):deal with url_hash collision
		"""
		Check if url has been in db by url_hash and url.
		Use url_hash to accerlate db checking procession.
		"""
		self.cur.execute("SELECT url,key_id FROM url_info WHERE url_hash=(?)",(url_hash,))
		result_list=self.cur.fetchall()
		if not result_list:#if result_list==None:
			return None# url is not in db
		else:
			# may be collision,url_hashs are the same even though their urls do not equal
			# the following code deal with the case when inserting the same url twice
			result_dict=dict((x,y) for x,y in result_list)
			if url in result_dict: 
				return result_dict[url]
			else:
				return -1# collision

	def add_url(self,url,url_hash):
		"""
		Add url, and url_hash into db.
		"""
		self.cur.execute("INSERT INTO url_info(url,url_hash) VALUES(?,?)",(url,url_hash))
		self.cont.commit()

	def add_book_info(self,ext_result_book):
		"""
		Add book info into db.
		"""
		self.cur.execute("INSERT INTO book_info(title,author,isbn,tags,book_id) VALUES(?,?,?,?,?)",ext_result_book)
		self.cont.commit()
		# ignore http:abc/de and http:ab/cde
	def get_url(self):
		"""
		Get url from db.
		Note that the rank info about the url must have been existed in db.  
		"""
		self.cur.execute('''SELECT eva_id FROM evalu_info WHERE visited==0 ORDER BY rank DESC LIMIT 1''')
		key_id=self.cur.fetchone()
		self.cur.execute("UPDATE evalu_info SET visited=1 WHERE eva_id=(?)",key_id)
		self.cont.commit()
		self.cur.execute("SELECT url FROM url_info WHERE key_id=(?)",key_id)
		url=self.cur.fetchone()
		res=utils.merge_tups(key_id,url)
		if settings.DEBUG_FLAG:
			print res
		return res

	def add_rank_info(self,rank,key_id):
		"""
		Add rank of page into db.
		Pages are distinguished by key_id.
		"""
		self.cur.execute("INSERT INTO evalu_info(rank,eva_id) VALUES(?,?)",(rank,key_id))
		self.cont.commit()
	
	def close(self):
		"""
		Close db connection.
		Should be called after all db operation.
		"""
		self.cont.commit()
		self.cont.close()

if __name__=='__main__':
	"""
	Test code for db.
	"""
	
	crawlerdb=CrawlerDb()
	# test on check_db() and add_url()
	url='http://book.douban.com/subject/1863930/'
	url_hash='12345678'
	crawlerdb.cur.execute("DELETE FROM url_info WHERE url_hash=(?)",(url_hash,))
	for i in range(2):
		check_num=crawlerdb.check_db(url+'aa',url_hash)
		if not check_num:
			crawlerdb.add_url(url)
			print 'inserted ok'
		elif check_num==-1:
			print 'url_hash collosion'
		else:
			print 'failed'
			print 'url has been in db'
	# test add_page()
	crawlerdb.add_url(url)
	crawlerdb.add_page(('a','b','c','d'))
	crawlerdb.cur.execute("DELETE FROM book_info WHERE title='a'")
	result_list=crawlerdb.cur.fetchall()
	print len(result_list)
	for result in result_list:
		print result