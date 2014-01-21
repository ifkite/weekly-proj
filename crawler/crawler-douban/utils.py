# merge only two tuple, will merge N tuple
# def merge_tup(tup1,tup2):
# 	tup1_list=list() if tup1==None else list(tup1)
# 	tup2_list=list() if tup2==None else list(tup2)
# 	tup1_list.extend(tup2_list)
# 	return tuple(tup1_list)
import gdbm
import hashlib
import random
import time
def merge_tups(*args):
	"""
	Merge tuples given in args, return one merged tuple.
	"""
	li=[]
	for tup in args:
		tup_list=list() if tup==None else list(tup)
		li.extend(tup_list)
	return tuple(li)

def calc_hash(url):
	"""
	Return a constant hash string for url.
	"""	
	return hashlib.sha1(url).hexdigest()[0:8]


# The following three *_condition() func are used for encapsulating condition ctrl processing.
# You can change the func for your condition ctrl processing.
# My condition ctrl is: app should run in a specific period, and app can continue running even though
# termiated before.
def init_condition():
	"""
	Initlize condition variable and persistance file.
	"""
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
def stop_condition(run_time,begin):
	"""
	Check condition,if app should stop then reutrn 1 else return 0.
	"""
	run_time,begin=run_time,begin
	stop=20# run 20 sec
	if run_time>stop-begin:
		return 1
	else:
		return 0
def update_flag(run_time,begin):
	"""
	Update flag that use for condition checking.
	"""
	# weak code,what will happen when call update_falg before calling init_condition
	pass_time=time.clock()-begin
	run_time=run_time+pass_time
	conf_db=gdbm.open('conf.db','w')
	conf_db['run_time']=str(run_time)
	conf_db.close()
	return (run_time,begin)

if __name__ == '__main__':
	"""
	Test *_condition() func.
	"""
	run_time,begin=init_condition()
	while not stop_condition(run_time,begin):
		for x in range(8000000):pass
		run_time,begin=update_flag(run_time,begin)
		print run_time