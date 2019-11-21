import random

# create_key create 128 bits entropy
def create_entropy():
    entropy = random.randint(0, 2**128)
    entropy_str = entropy.to_bytes(16, byteorder='big').hex()
    return {
        "entropy": entropy_str
    }
