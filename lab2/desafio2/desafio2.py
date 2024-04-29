# Para explicação da resolução do desafio, ler README.md

import OpenSSL.crypto
import os
import glob
import re
from urllib.parse import urlparse

# Lê url da entrada e a processa para deixar num formato padrão
url = input("url: ")
url_parts = urlparse(url)
url = url_parts.netloc + url_parts.path
if url[-1]:
    url = url[0:-1]
    
# Usa o programa feito por TheScriptGuy para baixar os certificados da página web e o arquivo de certificados da entidade certificadora (cacert.pem)
os.system("python3 getCertificateChain/getCertChain.py --removeCertificateFiles")
os.system(f"python3 getCertificateChain/getCertChain.py --hostname {url} --getCAcertPEM")

# Constroi objetos para cada certificado salvo pelo programa acima
certs = []
for crt_file in glob.glob(os.path.join('.', '*.crt')):
    certs.append(OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM,
        bytes(open(crt_file).read(), 'utf-8')
    ))

# Caso o website não forneça nenhum certificado, imprime mensagem e finaliza o programa
if(len(certs) == 0):
    print("O website nao possui certificados!".upper())
    exit()

# Carrega todos os certificados disponibilizados pela entidade certificadora (localizados em cacert.pem)
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
    
# Os trechos de código abaixo podem ser descomentados para imprimir informações a respeito dos certificados fornecedos pela página web ou pela entidade certificadora

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

# Verifica se a cadeia de certificados é válida (se o certificado n foi emitido pela entidade n+1)
for pos, cert in enumerate(certs):
    if((pos + 1) < len(certs)):
        if(cert.get_issuer().get_components()[2][1] != certs[pos + 1].get_subject().get_components()[2][1]):
            print("Os certificados não são válidos!".upper())
            exit()

# Verifica se o último certificado foi emitido pela entidade certificadora
for root in roots:
    c = root.get_subject().get_components()
    cert_root = certs[-1].get_issuer().get_components()[2]
    
    for i in c:
        if i[0] == b'CN':
            if i[1] == cert_root[1]:
                print("Todos os certificados são válidos!\n".upper())
                exit()

print("Os certificados não são válidos!".upper())