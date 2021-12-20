#Reference to code: https://github.com/RyanRiddle/elgamal=============
import random
import sys,os

class PublicKey(object):
    def __init__(self, p=None, g=None, h=None, iNumBits=256):
        self.p = p
        self.g = g
        self.h = h
        self.iNumBits = iNumBits

def modexp( base, exp, modulus ):
        return pow(base, exp, modulus)

def encode(sPlaintext, iNumBits):
        byte_array = bytearray(sPlaintext, 'utf-16')
        
        z = []
        
        k = iNumBits//8
        j = -1 * k
        for i in range( len(byte_array) ):
                if i % k == 0:
                        j += k
                        z.append(0)
                z[j//k] += byte_array[i]*(2**(8*(i%k)))
        
        return z

def encrypt(key, sPlaintext):

        try:
                        
                z = encode(sPlaintext, key.iNumBits)
                cipher_pairs = []
                for i in z:
                        y = random.randint( 0, key.p )
                        c = modexp( key.g, y, key.p )
                        d = (i*modexp( key.h, y, key.p)) % key.p
                        cipher_pairs.append( [c, d] )

                encryptedStr = ""
                for pair in cipher_pairs:
                        encryptedStr += str(pair[0]) + ' ' + str(pair[1]) + ' '
        
                return encryptedStr   
        except Exception as e :
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                

#==========================================================================================