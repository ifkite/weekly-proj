from threading import Thread
from Queue import Queue
import time
def worker(_task_queue):
	while(True):
		num=_task_queue.get()
		def sqrt(_num):
			time.sleep(2)
			print _num**2
		sqrt(num)
		_task_queue.task_done()

def main():
	t1=time.time()
	task_queue=Queue()
	for i in range(4):
		t=Thread(target=worker,args=(task_queue,))
		t.start()
		#ts.append(t)
	for i in range(100):
		task_queue.put(i)
	task_queue.join()
	#for t in ts:
	#	t.join()
	t2=time.time()
	print t2-t1

if __name__=='__main__':
	main()