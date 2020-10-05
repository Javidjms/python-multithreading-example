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
