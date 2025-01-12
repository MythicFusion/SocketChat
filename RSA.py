from Math.MillerRabin import genPrime
from Math.ExtendedEular import eGDC
import secrets

def GDC(a, b):
    while b:
        a, b = b, a % b
    return a

def GenKeyPair():
    P = genPrime(16)
    Q = genPrime(16)
    
    N = P * Q
    U = (P - 1) * (Q - 1)
    
    e = secrets.randbelow(U - 2**32) + 2**32
    while GDC(e, U) != 1:
        e = secrets.randbelow(U - 2**32) + 2**32
        
    d = eGDC(e, U)[0]
    while d<0: d+=U
    
    assert pow(15, e*d, N) == 15
    
    return e, d, N

if __name__ == "__main__":
    e, d, N = GenKeyPair("Hello World")