# Python Multithreading Example

## Code

```python
#  multithreading.py
import time
from threading import Thread
from threadsafe_generator import threadsafe_generator

NUM_THREADS = 10


@threadsafe_generator
def get_generator():
    count = 0
    while True:
        if count >= 500:
            break
        count += 1
        yield count


@threadsafe_generator
def get_generator_bis():
    return iter(range(0, 500))


def main_process(generator, thread_index):
    for value in generator:
        print('Thread ID :', thread_index, 'Value :', value)
        time.sleep(0.1)


def run(process, generator, thread_count):
    for thread_index in range(thread_count):
        thread = Thread(target=process, args=(generator, thread_index))
        thread.start()


def main():
    # g1 = get_generator()
    g2 = get_generator_bis()
    run(main_process, g2, NUM_THREADS)


if __name__ == "__main__":
    main()
```

## Installation

```bash
docker-compose build
docker-compose up -d
docker-compose exec app python example_bot_url_ping.py
```

## Example

```python
#  example_bot_url_ping.py
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

```

```python
#  example_download_files.py
import os
import time
import subprocess
from threading import Thread
from threadsafe_generator import threadsafe_generator

NUM_THREADS = 10

DOWNLOAD_URLS = [
    'http://localhost:8000/media/images/image1.png',
    'http://localhost:8000/media/images/image2.png',
    'http://localhost:8000/media/images/image3.png',
    # ............................................#
    # ............................................#
    # ............................................#
    'http://localhost:8000/media/images/image998.png',
    'http://localhost:8000/media/images/image999.png',
    'http://localhost:8000/media/images/image1000.png',
]

OUTPUT_FOLDER_PATH = '/tmp/downloads'


@threadsafe_generator
def get_url_generator():
    return iter(DOWNLOAD_URLS)


def download_file(url, output_path):
    cmd = [
        "wget",
        "--no-check-certificate",
        "{}".format(url),  # f"{url}"
        "--output-document",
        "{}".format(output_path),  # f"{output_path}"
    ]
    subprocess.run(cmd)


def main_process(generator, thread_index):
    for url in generator:
        filename = os.path.basename(url)
        output_path = '{}/{}'.format(OUTPUT_FOLDER_PATH, filename)
        download_file(url, output_path)
        time.sleep(1)


def run(process, generator, thread_count):
    for thread_index in range(thread_count):
        thread = Thread(target=process, args=(generator, thread_index))
        thread.start()


def main():
    g = get_url_generator()
    run(main_process, g, NUM_THREADS)


if __name__ == "__main__":
    main()

```

```python
#  example_mongo_bulk_insert_db_simple.py
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

```

```python
#  example_mongo_bulk_insert_db_with_threadsafe.py
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

```

## Contributors

* [Javid Mougamadou](https://github.com/Javidjms)
