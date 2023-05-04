#! /usr/bin/env python3
# Carey Hutchens m232850

import sage.all
from sage.rings.finite_rings.finite_field_constructor import GF
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
# from sage.misc.functional import log as exact_log
# from sage.functions.other import ceil as exact_ceil

p = 2**256 - 189
field256189 = GF(p)

def bytes_to_GF(data):
    """Convert a bytes object to a finite field element."""
    x = int.from_bytes(data, byteorder='big')
    assert x < p
    return field256189(x)

def GF_to_bytes(elt):
    """Convert a finite field element to a bytes object."""
    return int(elt).to_bytes(length=32, byteorder='big')

# Given a list of x and y coordinates, return a polynomial
# that interpolates those points
def interp(xs, ys):
    field_xs = list(map(bytes_to_GF, xs))
    field_ys = list(map(bytes_to_GF, ys))
    ring = PolynomialRing(field256189, 'x')
    return ring.lagrange_polynomial(zip(field_xs,field_ys))

# Given a list of coefficients, make a polynomial
def reform_poly(coef):
    ring = PolynomialRing(field256189, 'x')
    return ring(coef)

# Given an element, polynomial, and block cipher, eval a poly element
def eval(poly, e, cipher):
    return int.from_bytes((cipher.encrypt(GF_to_bytes(poly(bytes_to_GF(e))))),'big')

