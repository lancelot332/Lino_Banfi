import redis
import math

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def connect_to_redis():
    return redis.StrictRedis(
        host="localhost",
        port=6379,
        username="default",
        password="ODAzyiCudM%",
        decode_responses=True 
    )

def main():
    r = connect_to_redis()

    primes = generate_primes(1000)

    for idx, prime in enumerate(primes, start=1):
        key = f"prime:{idx}" 
        r.set(key, prime)    
        print(f"SET {key} -> {prime}")

    for idx in range(1, 1001):
        key = f"prime:{idx}"
        value = r.get(key)
        print(f"GET {key} -> {value}")

if __name__ == "__main__":
    main()
