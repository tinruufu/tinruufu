from random import random
from time import sleep

from nt import post_random_image


def post_in(hour_limit, tags):
    seconds = hour_limit * 60 * 60 * random()
    sleep(seconds)
    post_random_image(tags)


if __name__ == '__main__':
    from sys import argv
    post_in(2, argv[1:])
