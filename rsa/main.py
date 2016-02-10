#!/usr/bin/python
# created on 10.02.2016 by Alexander Goedeke

from random import randint

# use test values for RSA
p, q, n, e, d = 593, 487, 288791, 5, 115085


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
    # read plaintext
    h = int(input("plaintext: "))

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
        print "found private key: (" + str(p1) + ", " + str(n / p1) + ")"

    return 0


main()
