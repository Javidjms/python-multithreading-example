import pymongo
from threading import Thread


STEP = 1000
NUM_THREADS = 10
THREAD_STEP = STEP * NUM_THREADS  # 10000
MONGO_URL = 'mongodb://localhost:270017/db'

client = pymongo.MongoClient(MONGO_URL)
db = client.my_database


def get_query(thread_index):
    count = 0
    output = []
    while True:
        skip_count = count * THREAD_STEP + thread_index * STEP
        cursor = db.my_first_collection\
            .find()\
            .skip(skip_count)\
            .limit(STEP)

        output = list(cursor)

        if len(output) == 0:
            break

        yield output
        count += 1
        output = []


def insert_data(thread_index):
    for bulk_values in get_query(thread_index):
        if len(bulk_values):
            print('BULK INSERTED BY THEAD COUNT', thread_index)
            db.my_second_collection.insert_many(bulk_values)


def run(process, thread_count):
    for thread_index in range(thread_count):
        thread = Thread(target=process, args=(thread_index))
        thread.start()


def main():
    run(insert_data, NUM_THREADS)


if __name__ == "__main__":
    main()
