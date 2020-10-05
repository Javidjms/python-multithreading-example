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
