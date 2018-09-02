import random
from functools import partial


log = print


class Sender:
    def __init__(self, secret):
        self._secret = secret

    def update_random_num(self, product):
        self._random_num = random.randrange(1, product)
        log("Sender:\t\trandom number r = {}".format(self._random_num))

    def get_public_key(self, product):
        pubkey = pow(self._secret, 2, product)
        log('Sender:\t\tpublic key v = s ** 2 (mod n) = {} ** 2 (mod {}) = {}'.format(self._secret, product, pubkey))
        log()
        return pubkey

    def get_x(self, product):
        x = pow(self._random_num, 2, product)
        log('Sender:\t\tx = r ** 2 (mod n) = {} ** 2 (mod {}) = {}'.format(self._random_num, product, x))
        return x

    def get_answer(self, random_bit, product):
        answer = self._random_num * self._secret**random_bit % product
        log('Sender:\t\tr * s ** e (mod n) = {} * {} ** {} (mod {}) = {}'.format(
                self._random_num, self._secret, random_bit, product, answer
            )
        )
        return answer


class Verifier:
    def __init__(self, p, q):
        self._p = p
        self._q = q
        self.product = p * q
        log('Verifier:\tn = p*q = {} * {} = {}'.format(p, q, self.product))

    def update_random_bit(self):
        self.random_bit = random.choice([0, 1])
        log('Verifier:\trandom bit e = {}'.format(self.random_bit))

    def verify_answer(self, x, answer, pubkey):
        verifier_result = pow(answer, 2, self.product)
        log('Verifier:\tmy result is {} ** 2 (mod {}) = {}'.format(answer, self.product, verifier_result))

        if self.random_bit == 1:
            new_x = x * pubkey % self.product
            log('Verifier:\tx*v (mod n) = {} * {} (mod {}) = {}'.format(
                    x, pubkey, self.product, new_x
                )
            )
            x = new_x

        if x == verifier_result:
            log('Verifier:\tboth numbers are {}'.format(x))
            log('Verifier:\tverification OK')
        return x == verifier_result


def verify(verifier, sender, n_accreditations):
    pubkey = sender.get_public_key(verifier.product)

    ok_verifications = 0
    for i in range(n_accreditations):
        log('[Accreditation {}/{}]'.format(i + 1, n_accreditations))
        sender.update_random_num(verifier.product)
        x = sender.get_x(verifier.product)
        verifier.update_random_bit()
        answer = sender.get_answer(verifier.random_bit, verifier.product)
        if verifier.verify_answer(x, answer, pubkey) == True:
            ok_verifications += 1
        log()
    log('{}/{} passed OK'.format(ok_verifications, n_accreditations))


def init_logger(path='log'):
    logfile = open(path, 'w')
    global log
    log = partial(print, file=logfile)
    return logfile


def close_logger(logfile):
    logfile.close()


def verify_and_write_log(p, q, secret, n_accreditations):
    f = init_logger()
    try:
        verifier = Verifier(p, q)
        sender = Sender(secret)
        verify(verifier, sender, n_accreditations)
    finally:
        close_logger(f)

