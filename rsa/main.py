#!/usr/bin/python
# created on 10.02.2016 by Alexander Goedeke

from random import randint
import os

# use test values for RSA
p, q, n, e, d = 11, 13, 143, 23, 47
HEX = 1


# read private key file (a=1: generate new openssl rsa key)
def generateKey(a):
    if a == 1:
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

    n = int(text[i_n + 7: i_e].translate(None, ': \n'), 16)
    e = int(text[i_e + 16: i_e + 21])
    d = int(text[i_d + 15: i_p].translate(None, ': \n'), 16)
    p = int(text[i_p + 6: i_q].translate(None, ': \n'), 16)
    q = int(text[i_q + 6: i_end].translate(None, ': \n'), 16)

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
    for bit in bin(b)[2:]:
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
    i = bin(h)[2:]
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


sig_ok = 0
sig_fault = 0
h = 0


def main():
    while 1:
        print "\n--------------------------------------------------- MENU ---------------------------------------------------"
        i = input("(1) generate signature, (2) generate fault signature, (3) do fault attack, (4) generate real key, (5) exit: ")
        print "------------------------------------------------------------------------------------------------------------\n"
        global sig_ok
        global sig_fault
        global h

        if i == 1:
            print "\n-------------------------------------------- generate signature --------------------------------------------"
            h = input("message: ")
            sig_ok = sig(h)

            if HEX == 1:
                print "signature: " + str(hex(sig_ok))
            else:
                print "signature: " + str(sig_ok)
            print "------------------------------------------------------------------------------------------------------------\n"
        elif i == 2:
            print "\n----------------------------------------- generate fault signature -----------------------------------------"
            h = input("message: ")
            sig_fault = fsig(h)
            if HEX == 1:
                print "signature: " + str(hex(sig_fault))
            else:
                print "signature: " + str(sig_fault)
            print "------------------------------------------------------------------------------------------------------------\n"
        elif i == 3:
            print "\n---------------------------------------------- do fault attack ---------------------------------------------"
            i2 = input("(1) knows s and sf, (2) known sf and h: ")
            if i2 == 1:
                if (sig_ok != 0) & (sig_fault != 0):
                    p1, p2, p3 = gcd(n, sig_ok - sig_fault)
                    if p1 == p:
                        if HEX == 1:
                            print "found private key: (" + str(hex(p1)) + ", " + str(hex(n / p1)) + ")"
                        else:
                            print "found private key: (" + str(p1) + ", " + str(n / p1) + ")"
                    else:
                        print "no private key computed :("
                else:
                    print "not enough data"
            elif i2 == 2:
                if (h != 0) & (sig_fault != 0):
                    p1, p2, p3 = gcd(n, power(sig_fault, e, n) - h)
                    if p1 == p:
                        if HEX == 1:
                            print "found private key: (" + str(hex(p1)) + ", " + str(hex(n / p1)) + ")"
                        else:
                            print "found private key: (" + str(p1) + ", " + str(n / p1) + ")"
                    else:
                        print "no private key computed :("
                else:
                    print "not enough data"
            print "------------------------------------------------------------------------------------------------------------\n"
        elif i == 4:
            print "\n--------------------------------------------- generate real key --------------------------------------------"
            i4 = input("(1) use old files, (2) generate new: ")
            if 1 <= i4 <= 2:
                generateKey(i4-1)
            print "------------------------------------------------------------------------------------------------------------\n"
        else:
            exit(0)
main()