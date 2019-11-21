import random

from app.model.signature import *
from app.model.edwards25519 import *
from app.model.utils import *
from app.model import receiver

# create_key create 128 bits entropy
def create_entropy():
    entropy = random.randint(0, 2**128)
    entropy_str = entropy.to_bytes(16, byteorder='big').hex()
    return {
        "entropy": entropy_str
    }
