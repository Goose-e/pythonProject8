import random
import time


def generationId():
    return int(time.time())+random.randint(0, 9999)