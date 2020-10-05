import time
import requests
from threading import Thread

NUM_THREADS = 10

PING_URL = 'http://localhost:8000'


def main_process():
    requests.get(PING_URL)
    time.sleep(1)


def run(process, thread_count):
    for thread_index in range(thread_count):
        thread = Thread(target=process)
        thread.start()


def main():
    run(main_process, NUM_THREADS)


if __name__ == "__main__":
    main()
