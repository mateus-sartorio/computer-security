def genkey(length: int) -> bytes:
    return str.encode("".join([chr(ord("A"))*length]))

def xor_strings(s, t) -> bytes:
    if isinstance(s, str):
        return "".join(chr(ord(a) ^ b) for a, b in zip(s, t)).encode("utf8")
    else:
        return bytes([a ^ b for a, b in zip(s, t)])

def decrypt(s):
    for i in range(256):
        decrypted_message = "".join(chr(a ^ i) for a in s).encode("utf8")
        print(f"\nkey: {i}, message: {decrypted_message}\n")

message = 'This is the unencrypted message!'
print('Message:', message)

key = genkey(len(message))
print('Key:', key)

cipherText = xor_strings(message.encode('utf8'), key)
print('cipherText:', cipherText)

decrypt(cipherText)
