import secrets

def genPrime(bytes : int):
    while True:
        a = int.from_bytes(secrets.token_bytes(bytes)) | 2**(bytes*8-1) + 1
        if miller_rabin(a): return a
    
def single_test(n, a):
    exp = n - 1
    while not exp & 1:
        exp >>= 1
        
    if pow(a, exp, n) == 1:
        return True
    
    while exp < n - 1:
        if pow(a, exp, n) == n - 1:
            return True
        exp <<= 1
    
    return False

def miller_rabin(n, k=40):
    for _ in range(k):
        a = secrets.randbelow(n-4)+2
        assert a < (n - 1), f"{a}"
        if not single_test(n, a):
            return False
    return True

if __name__ == "__main__":
    print(genPrime(64))