import random
import math

def is_prime(n, k=5):
    """Check if a number is prime using Miller-Rabin primality test."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n as 2^r*d + 1
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(length):
    """Generate a prime number with the specified length in bits."""
    while True:
        num = random.getrandbits(length)
        # Set the most significant and least significant bits to ensure the correct length
        num |= (1 << length - 1) | 1
        if is_prime(num):
            return num

def find_prime_pair_with_diff(length, diff):
    """Find a pair of prime numbers with the specified length and difference between them."""
    while True:
        print(".",end="")
        prime1 = generate_prime(length)
        prime2 = prime1 + diff
        if is_prime(prime2):
           print("\nFinished!")
           return prime1, prime2

length = 512
diff = 10

p, q = find_prime_pair_with_diff(length, diff)

print(f"p: {p}")
print(f"q: {q}")

from Crypto.Util import number
from Crypto.PublicKey.RSA import construct
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

e = 65537                 #Default RSA value
n = p*q                   #we make our modulus
phi = (p-1)*(q-1)         #this one is for making the private key
gcd, d, b = egcd(e, phi)  #now we have all our RSA values.

print(gcd)
print(f"d: {d}")
print(b)

key_params = (n, e, d)
key = RSA.construct(key_params)
print(key_params)

privateKey = key
publicKey = key.publickey()

print(key.exportKey())
print(key.publickey().exportKey())


from Crypto.Util.number import isPrime
from gmpy2 import iroot
from Crypto.PublicKey import RSA

encryptedMsg = b'6\xa6\x81;\xa5xm\xc5*\x9dp\x1b\xc9\xefL\xe3\xc0\x9b\xda\x0fc\x9fCm\x1a\xb4{\x8b\x94\x8b\xf7\xfc\x87\x9c\xf3\x80z\x0f\xf6O\xee\xa5\xdb\xc3\x12]\xb0\x9c\xf5\x92\xd3\x12`\xa5\xa7\x8d\x00\xab\xb9,\xf3r\xbb\x14\xf1Wkg\x95.\x7f"\xe3\xe4-\xc7\xc2Y=\x9bQ ]\xfbc\x08\x13~\xcc\xf7M\xa5\xfeA%\xef)\x98\xd5\xb8\xeb\xf9rq%\xc3*\x9f\x05JcA\xc5\x15\xb1\xd5\x1aU\xd2\x12\xdc\x16X\x9d\xa7\xe8\xf1\xe2'
public_key = RSA.import_key(b'-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDd+ALya2U5hTM8+2F4Ju06b+7a\nA6vDR2nEzJfHBRpyNdovHsG1H+zObMQro+V1ORrZfZ4Y4aEscCEcEuzDEMaUluCM\nHdncv7VkdhUqqicnJIXlstIPB5ScbQIpJMu3asVtz8XpkPIMLmgYUgpRxXz9tKza\nvjzkaRQrETZM8TOG6wIDAQAB\n-----END PUBLIC KEY-----')

p = iroot(public_key.n,2)[0]
while not isPrime(p):
  p += 1

q = p - 1
while not isPrime(q):
  q -= 1

assert public_key.n == p * q
assert e == 65537

phi = (p-1)*(q-1)

def egcda(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

gcd, d, b = egcda(e, phi)
print(gcd)
print(d)
print(b)

key_params = (public_key.n, e, d)

key = RSA.construct(key_params)

# privateKey = key
# publicKey = key.publickey()
# cipher_rsa = PKCS1_OAEP.new(privateKey)
# decryptedMsg = cipher_rsa.decrypt(encryptedMsg)
# print(key.exportKey())
# print(key.publickey().exportKey())
# print("decryptedMsg: ", decryptedMsg.decode("utf-8"))
# print('\n')
