import time
import pymongo
from threading import Thread
from threadsafe_generator import threadsafe_generator

NUM_THREADS = 10
FIND_QUERY_PAGINATION_STEP = 1000
MONGO_URL = 'mongodb://localhost:270017/db'


client = pymongo.MongoClient(MONGO_URL)
db = client.my_database


@threadsafe_generator
def get_pagination_step_generator():
    count = 0
    while True:
        yield count
        count += FIND_QUERY_PAGINATION_STEP


def get_query(generator):
    output = []
    for skip_count in get_pagination_step_generator():
        cursor = db.my_first_collection\
            .find()\
            .skip(skip_count)\
            .limit(FIND_QUERY_PAGINATION_STEP)

        output = list(cursor)
        if len(output) == 0:
            break

        yield output
        output = []


def insert_data(generator, thread_index):
    for bulk_values in get_query(generator):
        if len(bulk_values):
            db.my_second_collection.insert_many(bulk_values)
            time.sleep(0.5)


def run(process, generator, thread_count):
    for thread_index in range(thread_count):
        thread = Thread(target=process, args=(generator, thread_index))
        thread.start()


def main():
    g = get_pagination_step_generator()
    run(insert_data, g, NUM_THREADS)


if __name__ == "__main__":
    main()
