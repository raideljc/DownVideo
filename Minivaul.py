
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
#from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty,ListProperty, StringProperty, ColorProperty, BooleanProperty, ObjectProperty
from datetime import datetime
from kivymd.uix.screen import MDScreen
from pathlib import Path 
from cipher import cipher
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from itertools import cycle
from comun import *
import base64
import time
import os



               
class  MainVaul(MDScreen):
    pass
#    def on_enter(self):
#        self.app = App.get_running_app()
    
                             
class LoginVaul(MDScreen):
    def on_enter(self):
        try:
            self.app = MDApp.get_running_app()
            self.app.is_active = False
            self.app.cippass =  "" 
            self.app.ciplist = []
        finally:
            pass  
       
    def changepath(self):
        if self.app.cippass == "ShowHistorial" and self.app.path == "/storage/emulated/0/Documents":
            self.app.is_active = True
            self.app.ChangeScreenVaul('histovaul')
        else: 
            open_selector("Seleccione la carpeta donde están y/o estaran los archivos del baul.", path=self.app.path, callback = self.chpathend)
        
    def chpathend(self,path):
         self.app.path = path
      
    def key_down(self,txt):
       self.app.cippass = txt
       
    def aceptlogin(self):
        if self.app.cippass == '':
            return None
        self.app.ciplist = cipher.CheckPath(self.app.cippass, self.app.path) 
        self.app.is_active = True
        #self.app.writehistorial("A","" ,self.app.path )
        self.app.ChangeScreenVaul('mainvaul')   
        

class ItemVaul(MDBoxLayout):
    icon = StringProperty("")
    idfile = NumericProperty()
    file = StringProperty("")
    filedir = StringProperty("")
    color = ColorProperty((1,1,0,0.5))
    screen = ObjectProperty()
        
    def delitem(self):
        app = MDApp.get_running_app()
        app.ciplist.pop(self.idfile)
        self.screen.actlist()
        os.remove(self.filedir)
        showmessage(f"Archivo {self.file} eliminado correctamente", tipo = "succes")
        app.writehistorial("E",self.file, self.filedir)

    def dwitem(self):
        open_selector("Seleccione la carpeta donde se descargara el archivo", path='/storage/emulated/0/', callback = self.decifile)
        
    def decifile(self, path):
       app = MDApp.get_running_app()
       cipher.DecipherFile(app.cippass, self.filedir, path)
       app.writehistorial("D", self.file, self.filedir)
       #self.app.ChangeScreenVaul('mainvaul')
       #showmessage( f"Archivo {self.file} descargado  correctamente", tipo = "succes")
    

class Minivaul(MDScreen):
    dwfile = StringProperty("")
    
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.actlist()     
         
    def actlist(self):
        data = []
        cicle = cycle([(0.5, 0.5, 0.5, 0.08), (0.5, 0.5, 0.5, 0.15) ])
#        FILA_PAR   = 
#        FILA_IMPAR = 
        #cicle = cycle([(0, 0, 0, 0.4), (1, 1, 1, 0.3)])
        if self.app.ciplist != []: 
            for j,i in enumerate(self.app.ciplist):
                color = next(cicle)  
                data.append({
                    "icon": geticon(i[0]),
                    'file':  f'{ i[0] }', 
                    'filedir': f"{ i[1] }",
                    'idfile': j,
                    "color": color,
                    "screen": self,
                })    
        self.ids.rv_vaul.data = list(reversed(data))
     
    def upfile(self):
        open_selector("Seleccione el archivo a guardar", is_folder=False, path='/storage/emulated/0/', callback = self.upend)                
    def upend(self, file):
        fil = cipher.CipherFile(self.app.cippass , file, self.app.path)
        nom = os.path.basename(file)
        self.app.writehistorial("C", nom, fil)
        self.app.ciplist.append((nom,fil))
        showmessage("Achivo guardado correctamente", tipo = "succes")
        self.app.ChangeScreenVaul('mainvaul')
        self.actlist()     


   

                          

