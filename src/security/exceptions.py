import re
from zxcvbn import zxcvbn  # for password strength estimation
from src.routers.v1.websockets import manager

COMMON_PASSWORDS = {
    "password", "123456", "qwerty", "letmein", "abc123"
}

SPECIAL_CHARACTERS = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~")


async def user_policies(email, name, family_name, password, passphrase=None):
    # Email validation
    if not re.match(r"^[a-z0-9!#$%&'*+/=?^_`{|}~.-]+@[a-z0-9.-]+\.[a-z]{2,50}$", email):
        await manager.send_personal_message("Invalid email format. Example: username@example.com", email)
        raise ValueError("Invalid email format. Example: username@example.com")

    # Name and family name validation
    if not re.match(r"^[A-Za-z]{2,30}$", name):
        await manager.send_personal_message("Name must be at least 2 alphabetic characters.", email)
        raise ValueError("Name must be at least 2 alphabetic characters.")
    if not re.match(r"^[A-Za-z]{2,30}$", family_name):
        await manager.send_personal_message("Family name must be at least 2 alphabetic characters.", email)
        raise ValueError("Family name must be at least 2 alphabetic characters.")

    # Password length
    if len(password) < 10 or len(password) > 64:
        await manager.send_personal_message("Password must be between 10 and 64 characters long.", email)
        raise ValueError("Password must be between 10 and 64 characters long.")

    # Password complexity checks
    if not re.search(r"[a-z]", password):
        await manager.send_personal_message("Password must include at least one lowercase letter.", email)
        raise ValueError("Password must include at least one lowercase letter.")
    if not re.search(r"[A-Z]", password):
        await manager.send_personal_message("Password must include at least one uppercase letter.", email)
        raise ValueError("Password must include at least one uppercase letter.")
    if not re.search(r"\d", password):
        await manager.send_personal_message("Password must include at least one digit.", email)
        raise ValueError("Password must include at least one digit.")
    if not any(ch in SPECIAL_CHARACTERS for ch in password):
        await manager.send_personal_message(
            "Password must include at least one special character: " + ''.join(SPECIAL_CHARACTERS),
            email,
        )
        raise ValueError("Password must include at least one special character: " + ''.join(SPECIAL_CHARACTERS))

    # Disallow common passwords
    if password.lower() in COMMON_PASSWORDS:
        await manager.send_personal_message("Password is too common; choose a more unique password.", email)
        raise ValueError("Password is too common; choose a more unique password.")

    # Disallow sequences and repeated characters
    if re.search(r"(.)\1{2,}", password):
        await manager.send_personal_message("Password must not contain sequences of the same character more than twice.", email)
        raise ValueError("Password must not contain sequences of the same character more than twice.")
    if any(seq in password.lower() for seq in ["1234", "abcd", "qwer"]):
        await manager.send_personal_message("Password must not contain common sequences.", email)
        raise ValueError("Password must not contain common sequences.")

    # Prevent use of personal info in password
    lowered = password.lower()
    for term in (email, name, family_name):
        if term.lower() in lowered:
            await manager.send_personal_message("Password must not contain parts of your personal information.", email)
            raise ValueError("Password must not contain parts of your personal information.")

    # Password strength estimation using zxcvbn
    strength = zxcvbn(password)
    if strength['score'] < 3:
        await manager.send_personal_message(
            "Password is too weak. Try combining unrelated words to increase entropy.",
            email,
        )
        raise ValueError("Password is too weak. Try combining unrelated words to increase entropy.")

    # Passphrase validation
    if passphrase is not None:
        if (
            not isinstance(passphrase, list)
            or len(passphrase) != 4
            or not all(w.isalpha() and w.islower() for w in passphrase)
        ):
            await manager.send_personal_message("Passphrase must be a list of 4 lowercase words.", email)
            raise ValueError("Passphrase must be a list of 4 lowercase words.")
