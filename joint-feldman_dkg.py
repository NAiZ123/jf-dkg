from __future__ import division
from __future__ import print_function
import random
import math
import time
import sympy
from random import randrange
from hashlib import sha1
from gmpy2 import xmpz, to_binary, invert, powmod, is_prime


def generate_p_q(L, N):
    g = N  # g >= 160
    n = (L - 1) // g
    b = (L - 1) % g
    while True:
        # generate q
        while True:
            s = xmpz(randrange(1, 2 ** (g)))
            a = sha1(to_binary(s)).hexdigest()
            zz = xmpz((s + 1) % (2 ** g))
            z = sha1(to_binary(zz)).hexdigest()
            U = int(a, 16) ^ int(z, 16)
            mask = 2 ** (N - 1) + 1
            q = U | mask
            if is_prime(q, 20):
                break
        # generate p
        i = 0  # counter
        j = 2  # offset
        while i < 4096:
            V = []
            for k in range(n + 1):
                arg = xmpz((s + j + k) % (2 ** g))
                zzv = sha1(to_binary(arg)).hexdigest()
                V.append(int(zzv, 16))
            W = 0
            for qq in range(0, n):
                W += V[qq] * 2 ** (160 * qq)
            W += (V[n] % 2 ** b) * 2 ** (160 * n)
            X = W + 2 ** (L - 1)
            c = X % (2 * q)
            p = X - c + 1  # p = X - (c - 1)
            if p >= 2 ** (L - 1):
                if is_prime(p, 10):
                    return p, q
            i += 1
            j += n + 1

def generate_g(p, q):
    while True:
        h = randrange(2, p - 1)
        exp = xmpz((p - 1) // q)
        g = powmod(h, exp, p)
        if g > 1:
            break
    return g


def power_mod(n,k,p):
    result = 1
    while k > 0:
        if (k&1) == 1:
            result = (result * n) % p
        n = n * n % p
        k >>= 1

    return result

def _extended_gcd(a, b):
    """
    Division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1) this can
    be computed via extended Euclidean algorithm
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
    """
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y


def _divmod(num, den, p):
    """Compute num / den modulo prime p
    To explain what this means, the return value will be such that
    the following is true: den * _divmod(num, den, p) % p == num
    """
    inv, _ = _extended_gcd(den, p)
    return num * inv


def _lagrange_interpolate(x, x_s, y_s, p):
    """
    Find the y-value for the given x, given n (x, y) points;
    k points will define a polynomial of up to kth order.
    """
    k = len(x_s)
    assert k == len(set(x_s)), "points must be distinct"

    def PI(vals):  # upper-case PI -- product of inputs
        accum = 1
        for v in vals:
            accum *= v
        return accum

    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
    den = PI(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p)
               for i in range(k)])
    return (_divmod(num, den, p) + p) % p


def recover_secret(shares, q):
    """
    Recover the secret from share points
    (x, y points on the polynomial).
    """
    if len(shares) < 2:
        raise ValueError("need at least two shares")
    x_s, y_s = zip(*shares)
    return _lagrange_interpolate(0, x_s, y_s, q)


def isprime(n):
    if n == 2:
        return True
    if n == 1 or n % 2 == 0:
        return False
    i = 3
    while i <= math.sqrt(n):
        if n % i == 0:
            return False
        i = i + 2
    return True


def Verifi(broadcastcommit, n, k, p, g, share, id):
    gshare = [0] * n
    Veri = [0] * n

    # もう一つfor文？
    for i in range(0, n):
        if i != id:
            gshare[i] = power_mod(g, share[i][id], p)  # OK
            for j in range(0, k):
                if j == 0:
                    Veri[i] = broadcastcommit[i][j] % p
                else:
                    tmp = (id + 1) ** j
                    Veri[i] *= power_mod(broadcastcommit[i][j],tmp,p)

        Veri[i] %= p

    print("\ng^share[] : " + str(gshare))
    print("Veri[]    : " + str(Veri))

    if Veri == gshare:
        return "True"
    else:
        return "Complain"


