import numpy as np
import pickle

np.errstate(over="ignore")

def sha256(n):
    
    ### Format Data for Hashing ###
    if type(n) == str:
        n = int(''.join(format(ord(i), '08b') for i in n), 2)%(2**256-1)
    if type(n) == float:
        n = int(n)
    
    data_len = int(np.ceil((len(bin(n)) - 2)/8)*8)
    target_len = int(np.ceil(data_len/512)*512)
    diff = target_len - data_len
    
    n = (n << diff) + 2**(diff-1) + data_len
    
    ### Init Hash Values ###
    primes = pickle.load(open("Math/primes.dat", "rb"))
    hash_values = np.array([int(np.sqrt(prime)%1*2**32) for prime in primes[:8]], dtype=np.uint32)
    const_values = np.array([int(np.cbrt(prime)%1*2**32) for prime in primes[:64]], dtype=np.uint32)
    
    ### Sigma Functions ###
    def rr(n, d, bit_size=32):
        return (n >> d) | (n << (bit_size - d)) & ((1 << bit_size) - 1)    
    def s0(x):
        return rr(x, 7) ^ rr(x, 18) ^ (x >> 3)
    def s1(x):
        return rr(x, 17) ^ rr(x, 19) ^ (x >> 10)
    def S0(x):
        return rr(x, 2) ^ rr(x, 13) ^ rr(x, 22)
    def S1(x):
        return rr(x, 6) ^ rr(x, 11) ^ rr(x, 25)
    def Ch(x, y, z):
        return (y & x) | (z & ~x)
    def Maj(x, y , z):
        return (x & y) | (y & z) | (z & x)
    
    ### Iterating Block ###
    blocks = [int(bin(n)[i*512+2:i*512+514], 2) for i in range(target_len//512)]
    for block in blocks:
        
        message = np.zeros(64, dtype=np.uint32)
        
        ### Message Schedule ###
        for i in range(16):
            message[i] = int(hex(block)[8*i+2:8*i+10],16)
        for i in range(16, 64):
            message[i] = s1(message[i-2])+message[i-7]+s0(message[i-15])+message[i-16]
            
        ### Hashing Message ###
        working_values = hash_values.copy()
        for i in range(64):
            T1 = working_values[7] + S1(working_values[4]) + Ch(working_values[4], working_values[5], working_values[6]) + const_values[i] + message[i]
            T2 = S0(working_values[0]) + Maj(working_values[0], working_values[1], working_values[2])
            working_values[7] = working_values[6]
            working_values[6] = working_values[5]
            working_values[5] = working_values[4]
            working_values[4] = (working_values[3] + T1)
            working_values[3] = working_values[2]
            working_values[2] = working_values[1]
            working_values[1] = working_values[0]
            working_values[0] = (T1 + T2)
        hash_values += working_values
        
    return int(''.join([format(hash_value, "08x") for hash_value in hash_values]), 16)
            
if __name__ == "__main__":
    print(hex(sha256("Hello World")))