from multiprocessing import Pool
import timeit
import time
def f(x):
	return x*x

if __name__=='__main__':
	pool=Pool(4)
	t1=time.time()
	pool.apply_async(f,2)
	t2=time.time()
	print t2-t1

	t3=time.time()
	map(lambda x:x**2,range(100))
	t4=time.time()
	print t4-t3

	t5=time.time()
	for x in range(100):
		f(x)
	t6=time.time()

	print t6-t5