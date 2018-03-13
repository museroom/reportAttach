from queue import Queue
from threading import Thread


def do_stuff(i, q):
    while True:
        print("{}:{}".format(i, q.get()))
        q.task_done()


q = Queue(maxsize=0)
num_threads = 10

for i in range(num_threads):
    worker = Thread(target=do_stuff, args=(i, q,))
    worker.setDaemon(True)
    worker.start()
    # workers.append(worker)

for x in range(100):
    q.put(x)

q.join()

for x in range(100,200):
    q.put(x)

q.join()

