import numpy as np

class GaloisField:
    def __init__(self, x):
        assert x < 2**8
        self.x = x
        self.primative = 283 #285

    def __add__(self, other : "GaloisField"):
        return GaloisField(self.x ^ other.x)
    
    def __sub__(self, other : "GaloisField"):
        return GaloisField(self.x ^ other.x)
    
    def __mul__(self, other : "GaloisField"):
        a = self.x
        b = other.x
        sum = 0
        while b:
            if b%2:
               sum ^= a
            b >>= 1
            a <<= 1
            if a >= 2**8:
                a ^= self.primative
        return GaloisField(sum)
    
    def __rmul__(self, other : int):
        a = self.x
        b = other
        sum = 0
        while b:
            if b%2:
               sum ^= a
            b >>= 1
            a <<= 1
            if a >= 2**8:
                a ^= self.primative
        return GaloisField(sum)
    
    def __truediv__(self, other : "GaloisField"):
        raise NotImplementedError
    
    def __mod__(self, other : "GaloisField"):
        raise NotImplementedError

    def __floordiv__(self, other : "GaloisField"):
        raise NotImplementedError
    
    def __pow__(self, other : "GaloisField"):
        raise NotImplementedError
    
    def __int__(self):
        return self.x
        
    def __repr__(self):
        return format(self.x, "02x")
    
if __name__ == "__main__":
    GaloisField(5, 6)