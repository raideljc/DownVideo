from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import os, time
from pathlib import Path 
import threading
import string
import random
import base64


#nonce 16
#pass 32

class CipherClass():
    def __init__(self):
        self._filesize = 0
        self._tokenlen = 1024 * 1024 * 10
        self._filetoken = 0
        self._is_active = False
        self._init_time = 0
        self._hilo = None
        self._mode = ""
        
    @property
    def is_active(self):
            return self._is_active
   
    @property
    def mode(self):
            return self._mode 
            
    @property  
    def porcent(self)->float:
           if not self._is_active or self._filesize == 0:
               return 100
           per = 100*self._filetoken/self._filesize 
           return round(per,2)
                          
    @property  
    def velocity(self)->float:
           if not self._is_active or self._filesize == 0:
               return 0
           timepas = time.time() - self._init_time
           distpas = self._filesize - self._filetoken
           return round(distpas / timepas,2)         
     
    def _Ciphersys(self, pw, nonce = None, isencode=True):
        if not nonce:
            nonce = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=nonce,
            iterations=1000,
            backend=default_backend()
        )
        if isinstance(pw, str):
            pw=pw.encode()
        clave = kdf.derive(pw) 
        cip = Cipher(algorithms.AES(clave), modes.CTR(nonce), backend=default_backend())
        mode = cip.encryptor( )if isencode else cip.decryptor()
        return mode, nonce
        
    def GetKeyFernet(self, pw):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'\xf2)B\xdb\xb1 `\xae\x0fx',
            iterations=100,
        )
        key = base64.urlsafe_b64encode(kdf.derive(pw.encode()))
        cipher = Fernet(key)
        return cipher
        #return (Fernet.generate_key())  
        
    def CipherFernet(self, pw, text):
        cipher = self.GetKeyFernet(pw) 
        return (base64.b64encode(cipher.encrypt(text.encode())).decode())

    def DecipherFernet(self, pw, text):
        try:
            cipher = self.GetKeyFernet(pw) 
            return(cipher.decrypt(base64.b64decode(text)).decode() )
        except: 
            return ""      
    
    def CipherTxt(self, pw, txt, nonce = None):
        cpsys, nonce = self._Ciphersys(pw, nonce)
        if isinstance(txt, str):
            txt = txt.encode("utf-8")
        cp=cpsys.update(txt)   
        return  nonce+cp
     
     
     
    def DecipherTxt(self, pw, ciphbin): 
        nonce = ciphbin[:16]     
        cpsys, _ = self._Ciphersys(pw, nonce, False)
        txtbin = cpsys.update(ciphbin[16:])   
        return txtbin
        
           
    def CipherFile(self, pw, filein, pathout):
        while True:       
            flistnom = random.choices( string.ascii_letters, k=15) 
            fname = ''.join( i for i in flistnom)+".bin"
            fileout = os.path.join(pathout, fname)
            if not(Path(fileout).is_file()): 
                break
        def ciphilo(pw):
            pwpass = b'\x9fd\x1c\x98\xfaG\xf57\xa4\xdc\xf82\xb7\xad\xa7\nq\xf1\xf2\xd8\x17\xc2\xc2\x81+\x00\xdb<\xa2\x85\xfc)'
            cpsys, nonce = self._Ciphersys(pw)
            if isinstance(pw, str):
                pw = pw.encode("utf-8")
            lpw = len(pw)
            for i in range(0, 32-lpw):
                pw += chr((125+lpw*i)%128).encode("ascii") 
            hashfile = self.CipherTxt(pwpass,pw, nonce)
            fn = os.path.basename(filein)
            flenname = len(fn)
            fname = b""
            for i in range(0, flenname):
                fname += chr((ord(fn[i])+ flenname+i)%128).encode("utf-8")
            flenname = bytes([flenname])
            with open(fileout,"wb") as fo:
                fo.write(hashfile+nonce+ flenname+fname)
                with open(filein,"rb") as fi: 
                    while True:
                        firead = fi.read(self._tokenlen)
                        if not firead:
                            break
                        cipchunk = cpsys.update(firead)
                        fo.write(cipchunk)
                        self._filetoken += len(firead)
                fo.write(cpsys.finalize())
                self._filesize = 0
                self._filetoken = 0
                self._is_active = False
                self._init_time = 0
                self._hilo = None          
                self._mode = ""     
        f = Path(filein)
        if not(f.exists() and f.is_file()): 
            return "error file no fount"
        self._filesize = os.path.getsize(filein)
        self._filetoken = 0
        self._is_active = True
        self._mode = "cipher"     
        if self._filesize < 5 * self._tokenlen:
            ciphilo(pw)
        else:
            self._hilo= threading.Thread(target=ciphilo,args=(pw,), daemon=True) 
            self._hilo.start()
        
        return fileout

 
                           
    def DecipherFile(self, pw, filein, pathout):
        def decihilo():
             with open(filein, "rb") as fi:
                fi.read(48)
                nonce = fi.read(16)
                cpsys, _ = self._Ciphersys(pw,nonce , False )
                lfnom = int(fi.read(1)[0])
                nom = fi.read(lfnom).decode("utf-8")
                fname = ""
                for i in range(0, lfnom):
                    fname += chr((ord(nom[i]) - lfnom -i) % 128)
                fname = os.path.join(pathout, fname)
                with open(fname, "wb") as fo:
                    while True:
                        firead = fi.read(self._tokenlen)
                        if not firead:
                            break
                        cipchunk = cpsys.update(firead)
                        fo.write(cipchunk)
                        self._filetoken += len(firead)
                    fo.write(cpsys.finalize()) 
                    self._filesize = 0
                    self._filetoken = 0
                    self._is_active = False
                    self._init_time = 0
                    self._hilo = None    
                    self._mode = ""      
        if not self.CheckFile(pw, filein):
            return None
        self._filesize = os.path.getsize(filein)
        self._filetoken = 0
        self._is_active = True  
        self._init_time = time.time()
        self._mode = "decipher"
        if self._filesize < 5 * self._tokenlen:
            decihilo()
        else:
            self._hilo= threading.Thread(target=decihilo, daemon=True) 
            self._hilo.start()
        
                           
 
           
    def CheckFile(self, pw, file):
        pwpass = b'\x9fd\x1c\x98\xfaG\xf57\xa4\xdc\xf82\xb7\xad\xa7\nq\xf1\xf2\xd8\x17\xc2\xc2\x81+\x00\xdb<\xa2\x85\xfc)'
        f = Path(file)
        if not(f.exists() and f.is_file()):
            return False
        if os.path.getsize(f)<80:
            return False
        with open(f,"rb") as fi:
            nonce = fi.read(16)
            fhash = fi.read(32)
            if isinstance(pw, str):
                pw = pw.encode("utf-8")
            lpw = len(pw)
            for i in range(0, 32-lpw):
                pw += chr((125+lpw*i)%128).encode("ascii") 
            hash = self.CipherTxt(pwpass,pw, nonce)
        return hash == nonce+fhash
        

       
    def CheckPath(self, pw, path):  
        res = []   
        if path == "":
            path = os.path.dirname(__file__)
        for i in os.scandir(path):
            if i.is_file():
                name = self.GetFileName(pw, i)
                if name != "":
                    xdir = os.path.join('', i)
                    res.append((name, xdir))
        return res
            
 
               
    def GetFileName(self, pw, file):
        if not self.CheckFile(pw, file):
            return ""
        with open(file, "rb") as f:  
            f.read(64)
            lfnom = int(f.read(1)[0])
            nom = f.read(lfnom).decode("utf-8")
            fname = ""
            for i in range(0, lfnom):
                fname += chr((ord(nom[i]) - lfnom -i) % 128)
            return fname
            
        
    
      
    
    
    
    
cipher = CipherClass()


if __name__ == '__main__':
    cip = cipher.CipherTxt( "pass", "Prueba de cifrado")
    print(cipher.GetKeyFernet())
    plaintxt = cipher.DecipherTxt( "pass", cip)
    #print(plaintxt)
#    cipname = cipher.CipherFile("paipher.py" ,"Cip")
#    print(cipher.CheckFile("pass", "cipherfile.bin"))
#    print(cipher.GetFileName("pass", "cipherfile.bin"))
#    #cipher.DecipherFile("pass", f"Cip/{cipname}", "Cip")
#    print(cipher.CheckPath("pass", "") )
