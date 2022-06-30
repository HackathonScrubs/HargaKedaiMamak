import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

def create_thread(thread_count):
    threads_list = []

    for i in range(thread_count):
        x = threading.Thread(target=thread_function, args=(i,))
        threads_list.append(x);

    return threads_list

def start_thread(thread_list, options):

    if options == 0:
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        logging.info("Main    : before starting thread")

    for thread in thread_list:
        thread.start();

def join_thread(thread_list):
    for thread in thread_list:
        thread.join();

if __name__ == "__main__":
    thread_list = create_thread(100)
    start_thread(thread_list, 0)
    join_thread(thread_list)

    logging.info("Main    : wait for the thread to finish")
    logging.info("Main    : all done")
