import rsa.rsa as rsa
from controllers.common import write_to_file
from flask import render_template





def render_encrypt_file(file, params):
    text = file.read().decode('utf-8-sig')
    return render_encrypt_text(text, params)


def render_encrypt_text(text, params):
    params = tuple(int(param) for param in params)
    encrypted = rsa.encrypt(text, params)
    p, q, e = params
    n, phi = rsa._get_n(p, q), rsa._get_phi(p, q)
    decrypted = rsa.decrypt(encrypted, n, rsa._get_private_key(phi, e))
    write_to_file(decrypted, 'output.txt')
    return render_template('rsa.html')