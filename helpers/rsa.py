# RSA helper class for pycrypto
# Copyright (c) Dennis Lee
# Date 21 Mar 2017

# Description:
# Python helper class to perform RSA encryption, decryption,
# signing, verifying signatures & keys generation

# Dependencies Packages:
# pycrypto

# Documentation:
# https://www.dlitz.net/software/pycrypto/api/2.6/

# https://gist.github.com/dennislwy/0194036234445776d48ad2fb594457d4

import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
ALPHA_NUMERIC = "abcdefghijklmnopqrstuvwxyz0123456789"


def generateNewRandomAlphaNumeric(length):
    random.seed()
    values = []
    for i in range(length):
        values.append(random.choice(ALPHA_NUMERIC))
    return "".join(values)


hash = "SHA-256"


def newkeys(keysize):
    random_generator = Random.new().read
    key = RSA.generate(keysize, random_generator)
    private, public = key, key.publickey()
    return public, private


def importKey(externKey):
    return RSA.importKey(externKey)


def getpublickey(priv_key):
    return priv_key.publickey()


def encrypt(message, pub_key):
    # RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(message)


def decrypt(ciphertext, priv_key):
    # RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)


def sign(message, priv_key, hashAlg="SHA-256"):
    global hash
    hash = hashAlg
    signer = PKCS1_v1_5.new(priv_key)
    if (hash == "SHA-512"):
        digest = SHA512.new()
    elif (hash == "SHA-384"):
        digest = SHA384.new()
    elif (hash == "SHA-256"):
        digest = SHA256.new()
    elif (hash == "SHA-1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.sign(digest)


def verify(message, signature, pub_key):
    signer = PKCS1_v1_5.new(pub_key)
    if (hash == "SHA-512"):
        digest = SHA512.new()
    elif (hash == "SHA-384"):
        digest = SHA384.new()
    elif (hash == "SHA-256"):
        digest = SHA256.new()
    elif (hash == "SHA-1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.verify(digest, signature)


def sign_url(url, private_pem, salt=""):
    private_key = importKey(private_pem)
    msg = "%s%s" % (url, salt)
    return b64encode(sign(msg, private_key, "SHA-256"))


def verify_sig(url, signature, public_openssh, salt=""):

    public_key = importKey(public_openssh)
    msg = "%s%s" % (url, salt)
    return verify(msg, b64decode(signature), public_key)
