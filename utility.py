import hmac

SECRET = "jksjdjk8s99098jhdakjfhb*7&jhakjd"


def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val


def hash_str(s):
    """
        This is the method that hashes the password to a random
        string
        :param The password in plain text
        :return Hashed password
    """
    return hmac.new(SECRET, s).hexdigest()