def polynomial(p, q, k, share, id):
    a = []  # Secret taken from the group Z_q* 集合Z_q*から取られた秘密値
    while True:
        a.append(sympy.randprime(3, q))
        #a.append(secrets.choice(Z_p_star))
        # a.append(secrets.randbelow(q))
        if a[0] >= 1 or a[0] <= q:
            break

    a[0] %= q
    print("id : " + str(id))
    print("secret z :" + str(a[0]))

    for i in range(1, k):
        a.append(random.randint(1, q))

    print("a[] : ")
    print(a)

    # share = [0] * n

    for i in range(0, n):
        share[id][i] = a[0]
        for j in range(1, k):
            share[id][i] += (a[j] * ((i + 1) ** j))

    for i in range(0, n):
        share[id][i] %= q

    print("\nshare[] : ")
    print(share)

    commitment = [0] * k

    for i in range(0, k):
        commitment[i] = (pow(g, a[i], p))  # commitment[i] = ((g**a[i]) % p)

    print("commitment[] : ")
    print(commitment)
    print("______________________________________________")

    return share, commitment, a[0]


def join(share, n, q):
    x = [[0] * 2 for i in range(n)]
    for i in range(0, n):
        x[i][0] = i + 1
        for j in range(0, n):
            x[i][1] += share[j][i]

    for i in range(0, n):
        x[i][1] %= q

    return x


def pubcommitment(broadcastcommit):
    pubcom = [1] * n
    for i in range(0, n):
        for j in range(0, k):
            pubcom[i] = broadcastcommit[i][j]
        pubcom[i] %= p

    return pubcom


if __name__ == '__main__':
    while True:
        k = int(input("k = "))
        n = int(input("n = "))

        if k > 0 and n > 0:
            if k <= n:
                break
            else:
                print("please k <= n ")
        else:
            print("k,n is positive")

    q = sympy.randprime(3, int('FFFFFF', 16))
    #while True:
        #q = int(input("Insert a prime q : "))

        #if isprime(q):
        #    break

    broadcastcommit = [[0] * k for i in range(n)]

    start = time.time()
    xx = 0

    N = 160
    L = 1024
    p,q = generate_p_q(L, N)
    g = generate_g(p, q)

    print("q : " + str(q))
    print("p : " + str(p))
    print("g : " + str(g))

    # 　各個人のシェア、コミットメント生成
    sp = [[0] * n for i in range(n)]  # [send_id, share, my_id]

    for i in range(0, n):
        share, commitment, z0 = polynomial(p, q, k, sp, i)
        xx += z0
        for j in range(0, k):
            broadcastcommit[i][j] = commitment[j]

    print("broadcastcommit : ")
    print(broadcastcommit)

    print("shar secret x = (" + str(xx % q) + ")")

    # シェアの検証 (改造の必要あり)
    for i in range(0, n):
        judg = Verifi(broadcastcommit, n, k, p, g, share, i)
        print("id:" + str(i))
        print(judg)

    # 　シェアの結合
    x = join(share, n, q)
    # 公開鍵yの計算
    y = 1
    for i in range(0, n):
        y *= broadcastcommit[i][0]

    CCC = y
    y %= p
    print('\ndkg share  x :', *x)
    print('dkg public y :', y)

    elapsed_time = time.time() - start
    print("\nelapsed_time:{0}".format(elapsed_time) + "[sec]")

    pubc = pubcommitment(broadcastcommit)
    print("\npublic commitment : " + str(pubc))

    pool = random.sample(x, k)
    print('\nCombining shares:', *pool)

    print('Secret recovered from minimum subset of shares:             ',
          recover_secret(pool, q))
    print('Secret recovered from a different minimum subset of shares: ',
          recover_secret(pool, q))

    if  (xx % q) == recover_secret(pool, q):
        print("True")
    else:
        print("False")

    print("size CCC : " + str(len(CCC)) + "bit")