class Imgvaul(MDScreen):
    imgid = NumericProperty(0)
    imgnom = StringProperty("")
    listimg = ListProperty([])
    imglen = NumericProperty(0)
    #_ant = NumericProperty(0)
    
    def on_enter(self):
        self.listimg=[]
        extimg =['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'svg', 'ico', 'heic', 'raw',  'psd', 'ai', 'xcf']
        self.app = MDApp.get_running_app()
        for i in self.app.ciplist:
            ext = i[0].split(".")[-1]
            if ext in extimg:
                self.listimg.append(i)
        if  self.listimg ==[]:
            self.app.ChangeScreenVaul( 'mainvaul' )  
            return None
        self.imgid = 0
        self.imglen = len(self.listimg )
        self._ant = 0
        self.actimg()        
        
    def actimg(self):
        self.app.cleartemp()
        img = self.listimg[self.imgid ]
        self.imgnom = img[0]
        cipher.DecipherFile(self.app.cippass, img[1], self.app.temp)  
        imgdir = os.path.join(self.app.temp, img[0])  
        self.ids.img1.source = imgdir
        self.ids.img2.source = imgdir
        self.ids.img3.source = imgdir

    def complete(self, carrucel, dt):         
         if self._ant == 2 and dt == 0:
             self.imgid += 1
         elif (self._ant == 0 and dt == 2) or (self._ant > dt):
             self.imgid -= 1
         else:
             self.imgid += 1
         self.imgid %= self.imglen
         self._ant = dt
         self.actimg()

    def downimg(self):
        open_selector("Seleccione la carpeta donde se descargará la imagen", path='/storage/emulated/0/', callback = self.decifile)
        
    def decifile(self, path):
       img = self.listimg[self.imgid ][1]
       self.app.writehistorial("D",self.listimg[self.imgid ][0], img)
       cipher.DecipherFile(self.app.cippass, img, path)
       showmessage( "Imagen descargada correctamente", tipo = "succes")



class Videovaul(MDScreen):
    videoid = NumericProperty(0)
    videonom = StringProperty("")
    videolist = ListProperty([])
    videolen = NumericProperty(0)
    #_ant = NumericProperty(0)
    
    def on_enter(self):
        self.videolist=[]
        
        extvideo =['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv','webm', 'm4v','mpg', 'mpeg','3gp', 'ts']
        self.app = MDApp.get_running_app()
        for i in self.app.ciplist:
            ext = i[0].split(".")[-1]
            if ext in extvideo:
                self.videolist.append(i)
        if  self.videolist ==[]:
            self.app.ChangeScreenVaul( 'mainvaul' )  
            return None
        self.videoid = 0
        self.videolen = len(self.videolist )
        self.actvideo()      
        
    def actvideo(self):
        self.app.cleartemp()
        video = self.videolist[self.videoid ]
        self.videonom = video[0]
        cipher.DecipherFile(self.app.cippass, video[1], self.app.temp)  
        videodir = os.path.join(self.app.temp, video[0])  
        self.ids.videoplayer.source = videodir   

    def downimg(self):
        open_selector("Seleccione la carpeta donde se descargará la imagen", path='/storage/emulated/0/', callback = self.decifile)
        
    def decifile(self, path):
       img = self.listimg[self.imgid ][1]
       self.app.writehistorial("D",self.listimg[self.imgid ][0], img)
       cipher.DecipherFile(self.app.cippass, img, path)
       #showmessage( "Video descargado  correctamente", tipo = "succes")
        
        
 
class Vaulwait(MDScreen):    
    vel = NumericProperty(0)
    porc = NumericProperty(0)
    cipmodo = StringProperty("")
    def on_enter(self):
        self.app = MDApp.get_running_app()
        if not cipher.is_active:
            self.app.ChangeScreenVaul('mainvaul')    
            return None     
        Clock.schedule_once(self.showdatas, 0.1)
              
    def showdatas(self, dt):
        self.vel = cipher.velocity    
        self.porc = cipher.porcent       
        self.cipmodo = cipher.mode
        if not cipher.is_active:
            self.app.ChangeScreenVaul('mainvaul')    
            return None
        Clock.schedule_once(self.showdatas, 0.1)   
 

class ItemHistVaul(MDCard):
    fecha = StringProperty("")
    file = StringProperty("")
    icono = StringProperty("info")     
    action = StringProperty("")
                                  
                       
class Histovaul(MDScreen):   
    cachelist = ListProperty([])
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.showhist()
 
    def showhist(self):
        datalist = {
        "A":  ("Inicio la Aplicación","","application-open-outline"),
        "C": ("Archivo subido","file-upload-outline"),
        "D":   ("Archivo descargado","file-download-outline", "file-lock-open"),
        "V": ("Ver información","file-eye-outline"),  
        "E":  ("Archivo Eliminado","trash-can-outline"), 
        "H":  ("Historial Guardado","history"),
    }# account-arrow-up-outline
#    A (Abrir app): application-open
#· C (Cifrar archivo): file-lock
#· D (Descifrar archivo): file-lock-open
#· V (Ver info): information-outline o file-eye
#· E (Eliminar archivo): trash-can-outline
#· H (Guardar historial): history o content-save
        histo = self.readhisto()[:50]
        if self.cachelist == histo:
            return
        self.cachelist = histo
        data = []
        for i in histo:
            fecha = datetime.fromtimestamp(float(i[0])).strftime("%d/%m/%Y\n%I:%M:%S %p")
            line = datalist[str(i[1])]
            data.append({
                'icono': line[1], #icolist.get([i[1]),
                'fecha': fecha,
                'file':  str(i[2]),  
                'action': line[0],
            })
        self.ids.rv_hist_vaul.data = data   

    def readhisto(self):
        if not Path(self.app.histofile).exists():
            return([])
        with open(self.app.histofile, "rt") as fh:
            histtemp = fh.read().split("\n")
        histobin = [] 
        for i in reversed(histtemp):
                dec = base64.b64decode(i.encode()).decode().split("|")
                if dec!= [""]:
                    histobin.append(dec)
        return histobin
        
    def histopath(self):
        open_selector("Seleccione la carpeta donde guardara el historial", path='/storage/emulated/0/', callback = self.savehisto)
        
    def savehisto(self, path):
       datalist = {
        "A":"Inicio la Aplicación",
        "C": "Archivo subido",
        "D": "Archivo descargado",
        "V": "Ver información",
        "E":  "Archivo Eliminado",
        "H":  "Historial Guardado",
    }
       dir = os.path.join(path,"histo.txt")
       for i in self.readhisto():
            with open(dir,"at") as f:
                fecha = datetime.fromtimestamp(float(i[0])).strftime("%d/%m/%Y\n%I:%M:%S %p")
                f.write(f"{fecha} {datalist[i[1]]}  {i[2]} {i[3]}\n" )
       self.app.writehistorial("H",path)
       showmessage( "Historial guardado correctamente", tipo = "succes")
      