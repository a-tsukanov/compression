def _get_n(p, q):
    return p * q


def _get_phi(p, q):
    return (p-1) * (q-1)


def _get_private_key(phi, e):

    def euclid(a, b, c, d):
        if c == 1:
            key = d
            return key
        else:
            new_c = a - ((a // c) * c)
            new_d = (b - (d * (a // c))) % phi
            return euclid(c, d, new_c, new_d)

    return euclid(phi, phi, e, 1)


def encrypt(text, params):
    n, phi, e = params
    lst = []
    for c in text:
        encrypted_char = pow(ord(c), e, n)
        lst.append(encrypted_char)
    return ' '.join([str(value) for value in lst])


def decrypt(encrypted, n, private_key):
    rv = ''
    for item in encrypted.split(' '):
        code = pow(int(item), private_key, n)
        char = chr(code)
        rv += char
    return rv


p, q, e = (107, 397, 17)
n, phi = _get_n(p, q), _get_phi(p, q)

enc = encrypt('hello', (n, phi, e))
print(decrypt(enc, n, _get_private_key(phi, e)))
