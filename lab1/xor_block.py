def xor_block(message_block: bytes, key: bytes) -> bytes:
    return bytes([a ^ b for a, b in zip(message_block, key)])

def encrypt(message: bytes, key: bytes) -> bytes:
    cipher_text = b''

    for i in range(0, len(message), 16):
        message_block = message[i:i+16]
        cipher_text += xor_block(message_block, key * (len(message_block)//len(key)))

    return cipher_text

def decrypt(cipher_text: bytes, key: bytes) -> bytes:
    decrypted_text = b''

    for i in range(0, len(cipher_text), 16):
        cipher_block = cipher_text[i:i+16]
        decrypted_text += xor_block(cipher_block, key * (len(cipher_block)//len(key)))

    return decrypted_text

def find_first_byte(cipher_text: bytes):
    for i in range(256):
        msg = decrypt(cipher_text, bytes([i, i]))
        try:
            print(f"i: {i}, message: {msg.decode("utf8")}")
        except:
            pass

def find_second_byte(cipher_text: bytes, first_byte: int):
    for i in range(256):
        msg = decrypt(cipher_text, bytes([first_byte, i]))
        try:
            print(f"i: {i}, message: {msg.decode("utf8")}")
        except:
            pass


encrypted_msg = b'\x12\'&73#/! b$/a\x01./175#"#.bsrsvns'

# find_first_byte(encrypted_msg)
first_byte = 65
# find_second_byte(encrypted_msg, first_byte)
second_byte = 66

decrypted = decrypt(encrypted_msg, bytes([first_byte, second_byte]))
print(decrypted.decode("utf8"))
