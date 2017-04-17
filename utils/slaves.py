import threading

threadLock = threading.Lock()


class UbikThread (threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print "Starting " + self.name
        # Get lock to synchronize threads
        threadLock.acquire()
        keep_asking()
        # Free lock to release next thread
        threadLock.release()


def keep_asking():
    pass
