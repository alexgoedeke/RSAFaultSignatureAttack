#!/usr/bin/python
# created on 10.02.2016 by Alexander Goedeke

p, q, n, e, d = 593, 487, 288791, 5, 115085


def gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        k, x, y = gcd(b % a, a)
        return k, y - (b // a) * x, x


def inv(a, m):
    k, x, y = gcd(a, m)
    if k == 1:
        return x
    else:
        return 0


def power(a, b, m):
    result = 1
    for bit in "{0:b}".format(b):
        result = (result ** 2) % m
        if bit == "1":
            result = (result * a) % m
    return result


def crt(a1, a2):
    dp = d % (p - 1)
    dq = d % (q - 1)
    iq = inv(q, p) + p
    sp = power(a1, dp, p)
    sq = power(a2, dq, q)
    s = sq + q * (iq * (sp - sq) % p)
    return s


def sig(h):
    return crt(h, h)


def fsig(h):
    return crt(h, h + 1)


def main():
    h = int(input("plaintext: "))
    s1 = sig(h)
    s2 = fsig(h)

    print "sig(" + str(h) + ") = " + str(s1)
    print "fsig(" + str(h) + ") = " + str(s2)

    p1, p2, p3 = gcd(n, s1 - s2)
    if p1 == p:
        print "found private key: ("+str(p1)+", "+str(n/p1)+")"

    return 0


main()