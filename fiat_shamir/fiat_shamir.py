import random


def get_parameters(p, q):
    n = p * q
    r = random.randint(1, n - 1)
    x = pow(r, 2, n)
    return n, r, x


def get_key(n, s):
    return pow(s, 2, n)


def get_verification_metrics(n, r, s, v, x):
    e = random.choice([0, 1])
    y = r * pow(s, e) % n
    y2 = pow(y, 2, n)
    xv = x * v % n
    return y2, xv, e


def verify(n, r, s, v, x):
    y2, xv, e = get_verification_metrics(n, r, s, v, x)
    if e == 0:
        return y2 == x
    elif e == 1:
        return y2 == xv