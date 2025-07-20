import re

def user_policies(email, name, family_name, password, passphrase_clue, passphrase):
    if not re.match(r"^[a-z0-9!#$%&'*+/=?^_`{|}~.-]+@[a-z0-9.-]+\.[a-z]{2,}$", email):
        raise ValueError("Invalid email format. Example: username@example.com")

    if not re.match(r"^[A-Za-z]{2,}$", name):
        raise ValueError("Name must be at least 2 alphabetic characters.")

    if not re.match(r"^[A-Za-z]{2,}$", family_name):
        raise ValueError("Family name must be at least 2 alphabetic characters.")

    if len(password) < 8 or len(password) > 20:
        raise ValueError("Password must be 8–20 characters long.")

    if not isinstance(passphrase, list) or len(passphrase) != 4 or not all(w.isalpha() and w.islower() for w in passphrase):
        raise ValueError("Passphrase must be a list of 4 lowercase words.")

    if not re.match(r"^[a-z]{4}$", passphrase_clue):
        raise ValueError("Passphrase clue must be exactly 4 lowercase letters.")
