#coding=utf-8
from Crypto.Cipher import AES
KEY = "9878*(&^^&)0LLIu(*&^))#$@!KJLKJj"

class crypt():
    def __init__(self,key):
        self.key = key
        self.mode = AES.MODE_CBC

    def encrypt(self,text):
        cryptor = AES.new(KEY,self.mode)
        length = 16
        count = text.count('')
        if count < length:
            add = (length-count) + 1
            text = text + (' ' * add)
        elif count > length:
            add = (length-(count % length)) + 1
            text = text + (' ' * add)
        self.ciphertext = cryptor.encrypt(text)
        return self.ciphertext

    def decrypt(self,text):
        cryptor = AES.new(KEY,self.mode)
        plain_text  = cryptor.decrypt(text)
        return plain_text

if __name__=='__main__':
    text = "你好"
    key = "9878*(&^^&)0LLIu(*&^))#$@!KJLKJj"
    en = crypt(key)
    entext = en.encrypt(text)
    print entext

    detext = en.decrypt(entext).rstrip()
    print detext