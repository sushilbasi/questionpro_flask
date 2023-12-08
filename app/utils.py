import secrets


def generate_unique_hex():
    # Generate a 24-bit random number and convert it to a 6-digit hexadecimal string
    unique_hex = secrets.token_hex(3)
    return unique_hex
