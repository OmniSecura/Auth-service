import re
# from zxcvbn import zxcvbn # for password strength estimation

COMMON_PASSWORDS = {
    "password", "123456", "qwerty", "letmein", "abc123"
}

SPECIAL_CHARACTERS = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~")


def user_policies(email, name, family_name, password, passphrase):
    # Email validation
    if not re.match(r"^[a-z0-9!#$%&'*+/=?^_`{|}~.-]+@[a-z0-9.-]+\.[a-z]{2,50}$", email):
        raise ValueError("Invalid email format. Example: username@example.com")

    # Name and family name validation
    if not re.match(r"^[A-Za-z]{2,30}$", name):
        raise ValueError("Name must be at least 2 alphabetic characters.")
    if not re.match(r"^[A-Za-z]{2,30}$", family_name):
        raise ValueError("Family name must be at least 2 alphabetic characters.")

    # Password length
    if len(password) < 10 or len(password) > 64:
        raise ValueError("Password must be between 10 and 64 characters long.")

    # Password complexity checks
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must include at least one lowercase letter.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must include at least one uppercase letter.")
    if not re.search(r"\d", password):
        raise ValueError("Password must include at least one digit.")
    if not any(ch in SPECIAL_CHARACTERS for ch in password):
        raise ValueError("Password must include at least one special character: " + ''.join(SPECIAL_CHARACTERS))

    # Disallow common passwords
    if password.lower() in COMMON_PASSWORDS:
        raise ValueError("Password is too common; choose a more unique password.")

    # Disallow sequences and repeated characters
    if re.search(r"(.)\1{2,}", password):
        raise ValueError("Password must not contain sequences of the same character more than twice.")
    if any(seq in password.lower() for seq in ["1234", "abcd", "qwer"]):
        raise ValueError("Password must not contain common sequences.")

    # Prevent use of personal info in password
    lowered = password.lower()
    for term in (email, name, family_name):
        if term.lower() in lowered:
            raise ValueError("Password must not contain parts of your personal information.")

    # Password strength estimation using zxcvbn
    # strength = zxcvbn(password)
    # if strength['score'] < 3:
    #     raise ValueError("Password is too weak. Try combining unrelated words to increase entropy.")

    # Passphrase validation
    if not isinstance(passphrase, list) or len(passphrase) != 4 or not all(w.isalpha() and w.islower() for w in passphrase):
        raise ValueError("Passphrase must be a list of 4 lowercase words.")
