#so naive
import thread,time
def read():
    exitmutexes.append(thread.allocate_lock())
    while 1:
        pipe_mutex.acquire()
        if len(li):
            print li[0]
            del li[0]
        pipe_mutex.release()
        time.sleep(2)

def write():
    exitmutexes.append(thread.allocate_lock())
    num = 0
    while 1:
        pipe_mutex.acquire()
        li.append(num)
        num = num + 1
        pipe_mutex.release()
        time.sleep(2)

li = []
exitmutexes = []
pipe_mutex = thread.allocate_lock()
thread.start_new(read,())
thread.start_new(write,())
time.sleep(0.2)
for mutex in exitmutexes:
    while not mutex.locked():pass
print 'main thread terminate'
