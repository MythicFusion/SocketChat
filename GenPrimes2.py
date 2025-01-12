import pickle
import numpy as np

def primes(n):
    x = np.ones((n+1,), dtype=np.bool_)
    x[0] = False
    x[1] = False
    for i in range(2, int(n**0.5)+1):
        if x[i]:
            print(i, end="\r")
            x[2*i::i] = False

    primes = np.where(x == True)[0]
    print(primes[-1])
    return primes

if __name__ == "__main__":
    prime_numbers = primes(2**30-1)
    print(len(prime_numbers))
    with open("primes.dat", "wb") as prime_data:
        pickle.dump(prime_numbers, prime_data)