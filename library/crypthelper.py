from binascii import b2a_hex, a2b_hex

from Crypto.Cipher import AES


# 加密类
class Crypter:
    def __init__(self):
        self.key = b"yingfei200566666"
        self.mode = AES.MODE_CBC
        self.length = 16
        self.ciphertext = ''

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        text = text.encode()  # bytes
        cryptor = AES.new(self.key, self.mode, b'0' * self.length)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        count = len(text)
        if (count % self.length != 0):
            add = self.length - (count % self.length)
        else:
            add = 0
        text = text + (b'\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext).decode()  # string

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0' * self.length)
        plain_text = cryptor.decrypt(a2b_hex(text))
        plain_text = plain_text.decode()
        return plain_text.rstrip('\0')


if __name__ == '__main__':
    pc = Crypter()
    e = pc.encrypt("123456")
    d = pc.decrypt(e)
    print(e, d)
