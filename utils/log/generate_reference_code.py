import time
import random

def generate_reference_code():
    timestamp = int(time.time() * 1000)
    rand_part = random.randint(1000, 9999)
    code = str(timestamp) + str(rand_part)

    return code[-10:]