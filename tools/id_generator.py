import random
import string
from datetime import datetime

def id_generator():
    characters = string.ascii_letters + string.digits
    middle_hash = ''.join(random.choice(characters) for _ in range(10))

    now = datetime.now()
    date_part = now.strftime("%d%m%Y")
    time_part = now.strftime("%H%M%S")

    return f"{date_part}-{middle_hash}-{time_part}"

def hash_generator():
    characters = string.digits

    return ''.join(random.choice(characters) for _ in range(6))