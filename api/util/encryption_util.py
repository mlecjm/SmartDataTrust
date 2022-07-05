import base64
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

"""
Author          : Neda Peyrone
Create Date     : 01-07-2022
File            : encryption_util.py
Purpose         : -
"""

def encrypt(path, raw_data):
  print(f'raw_data: {raw_data}')
  with open(path, 'rb') as f:
    data = f.read()
  public_key = RSA.importKey(data)
  cipher = PKCS1_v1_5.new(public_key)
  ciphertext = cipher.encrypt(bytes(raw_data, encoding="UTF-8"))
  return base64.b64encode(ciphertext)

def decrypt(path, base64_encoded):
  ciphertext = base64.b64decode(base64_encoded)
  with open(path, 'rb') as f:
    data = f.read()
  private_key = RSA.importKey(data)
  cipher = PKCS1_v1_5.new(private_key)
  sentinel = Random.new().read(16)
  return cipher.decrypt(ciphertext, sentinel)