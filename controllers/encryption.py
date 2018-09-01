import rsa.rsa as rsa
from controllers.common import write_to_file
from flask import render_template


def get_template_params(text, encrypted, decrypted, p, q, e):
    return {
        'initial_text': text,
        'encrypted_text': encrypted,
        'decrypted_text': decrypted,
        'p': str(p),
        'q': str(q),
        'e': str(e),
    }


def render_encrypt_file(file, params):
    text = file.read().decode('utf-8-sig')
    return render_encrypt_text(text, params)


def render_encrypt_text(text, params):
    params = tuple(int(param) for param in params)

    p, q, e = params
    n, phi = rsa._get_n(p, q), rsa._get_phi(p, q)
    encrypted = rsa.encrypt(text, (n, phi, e))
    decrypted = rsa.decrypt(encrypted, n, rsa._get_private_key(phi, e))

    write_to_file(decrypted, 'output.txt')

    template_params = get_template_params(text, encrypted, decrypted, p, q, e)
    return render_template('rsa.html', **template_params)