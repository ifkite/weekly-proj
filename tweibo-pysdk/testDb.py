import MySQLdb
def connectDb():
    cont=MySQLdb.connect(user='root',passwd='calm')#set your user and passwd pairs in your MySQL first
    cont.set_character_set('utf8')
    cur=cont.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    cur.execute('''USE tweet''')
    return (cont,cur)
cont,cur=connectDb()
if __name__=='__main__':
    li=cur.execute('''SELECT subject,count(subject) from tweet_info group by subject ORDER BY count(subject) DESC LIMIT 10''')
    res=cur.fetchall()
    for r in res:
        print r[0].decode('utf-8')
      #   for d in r:
		    # print d