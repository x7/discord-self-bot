import re
import time
import random

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

# Performance issues ??
def generate_reference_code():
    current_time_stamp = int(time.time() * 10)
    random_number = sum(random.randint(1, 100000) for _ in range(100))
    return current_time_stamp + random_number