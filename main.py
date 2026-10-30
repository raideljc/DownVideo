#wPydroid run terminal

#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
import os
os.environ["KIVY_VIDEO"] = "ffpyplayer"

from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty,ListProperty, StringProperty, ColorProperty, BooleanProperty, ObjectProperty, DictProperty
from kivy.clock import Clock
from Minivaul import *
from comun import *
from Downtube import *
from pathlib import Path 
from kivy.lang import Builder
#from android.permissions import request_permissions, Permission      
from cipher import cipher 
from datetime import  timedelta
from comun import *
from Minivaul import *
from Downtube import *
import time
import yt_dlp
import json
import shutil
import base64
from kivy.config import Config



class DownTubeApp(MDApp):
    # variables generales    
    version = StringProperty("1.0.0")
    appname = StringProperty("DownTube")
    appcode = StringProperty("")
    appcheck = StringProperty("")
#    ffmpegdir = StringProperty("")
    temp = StringProperty("")
    appmode = NumericProperty(0)
    basepath = StringProperty("")
    darkmode = BooleanProperty(False)
    datasfile = StringProperty('')
# Variables del baul
    cippass = StringProperty('')
    ciplist = ListProperty([])
    path = StringProperty('')
    is_active = BooleanProperty(False)
    histofile = StringProperty("")
#  variables del descargador   
    histodown = StringProperty("")
    pagelen = NumericProperty(4)
    downloading = BooleanProperty(False)
    download_path = StringProperty("")
    downless = StringProperty("")
    checksumhisto = StringProperty("")
    downprogress = NumericProperty(0)
    status = StringProperty("")
    subtitles = StringProperty('')
    geopass = StringProperty('')
    proxy = StringProperty('')
    retries = NumericProperty(10)
    histodict = DictProperty({
        "start" : True,
        "close": True,
        "setting": True,
    })

                
    def build(self):
        self.title = "DownTube"
        self.theme_cls.primary_palette =  "Blue"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.theme_style = "Dark" if self.darkmode else "Light"
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_hue ="700"
        Window.softinput_mode = "below_target"
        pat = get_default_paths()
        self.temp = pat['temp'] 
        self.basepath = pat['base'] 
        self.histofile =os.path.join(pat['datas'], "downdatas.bin")  
        self.datasfile = os.path.join(pat['datas'], "maindatas.bin")  
        self.histodown = os.path.join(pat['datas'],"historial.log")  
        self.checksumhisto = os.path.join(pat['datas'],"checksum.pyc")  
        self.download_path =os.path.join(pat['download'], self.title)  
        self.path =pat['base']
        if not(Path(self.temp ).exists()):
            Path.mkdir(self.temp)
        if os.path.exists("screens"):
            for file in os.listdir("screens"):
                if file.endswith(".kv"):
                    Builder.load_file(os.path.join("screens", file))
  #      request_permissions([
