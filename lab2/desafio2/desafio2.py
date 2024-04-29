import OpenSSL.crypto
import os
import glob
import re
from urllib.parse import urlparse

url = input("url: ")
url_parts = urlparse(url)
url = url_parts.netloc + url_parts.path

os.system("python3 getCertificateChain/getCertChain.py --removeCertificateFiles")
os.system(f"python3 getCertificateChain/getCertChain.py --hostname {url} --getCAcertPEM")

certs = []
for crt_file in glob.glob(os.path.join('.', '*.crt')):
    certs.append(OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM,
        bytes(open(crt_file).read(), 'utf-8')
    ))

if(len(certs) == 0):
    print("O website nao possui certificados!".upper())
    exit()

roots = []
try:
    with open("cacert.pem", 'r') as pem_file:
        raw = pem_file.read()
        pattern = r'-----BEGIN CERTIFICATE-----(.*?)-----END CERTIFICATE-----'
        pem_certs = re.findall(pattern, raw, re.DOTALL)
        for pem_cert in pem_certs:
            pem_cert = '-----BEGIN CERTIFICATE-----' + pem_cert + '-----END CERTIFICATE-----'
            c = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pem_cert)
            roots.append(c)
except FileNotFoundError:
    print("O arquivo cacert.pem não foi encontrado!")
    exit()
except Exception as e:
    print(f"Ocorreu um erro ao extrair os certificados do arquivo cacert.pem: {e}")
    
# print("")
# for pos, cert in enumerate(roots):
#     print("Certificate #" + str(pos))
#     for component in cert.get_subject().get_components():
#         print("Subject %s: %s" % (component[0].decode("utf-8"), component[1].decode("utf-8")))
#     for component in cert.get_issuer().get_components():
#         print("Issuer %s: %s" % (component[0].decode("utf-8"), component[1].decode("utf-8")))
#     print("notBefore: " + str(cert.get_notBefore().decode("utf-8")))
#     print("notAfter: " + str(cert.get_notAfter().decode("utf-8")))
#     print("version: " + str(cert.get_version()))
#     print("sigAlg: " + str(cert.get_signature_algorithm().decode("utf-8")))
#     print("digest: " + str(cert.digest('sha256').decode("utf-8")) +"\n")

# print("")
# for pos, cert in enumerate(certs):
#     print("Certificate #" + str(pos))
#     for component in cert.get_subject().get_components():
#         print("Subject %s: %s" % (component[0].decode("utf-8"), component[1].decode("utf-8")))
#     for component in cert.get_issuer().get_components():
#         print("Issuer %s: %s" % (component[0].decode("utf-8"), component[1].decode("utf-8")))
#     print("notBefore: " + str(cert.get_notBefore().decode("utf-8")))
#     print("notAfter: " + str(cert.get_notAfter().decode("utf-8")))
#     print("version: " + str(cert.get_version()))
#     print("sigAlg: " + str(cert.get_signature_algorithm().decode("utf-8")))
#     print("digest: " + str(cert.digest('sha256').decode("utf-8")) +"\n")


for pos, cert in enumerate(certs):
    if((pos + 1) < len(certs)):
        if(cert.get_issuer().get_components()[2][1] != certs[pos + 1].get_subject().get_components()[2][1]):
            print("Os certificados não são válidos!".upper())
            exit()

for root in roots:
    c = root.get_subject().get_components()
    cert_root = certs[-1].get_issuer().get_components()[2]
    
    for i in c:
        if i[0] == b'CN':
            if i[1] == cert_root[1]:
                print("Todos os certificados são válidos!\n".upper())
                exit()

print("Os certificados não são válidos!".upper())