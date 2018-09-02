from flask import render_template
from fiat_shamir.fiat_shamir import verify_and_write_log


def render_proove(secret, p, q, n_accreditations):
    verify_and_write_log(p, q, secret, n_accreditations)
    with open('log') as file:
        log = file.read()
    return render_template('fiat_shamir.html', output=log, p=p, q=q, s=secret, t=n_accreditations)