#            Permission.WRITE_EXTERNAL_STORAGE,
#            Permission.READ_EXTERNAL_STORAGE
#        ])
        self.cleartemp()
        self.ReadSetting()
        Window.bind(on_keyboard=self.hook_keyboard)
        if self.checkcode():
            Clock.schedule_once(lambda dt: self.ChangeScreenMain("MainScreen"))
        if self.histodict["start"] : self.write_hist_down("Iniciar aplicación")  
        return DownTube() 

          
    def on_stop(self): 
        if self.histodict["close"] : self.write_hist_down("Fin de Aplicación")
        self.histodict["close"] = False
        self.cleartemp()        

                                
    def cleartemp(self):
        shutil.rmtree(self.temp)
        Path(self.temp).mkdir(exist_ok=True)

    
    def SaveSetting(self):
        keys = {"AppCode": self.appcode,"AppCheck":self.appcheck,"Carpeta": self.download_path,"ModoOscuro":self.darkmode, "ColorPrincipal":self.theme_cls.primary_palette,"ColorSecundario": self.theme_cls.accent_palette, "Historial": self.histodict,  "Subtitles":self.subtitles, "Geopass":self.geopass,"Proxy": self.proxy, "Retries": self.retries, "Hue":self.theme_cls.primary_hue, }
        jsonstr = json.dumps(keys, indent=4, ensure_ascii=False)
        text = base64.b64encode(jsonstr.encode()).decode()
        with open(self.datasfile, 'w', encoding='utf-8') as f:
            f.write(text)   


    def ReadSetting(self):
         if not os.path.isfile(self.datasfile):
             self.appcode = makecode()
             self.SaveSetting()
             return
         with open(self.datasfile, 'r', encoding='utf-8') as f:
            text = f.read()
            dec = base64.b64decode(text.encode()).decode()
            datos = json.loads(dec)
            self.appcode = datos["AppCode"]
            self.appcheck = datos["AppCheck"]
            self.darkmode = datos["ModoOscuro"]
            self.theme_cls.theme_style = "Dark" if self.darkmode else "Light"
            self.download_path = datos["Carpeta"]
            self.histodict =datos["Historial"] 
            self.theme_cls.primary_palette = datos["ColorPrincipal"]
            self.theme_cls.accent_palette = datos["ColorSecundario"]
            self.subtitles = datos["Subtitles"]
            self.geopass = datos["Geopass"]
            self.proxy = datos["Proxy"]
            self.retries = datos["Retries"]
            self.theme_cls.primary_hue = datos["Hue"]

                                    
    def ChangeScreenMain(self, screen):      
        sm = self.root.ids.smmain
        self.cleartemp()    
        self.root.ids.nav_drawer.set_state("close")
        if self.appmode == 0:
            self.root.ids.smmain.current = "BlockScreen"        
        if sm.current == screen:
            return
        if screen == "VaulScreen" and self.appmode >= 2:
            if not self.downloading:
                self.root.ids.smmain.current = "VaulScreen"
                self.ChangeScreenVaul('loginvaul') 
        else:
            self.root.ids.smmain.current = screen

                        
    def checkcode(self):
       if not self.appcheck:
           return False
       ciptxt = cipher.DecipherFernet(self.appcode, self.appcheck)
       if str(ciptxt) in ["1", "2","3"]:
           self.appmode = int(ciptxt)
           return True
       else:
           return False

                                                  
    def ChangeScreenVaul(self, screen):
        self.cleartemp()
        if self.root.ids["smmain"]:
            sm = self.root.ids.smmain.current_screen.ids.smvaul
        else:
            sm = self.root.ids.smvaul
        if not self.is_active:
            sm.current = 'loginvaul'
        elif cipher.is_active:
            sm.current = 'vaulwait'
        else:
            sm.current = screen

                                                
    def toggle_dark_mode(self, active: bool):
        self.darkmode = active
        self.theme_cls.theme_style = "Dark" if active else "Light"


    def update_progress(self, value: float, status: str = None, left: str = None):
        self.downprogress = value
        if status:
            self.status = status
        if left:
            self.downless = left


    def writehistorial(self, action, file="", extra =""):
        #A: Abrir, C: Cifrar, D: Decifrar, V: Ver info, E: eliminar, H: Guardar historial  
        if os.path.isfile(file):
            filtxt = os.path.basename(extra)
        else:
            filtxt = extra
        fecha = datetime.now()
        text = f"{ str(fecha.timestamp()) }|{ action }|{ file }|{ filtxt }"
        text = base64.b64encode(text.encode()).decode()+"\n"
        with open(self.histofile,"at") as f:
            f.write(text)

                                              
    def write_hist_down(self, action, type="info",description="", extra =""):
        # "info"  "succes"  "error"
        fecha = datetime.now()  
        text = f"{ str(fecha.timestamp()) }|{ type }|{ action }|{ description }|{ extra }\n"
        with open(self.histodown,"at") as f:
            f.write(text)


    def progress_hook(self, d):
        percent = 0
        status = ""
        downless = ""
        if d['status'] == 'downloading':
            falta = d.get("eta", 0)
            downless=seg_to_time(falta)
            if "_percent" in d:
                percent = d["_percent"]
            elif 'total_bytes' in d:
                total = d['total_bytes']
                downloaded = d.get('downloaded_bytes', 0)
                percent = (downloaded / total) * 100
            if 'speed' in d:
                speed = d.get("speed", 0)
                speed_txt = human(speed)+'/s ' 
                status = f"Descargando...   {speed_txt} "
        elif d['status'] == 'finished':
            status = "Procesando archivo..."
        Clock.schedule_once(lambda dt: self.update_infos(percent, status, downless))

        
    def postprocessor_callback(self, d):
        #if self.root.ids.smmain.current == "MainScreen":
#            Clock.schedule_once(lambda dt: self.ChangeScreenMain("WaitScreen"))
        percent = 0
        status = ""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                total = d['total_bytes']
                downloaded = d.get('downloaded_bytes', 0)
                percent = (downloaded / total) * 100
            if 'speed' in d:
                speed = d.get("speed", 0)
                speed_txt = human(speed)+'/s ' 
                status = f"Descargando...   {speed_txt} "
        elif d['status'] == 'finished':
            Clock.schedule_once(lambda dt: self.ChangeScreenMain("MainScreen"))
        Clock.schedule_once(lambda dt: self.update_infos(percent, status))

        
    def update_infos(self, value, status, downless = ""):
        self.downless = downless
        if value > 0:
            self.downprogress = min(value, 100)
        if status != "":
            self.status = status                 

                
    def showsmsdown(self, texto, 
    type, extra=""):
             if type == "error":
                 if "Failed to establish a new connection" in extra:
                    extra = "Failed to establish a new connection. Connection refused"
                 Clock.schedule_once(lambda dt: showmessage(f"{texto}\n{extra}", type))
                 self.write_hist_down(f"{texto}",type, extra)
             else:
                 self.write_hist_down(f"{texto}", type,"", extra)
                 Clock.schedule_once(lambda dt: showmessage(f"{texto}", type))
             self.ChangeScreenMain("MainScreen")
             
    
    def hook_keyboard(self, win, key, *largs):
        if key == 27:  
            sm = self.root.ids.smmain
            if sm.current ==  "VaulScreen":
                smv = sm.current_screen.ids.smvaul.current
                if smv !=  'mainvaul' and smv !=  'loginvaul':
                    Clock.schedule_once(lambda dt: self.ChangeScreenVaul('mainvaul')) 
                    return True   
            if sm.current !=  "MainScreen":
                Clock.schedule_once(lambda dt: self.ChangeScreenMain("MainScreen"))
                return True  
            self.stop()
        return False  


if __name__ == "__main__":
    Config.set('kivy', 'exit_on_escape', '0')
    DownTubeApp().run()