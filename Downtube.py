from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.properties import NumericProperty,ListProperty, StringProperty, ColorProperty, BooleanProperty, ObjectProperty
from datetime import  timedelta,  datetime
from kivy.clock import Clock
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from comun import *
from Minivaul import *
from ytbdown import *
from kivymd.color_definitions import palette, colors
import yt_dlp 
import os

class  DownTube(MDFloatLayout):
    pass
           

                                                           
class  DownBlock(MDScreen):    
    def on_enter(self):
       self.app = MDApp.get_running_app() 
            
    def unblock(self):
       self.app.appcheck = self.ids.inpcode.text
       if self.app.checkcode():
           self.app.ChangeScreenMain("MainScreen")
           self.app.SaveSetting()
       else:
           showmessage(" Código incorrecto intentelo de nuevo.", "error")


                 
class  DownWait(MDScreen):
    pass


                                                            
class  DownMain(MDScreen):    
    activated = BooleanProperty(False)
    videoname = StringProperty("")
    imgsource = StringProperty("")
    qualitymenu = None
    
    def on_enter(self):
       self.app = MDApp.get_running_app()   
                       
    def cleanall(self):
        self.activated = False
       
    def cheakpage(self):
        if self.ids.url_input.text == "": 
            showmessage(f'La URL no puede estar vacía.', tipo = "info")
            return
        url = self.ids.url_input.text.strip() 
        try:
            info = getvideoinfo(url)
            self.videoname = info.get('title', 'titulo_desconocido')    
            self.ids.miniatura.source = info.get("thumbnail")
            self.formatdict = getformatsizes(info)
            lista = list(reversed(self.formatdict.keys()))
            self.ids.quality.text = str(lista[0])
            menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in lista]
            self.qualitymenu = MDDropdownMenu(
            caller=self.ids.quality,
            items=menu_items,
            width_mult=4,
        )
            self.activated = True
        except Exception as e:
            self.activated = False  
            if "Failed to establish a new connection" in str(e):
                msg = "Failed to establish a new connection. Connection refused"
            else:
                msg = str(e)
            showmessage(f'No se podido obtener del video. Compruebe la url y la conexión.     Error: "{msg}"', tipo = "error")
            self.app.write_hist_down( "Ver info de la url", "error",msg, url)   
    
    def start_download(self):
        url = self.ids.url_input.text.strip() 
        format = self.formatdict.get(self.ids.quality.current_item)            
        if not url:
            showmessage(f'La URL no puede estar vacía.', tipo = "error")
            return    
        downloadvideo(url, self.app.download_path, 
        format=format,
        showsms =self.app.showsmsdown, 
         subtitles= self.app.subtitles,
          progress_callback=self.app.progress_hook,
          postprocessor_callback=self.app.postprocessor_callback, 
          proxy=self.app.proxy,     
          retries=self.app.retries, bypass_country=self.app.geopass,
          )
        self.app.ChangeScreenMain("WaitScreen")

    def set_item(self, text_item):
        self.ids.quality.set_item(text_item)
        self.qualitymenu.dismiss()                  
                                                           
                                                                      
           
class  DownSetting(MDScreen):
    maincolor = ColorProperty((0,0,1))
    intensit = [  '200', '300', '400', '500', '600', '700', '800', '900']
    def on_enter(self):
        self.colorprin = None
        self.app = MDApp.get_running_app()
        self.maincolor = colors[self.theme_cls.primary_palette]["500"]
        self.resetresetscreen() 
        self.setcolorsmenu()
                           
    def guardar(self):
        if self.ids.retries.text == "" or int(self.ids.retries.text ) <= 0:
           showmessage("Los reintentos tienen que ser un número positivo mayor que cero.", tipo = "error")
           return
        self.app.proxy = self.ids.proxietext.text
        self.app.subtitles = self.ids.subtitles.text
        self.app.geopass = self.ids.geopass.text
        self.app.retries = int(self.ids.retries.text)
        self.app.download_path = self.ids.download_path.text
        self.app.darkmode = self.ids.darkradio.active
        self.theme_cls.primary_palette = self.ids.maincolor.current_item
        self.theme_cls.primary_hue = self.intensit[int(self.ids.mainslider.value)]
        #self.theme_cls.accent_palette = self.ids.seccolor.current_item   
        self.app.histodict["start"] = self.ids.startradio.active
        self.app.histodict["close"] = self.ids.endradio.active
        self.app.histodict["setting"] = self.ids.settingradio.active
        if self.app.histodict["setting"] :Clock.schedule_once(lambda dt:  self.app.write_hist_down( "Guardado de configuración", type="succes"))
        self.theme_cls.theme_style = "Dark" if self.app.darkmode else "Light"
        self.app.SaveSetting()
        showmessage('Configuraciones guardadas correctamente', tipo = "succes")
                        
    def resetresetscreen(self):
        self.ids.download_path.text = self.app.download_path
        self.ids.darkradio.active = self.app.darkmode 
        self.ids.mainslider.value = self.intensit.index(self.theme_cls.primary_hue ) 
        self.ids.maincolor.set_item(self.theme_cls.primary_palette)
        #self.ids.seccolor.set_item(self.theme_cls.accent_palette)
        self.ids.startradio.active = self.app.histodict["start"] 
        self.ids.endradio.active = self.app.histodict["close"] 
        self.ids.settingradio.active = self.app.histodict["setting"]
        self.ids.proxietext.text = self.app.proxy
        self.ids.subtitles.text = self.app.subtitles
        self.ids.geopass.text = self.app.geopass 
        self.ids.retries.text = str(self.app.retries)
 
                   
    def set_main_color(self, text_color ):
        if not text_color: return
        self.ids.maincolor.set_item(text_color)
        val = int(self.ids.mainslider.value)
        self.maincolor =colors[text_color][self.intensit[val]]
        if self.colorprin:
            self.colorprin.dismiss()                  

    def set_sec_color(self, text_color):
        #self.ids.seccolor.set_item(text_color)
        self.colorsec.dismiss()  
                                                           
    def setcolorsmenu(self):
        colorpri = []    
        colorsec = []    
        for i in palette:
           colorpri.append({
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "theme_text_color": "Custom",
                "text_color": colors[i]["500"],
                "on_release": lambda x=f"{i}": self.set_main_color(x),})
           colorsec.append({
                "viewclass": "OneLineListItem",
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_sec_color(x),})     
        self.colorprin = MDDropdownMenu(
            caller=self.ids.maincolor,
            items=colorpri,
            width_mult=4 ) 
        self.colorsec = MDDropdownMenu(
            #caller=self.ids.seccolor,
            items=colorsec,
            width_mult=4)     
         
    def searchpath(self):
       open_selector("Seleccione donde se harán las descargar de los videos.", is_folder=True, path='/storage/emulated/0/', callback = self.savepath)     
       
    def savepath(self, path):
        self.ids.download_path.text = path
        
        
        
