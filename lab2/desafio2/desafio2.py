import OpenSSL.crypto
import os
import glob

url = input("url: ")
url = url.replace("https://","")
url = url.replace("http://","")
url = url.rstrip("/")

os.system("python3 getCertificateChain/getCertChain.py --removeCertificateFiles")
os.system(f"python3 getCertificateChain/getCertChain.py --hostname {url} --getCAcertPEM")

certs = []
for crt_file in glob.glob(os.path.join('.', '*.crt')):
    certs.append(OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM,
        bytes(open(crt_file).read(), 'utf-8')
    ))

print("")
for pos, cert in enumerate(certs):
    print("Certificate #" + str(pos))
    for component in cert.get_subject().get_components():
        print("Subject %s: %s" % (component[0].decode("utf-8"), component[1].decode("utf-8")))
    for component in cert.get_issuer().get_components():
        print("Issuer %s: %s" % (component[0].decode("utf-8"), component[1].decode("utf-8")))
    print("notBefore: " + str(cert.get_notBefore().decode("utf-8")))
    print("notAfter: " + str(cert.get_notAfter().decode("utf-8")))
    print("version: " + str(cert.get_version()))
    print("sigAlg: " + str(cert.get_signature_algorithm().decode("utf-8")))
    print("digest: " + str(cert.digest('sha256').decode("utf-8")) +"\n")

for pos, cert in enumerate(certs):
    if((pos + 1) < len(certs)):
        if(cert.get_issuer().get_components()[2][1] != certs[pos + 1].get_subject().get_components()[2][1]):
            print("Os certificados não são válidos!".upper())
            """ os.system("python3 getCertificateChain/getCertChain.py --removeCertificateFiles") """

print("Todos os certificados são válidos!\n".upper())
""" os.system("python3 getCertificateChain/getCertChain.py --removeCertificateFiles") """
