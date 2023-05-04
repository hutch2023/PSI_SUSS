#!/usr/bin/python3
# Carey Hutchens m232850

import random as rd
import sage.all
from sage.rings.finite_rings.finite_field_constructor import GF
from sage.schemes.elliptic_curves.constructor import EllipticCurve

from elligator import fe
from elligator import curve_to_hash
from elligator import hash_to_curve
from elligator import can_curve_to_hash

# converting montgomery points to weierstrass points
def to_weierstrass(A, B, x, y):
    return (x/B + A/(3*B), y/B)

# converting weierstrass points to montgomery points
def to_montgomery(A, B, u, v):
    return (B * (u - A/(3*B)), B*v)

# Curve over finite field 2^255 - 19
class Curve25519:

    # Define curve 25519
    def __init__(self):
        # parameters in montgomery
        self.p = 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed
        self.q = 0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed * 0x08
        self.gx = 0x09
        self.gy = 0x20ae19a1b8a086b4e01edd2c7748d14c923d4d7e6d7c61b229e9c5a27eced3d9
        self.a = 0x76d06
        self.b = 0x01

        # convert and initialize in weierstrass
        self.field = GF(self.p)
        self.A = self.field(self.a)
        self.B = self.field(self.b)
        self.curve = EllipticCurve(self.field, ((3 - self.A**2)/(3 * self.B**2), (2 * self.A**3 - 9 * self.A)/(27 * self.B**3)))
        self.g = self.curve(*to_weierstrass(self.A, self.B, self.field(self.gx), self.field(self.gy)))
        self.curve.set_order(self.q)
    
    # Generate a secret ECDHKA key
    def pKey(self):
        return rd.randint(1,self.q - 1)

    # Generate a public ECDHKA message
    def pMsg(self, key):
        return self.g * key

    # Return a ECDHKA secret and its public message
    # This point must be encodable using elligator!
    def secretAndMessage(self):
        while(True):
            k = self.pKey()
            w_point = self.pMsg(k)
            m_point = to_montgomery(self.A, self.B, w_point.xy()[0], w_point.xy()[1])
            u = fe(int(m_point[0]))
            if(can_curve_to_hash(u)):
                return k, self.enc(w_point)

    # Take an EC point and encode it using elligator
    def enc(self, w_point):
        m_point = to_montgomery(self.A, self.B, w_point.xy()[0], w_point.xy()[1])
        v_neg = int(m_point[1]) > 0 
        u = fe(int(m_point[0]))
        return curve_to_hash(u,v_neg)

    # Take a pseudo-random string and decode it to an EC point using elligator
    def dec(self, r):
        u, v = hash_to_curve(fe(r))
        return self.curve(*to_weierstrass(self.A, self.B, self.field(u.val), self.field(v.val)))
        
    # Return the ECDHKA shared key
    def sKey(self, key, msg, hash):
        msg = self.dec(msg)
        x = int((msg * key).xy()[0])
        return hash(x.to_bytes(32,"big")).digest()


