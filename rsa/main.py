#!/usr/bin/python
# created on 10.02.2016 by Alexander Goedeke

from random import randint
import os

# use test values for RSA
#p, q, n, e, d = 593, 487, 288791, 5, 115085
p, q, n, e, d = 0, 0, 0, 0, 0

# read private key file (a=1: generate new openssl rsa key)
def generateKey(a):
    if a==1:
        os.system("openssl genrsa -out private.key")
        os.system("openssl rsa -in private.key -text > private.txt")

    global p, q, n, e, d

    f = open('private.txt', 'r')
    text = f.read()

    i_n = text.find("modulus")
    i_e = text.find("publicExponent")
    i_d = text.find("privateExponent")
    i_p = text.find("prime1")
    i_q = text.find("prime2")
    i_end = text.find("exponent1")

    n = int(text[ i_n + 7: i_e].translate(None, ': \n'), 16)
    e = int(text[ i_e + 16: i_e+21])
    d = int(text[ i_d + 15: i_p].translate(None, ': \n'), 16)
    p = int(text[ i_p + 6: i_q].translate(None, ': \n'), 16)
    q = int(text[ i_q + 6: i_end].translate(None, ': \n'), 16)

    f.close()


# greatest common divisor of a and b (euclidean algorithm)
def gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        k, x, y = gcd(b % a, a)
        return k, y - (b // a) * x, x


# a^-1 mod m
def inv(a, m):
    k, x, y = gcd(a, m)
    if k == 1:
        return x
    else:
        return 0


# a^b mod m
def power(a, b, m):
    result = 1
    for bit in "{0:b}".format(b):
        result = (result ** 2) % m
        if bit == "1":
            result = (result * a) % m
    return result


# chinese remainder theorem
def crt(a1, a2):
    dp = d % (p - 1)
    dq = d % (q - 1)
    iq = inv(q, p)
    sp = power(a1, dp, p)
    sq = power(a2, dq, q)
    s = sq + q * (iq * (sp - sq) % p)
    return s


# sign h correct
def sig(h):
    return crt(h, h)


# bitflip
def bitflip(h):
    i = "{0:b}".format(h)
    li = list(i)
    k = randint(0, len(i) - 1)
    if li[k] == '0':
        li[k] = '1'
    else:
        li[k] = '0'
    return int(''.join(li), 2)


# sign h with an bit manipulation
def fsig(h):
    return crt(h, bitflip(h))


def main():
    generateKey(0)

    # read plaintext dec
    h = int(input("plaintext: "))

    # read plaintext hex
    # h = int(input("plaintext: "), 16)

    # generate signatures
    s1 = sig(h)
    s2 = fsig(h)

    # print signatures
    print "sig(" + str(h) + ") = " + str(s1)
    print "fsig(" + str(h) + ") = " + str(s2)

    # do the fault signature attack
    # we know that s1 is an correct and s2 an incorrect signature
    p1, p2, p3 = gcd(n, s1 - s2)
    if p1 == p:
        print "found private key (1): (" + str(p1) + ", " + str(n / p1) + ")"

    p1, p2, p3 = gcd(n, power(s2, e, n) - h)
    if p1 == p:
        print "found private key (2): (" + str(p1) + ", " + str(n / p1) + ")"

    return 0


main()
