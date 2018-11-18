def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''
    for ch in plaintext:
        num = ord(ch)
        if 97 <= num <= 122 or 65 <= num <= 90:
            code = num + 3
            if 90 < code < 97 or code > 122:
                code -= 26
            ciphertext += chr(code)
        else:
            ciphertext += ch
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ''
    for ch in ciphertext:
        num = ord(ch)
        if 97 <= num <= 122 or 65 <= num <= 90:
            code = num - 3
            if 97 > code > 90 or code < 65:
                code += 26
            plaintext += chr(code)
        else:
            plaintext += ch
    return plaintext
