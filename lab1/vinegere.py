def encrypt_vinegere(plaintext, key):
    ciphertext = ""
    key_length = len(key)

    for i in range(len(plaintext)):
        char = plaintext[i]

        if char.isalpha():
            shift = ord(key[i % key_length].upper()) - ord('A')
            if(char.islower()):
                ciphertext += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                ciphertext += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            ciphertext += char

    return ciphertext

def decrypt_vigenere(ciphertext, key):
    plaintext = ""

    for i in range(len(ciphertext)):
        char = ciphertext[i]
        key_length = len(key)

        if char.isalpha():
            shift = ord(key[i % key_length].upper()) - ord('A')
            if char.islower():
                plaintext += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                plaintext += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            plaintext += char

    return plaintext

def find_key(ciphertext, key):
    for i in range(26):
        new_key = key + chr(ord('a') + i)
        x = decrypt_vigenere(ciphertext, new_key)
        print(f"key: {new_key}, message: {x.encode("utf8")}")



ciphertext1 = "Coqebkxmk ow Mywzedkmky 2024/1"
ciphertext2 = "Ciqybexgk oq Gyqzydemey 2024/1"
ciphertext3 = "Cieevyxgy ik Gmwtsdeaks 2024/1"
ciphertext4 = "Ciembeluk ce Gmezyrsmem 2024/1"

""" find_key(ciphertext1, "") """
key1 = 'k'
""" find_key(ciphertext2, "k") """
key2 = "ke"
""" find_key(ciphertext3, "ke") """
key3 = "key"
""" find_key(ciphertext4, key3) """
key4 = "keys"
