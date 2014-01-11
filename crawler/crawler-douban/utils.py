# merge only two tuple, will merge N tuple
# def merge_tup(tup1,tup2):
# 	tup1_list=list() if tup1==None else list(tup1)
# 	tup2_list=list() if tup2==None else list(tup2)
# 	tup1_list.extend(tup2_list)
# 	return tuple(tup1_list)
import hashlib
import random
import marshal
import gdbm
import time
def merge_tups(*args):
	li=[]
	for tup in args:
		tup_list=list() if tup==None else list(tup)
		li.extend(tup_list)
	return tuple(li)
	# return tuple(li)
def calc_hash(url):
	url_hash=''
	for i in [random.randint(1,20) for x in range(8)]:
		url_hash+=hashlib.sha1(url).hexdigest()[i]
	return url_hash

def init_condition():
	begin=time.clock()
	try:
		utils_db=gdbm.open('conf.db','r')
		run_time=utils_db['run_time']
		utils_db.close()
		return (float(run_time),begin)
	except gdbm.error:
		new_time=0
		utils_db=gdbm.open('conf.db','c')
		utils_db['run_time']=str(new_time)
		utils_db.close()
		return (new_time,begin)
# def init_condition():
# 	# 'with' version later
# 	begin=time.clock()
# 	try:
# 		out=open('flag.dat','rb')
# 		run_time=marshal.load(out)
# 		out.close()
# 		return (run_time,begin)
# 	except IOError:
# 		new_time=0
# 		new_out=open('flag.dat','wb')
# 		marshal.dump(new_time,new_out)
# 		new_out.close()
# 		return (new_time,begin)

# return flag
def stop_condition(run_time,begin):
	run_time,begin=run_time,begin
	stop=20
	if run_time>stop-begin:
		return 1
	else:
		return 0

# def update_flag(run_time,begin):
# 	# run_time,begin=run_time,begin
# 	pass_time=time.clock()-begin
# 	run_time=run_time+pass_time
# 	ouf=open('flag.dat','wb')
# 	marshal.dump(run_time,ouf)
# 	ouf.close()
# 	print run_time
# 	return (run_time,begin)

def update_flag(run_time,begin):
	# weak code,what will happen when call update_falg before calling init_condition
	pass_time=time.clock()-begin
	run_time=run_time+pass_time
	conf_db=gdbm.open('conf.db','w')
	conf_db['run_time']=str(run_time)
	conf_db.close()
	return (run_time,begin)


if __name__ == '__main__':
	# url='http://www.douban.com/note/321347716/'
	# url_hash=calc_hash(url)
	# print url_hash
	run_time,begin=init_condition()
	while not stop_condition(run_time,begin):
		for x in range(8000000):pass
		run_time,begin=update_flag(run_time,begin)
		print run_time