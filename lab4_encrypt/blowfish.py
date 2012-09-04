#! /usr/bin/python3
# -*- coding: utf-8 -*-
#~ Blowfish implementation
#~ look info http://www.fish-journal.com/2011/10/blowfish.html 

from blowfish_blocks import blocks
from copy import deepcopy

P, S = deepcopy(blocks.P), deepcopy(blocks.S)

def get_byte(n,k):
	return  (n>>(k*8))&0xFF
        
def get_block32(n,k):
        return  (n>>(k*32))&0xFFFFFFFF
        
def split_block32(block):
        return [get_byte(block,i) for i in range(3,-1,-1)]

def hexprint(lst):
        for bi in lst:
                print(hex(bi), end = ';')
        print()

def F(x):
        global S
        x3, x2, x1, x0 = [get_byte(x,i) for i in range(4)]
        return (((S[0][x0]+S[1][x1]) % 2**32 ^ S[2][x2]) +S[3][x3]) % 2**32
	
def feistel_encrypt(block):
        global P
        l, r = get_block32(block,0), get_block32(block,1)
        n = 16
        for i in range(n):
                l = l ^ P[i]
                r = F(l) ^ r
                l, r = r, l
        l, r = r, l
        r = r ^ P[n]
        l = l ^ P[n+1]
        return l, r
        
def feistel_decrypt(block):
        global P
        l, r = get_block32(block,1), get_block32(block,0)
        n = 16
        for i in range(n+1,1,-1):
                l = l ^ P[i]
                r = F(l) ^ r
                l, r = r, l
        l,r = r, l
        r = r ^ P[1]
        l = l ^ P[0]
        return l, r

def create_cryptkey(key):
        key_len = len(key)
        if not key or key_len < 8 or key_len > 56:
            raise ValueError("Incorrect length of the key")

        global P, S
        P, S = deepcopy(blocks.P), deepcopy(blocks.S)
        
        index = 0
        for i in range (len (P)):
                key_32bit = 0
                for j in range(4):
                        key_32bit <<= 8
                        key_32bit |= key[(index+j)%key_len]
                P[i] = P[i] ^ key_32bit
                index = index+4
        
        #~ Key and Blocks encription
        block = 0
        for i in range(0,len(P),2):
                l,r = feistel_encrypt(block)
                P[i] = l
                P[i+1] = r
                
                block = r; block <<= 32; block |= l
        
        for i in range(0,len(S)):
                for j in range(0,len(S[i]),2):
                        l,r = feistel_encrypt(block)
                        S[i][j] = l
                        S[i][j+1] = r
                        
                        block = r
                        block <<= 32; block |= l
        
def Blowfish(text,key,mode):
        #~ if mode == "ENCRYPT":
                #~ #expand text to mod 64 bit
                #~ mod = len(text)%8
                #~ if mod != 0: text += bytes(8-mod)
                

        chiperbyte = bytearray()
        l,r = 0,0
        for i in range(len(text)-8,-8,-8):
                block64 = 0
                for j in range(8):
                        block64 <<= 8
                        block64 |= text[i+j]
                
                
                if mode == "ENCRYPT":
                        l, r = get_block32(block64,1), get_block32(block64,0)
                        block64 = r; block64 <<= 32; block64 |= l
                        
                        l, r = feistel_encrypt(block64)
                elif mode == "DECRYPT":
                        l, r = get_block32(block64,0), get_block32(block64,1)
                        block64 = r; block64 <<= 32; block64 |= l
                        
                        l, r = feistel_decrypt(block64)
                        
                chiperbyte.extend(split_block32(l))
                chiperbyte.extend(split_block32(r))

        return chiperbyte

def exec_blowfish(key,plaintext,answer=None, mode=None, outfile=None):
        from binascii import a2b_hex, b2a_hex
        
        if mode == "ENCRYPT":
                #expand text to mod 64 bit
                mod = len(plaintext)%8
                if mod != 0: 
                        for i in range(8-mod):
                                plaintext += b'\0'
                print(plaintext)
        
        if (mode, outfile) == (None, None):
                #~ for ki in key:
                        #~ print(ki)
                key = a2b_hex(key)
                #~ for ki in key:
                        #~ print(ki) 
                plaintext = a2b_hex(plaintext)
                create_cryptkey(key)
                encrypttext = Blowfish(plaintext, key, "ENCRYPT")
                decrypttext = Blowfish(encrypttext, key, "DECRYPT")

                b2a_txt,b2a_key,b2a_enc,b2a_dec = [
			b2a_hex(bytes(t)).upper() for t in 
				(plaintext,key,encrypttext,decrypttext)]
				
                print("key = ", b2a_key, "plaintext = ",b2a_txt)
                print("enc = ", b2a_enc, "dec = ", b2a_dec)
        
                if b2a_enc != answer or b2a_dec != b2a_txt:
                        print("FAIL")
                        exit(-1)
                else:
                        print("OK")
        else:
                #~ key = a2b_hex(key)
                #~ plaintext = a2b_hex(plaintext)
                create_cryptkey(key)
                encrypttext = Blowfish(plaintext, key, mode)
                
                #~ b2a_enc = b2a_hex(bytes(encrypttext)).upper()
                b2a_enc = bytes(encrypttext)
                print(b2a_enc)
                open(outfile,'wb').write(b2a_enc)
        
        
def standart_tests():

        vectors = (
                (b'0000000000000000',        b'0000000000000000',        b'4EF997456198DD78'),
                (b'FFFFFFFFFFFFFFFF',        b'FFFFFFFFFFFFFFFF',        b'51866FD5B85ECB8A'),
                (b'3000000000000000',        b'1000000000000001',        b'7D856F9A613063F2'),
                (b'1111111111111111',        b'1111111111111111',        b'2466DD878B963C9D'),
                (b'49E95D6D4CA229BF',        b'02FE55778117F12A',        b'CF9C5D7A4986ADB5'),
                (b'E0FEE0FEF1FEF1FE',        b'0123456789ABCDEF',        b'C39E072D9FAC631D'),
                (b'07A7137045DA2A16',        b'3BDD119049372802',        b'2EEDDA93FFD39C79'),
                (b'0000000000000000',        b'0000000000000000',        b'4EF997456198DD78'),
                (b'FFFFFFFFFFFFFFFF',        b'FFFFFFFFFFFFFFFF',        b'51866FD5B85ECB8A'),
        )
        for k,t,a in vectors:
                exec_blowfish(k,t,a)
        
        

def main():
	
        import optparse
        
        cl = optparse.OptionParser()
        cl.add_option("-e",action = "store", dest = "enc", nargs = 3)
        cl.add_option("-d",action = "store", dest = "dec", nargs = 3)
        opts, args = cl.parse_args()
        enc, dec = opts.enc, opts.dec

        fin, fkey, fout, mode = 0,0,0,0
        if enc != None: 
                fin, fkey, fout = enc
                mode = "ENCRYPT"
        elif dec != None: 
                fin, fkey, fout = dec
                mode = "DECRYPT"
        else: 
                print("No args: standart test...")
                standart_tests()
                return None
                
        key = open(fkey,'rb').read()
        plaintext = open(fin,'rb').read()
        exec_blowfish(key=key, plaintext=plaintext, mode=mode, outfile=fout)


if __name__ == "__main__":
        main()