class  DownAbout(MDScreen):
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.timewait = 0 
        
    def setsettime(self):
        self.timewait = datetime.now()+timedelta(seconds=3.5)
        
    def cheaktime(self):
        if self.app.appmode >= 2:
            ahora =  datetime.now()
            if self.timewait != 0 and ahora >= self.timewait: 
                self.app.ChangeScreenMain("VaulScreen")    


class ItemHist(MDCard):
    icon = StringProperty("")
    fecha = StringProperty("")
    accion = StringProperty("")
    extra = StringProperty("")
    color_accion = ColorProperty((0,1,0))
    index =NumericProperty(0) 

                 
                                                   
class  DownHistory(MDScreen):
    cachelist = ListProperty([])
    page = NumericProperty(0)
    histolen = NumericProperty(0)
    
    def on_enter(self):
        self.app = MDApp.get_running_app()
        Clock.schedule_once(lambda dt: self.showhist())
        self.allhisto = self.readhisto()
        self.histolen = len(self.allhisto)
        

    def showhist(self):
        icolist= {
        "info":    ("information",   (0.2, 0.6, 1, 1)),
        "succes": ("check-circle", (0.2, 0.8, 0.3, 1)),
        "error":   ("alert-circle", (0.9, 0.2, 0.2, 1)),
        "warning": ("alert", (1, 0.7, 0.1, 1)),  
        }
        lenpage = self.page * self.app.pagelen
        histo = self.allhisto[lenpage:lenpage+self.app.pagelen]
        if self.cachelist == histo:
            return
        self.cachelist = histo
        data = []
        for j, i in enumerate(histo):
            fecha = datetime.fromtimestamp(float(i[0])).strftime("%d/%m/%Y %I:%M:%S %p")
            data.append({
                'icon': icolist[i[1]][0],
                'index': j,
                'fecha': fecha,
                'accion':  str(i[2]),
                'extra': str(i[3]),
                'color_accion':icolist[i[1]][1],
            })
        self.ids.rv_hist.data = data        
   
    def readhisto(self):
        if not Path(self.app.histodown ).exists():
            return([])
        with open(self.app.histodown, "rt") as fh:
            histtemp = fh.read().split("\n")
        histores = []
        for i in reversed( histtemp):
                dec = i.split("|")
                if dec!= [""]:
                    histores.append(dec)
        return histores   
        
    def histopath(self):
        open_selector("Seleccione la carpeta donde guardar el historial.", path='/storage/emulated/0/', callback = self.savehisto)
        
    def savehisto(self, path):
       dir = os.path.join(path,"histo.txt")
       with open(dir,"at") as f:
            for i in self.readhisto():
                fecha = datetime.fromtimestamp(float( i[0])).strftime("%d/%m/%Y %I:%M:%S %p")
                f.write(f"{i[1]}  {fecha}  {i[2]}  {i[3]}\n" )   

    def erasehisto(self):
        try:
            open(self.app.histodown, "w").close()
            self.ids.rv_hist.data = []    
            showmessage("Historial borrado correctamente", "succes")
        except:
            showmessage("Ha ocurrido un error al eliminar el historial", "error")


          
class  DownCheckSum(MDScreen):
    sal2 = StringProperty("")
    sal1 = StringProperty("")
    error = StringProperty("")
    anterior = StringProperty("")
    def on_enter(self):
        self.app = MDApp.get_running_app() 
       
    def writefile(self, text):
        fecha = datetime.now()
        text = f"{ str(fecha.timestamp()) }|{text}"
        text = base64.b64encode(text.encode()).decode()+"\n"
        with open(self.app.checksumhisto,"at") as f:
            f.write(text)
          
    def readfile(self, text):
        if not Path(self.app.checksumhisto).exists():
            return("")
        histobin = ""
        with open(self.app.checksumhisto, "rt") as fh:
            histtemp = fh.read().split("\n")
        for i in reversed(histtemp):
                dec = base64.b64decode(i.encode()).decode().split("|")
                if dec != [""] and dec[1] == text:
                    fecha = datetime.fromtimestamp(float(dec[0])).strftime("%d/%m/%Y %I:%M:%S %p")
                    return  f"visto el {fecha}"
        return histobin
        
    def check(self):
        txt = self.ids.input.text     
        if not txt: return  
        self.anterior = self.readfile(txt)
        self.sal1 = cipher.CipherFernet(txt, "1")
        self.sal2 = cipher.CipherFernet(txt, "2")
        self.writefile(txt)
            
          
class  MainVaul(MDScreen):
    def on_enter(self):
        self.app = MDApp.get_running_app()        
        