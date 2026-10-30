
#wPydroid run terminal

import os
import base64
from kivy.app import App
from kivy.lang import Builder
from cipher import cipher
from kivy.properties import StringProperty
from cryptography.fernet import Fernet
from datetime import datetime
from pathlib import Path 
KV = """
BoxLayout:
    orientation: "vertical"
    size_hint: (0.8, 0.6)
    pos_hint: {'center_y': 0.5, 'center_x': 0.5}
    BoxLayout:
        size_hint_y:0.15
        orientation: "vertical"
        Label:
            text: "codigo" 
        TextInput:
            id: input
    BoxLayout:
        size_hint_y:0.1
        orientation: "vertical"
        Button:
            on_release: app.check() 
    BoxLayout:
        size_hint_y:0.05
        orientation: "vertical"
        Label:
            text: app.anterior
    BoxLayout:
        size_hint_y:0.3
        orientation: "vertical"
        padding: 5
        Label:
            size_hint_y:0.2
            text: "version 1" 
        TextInput:
            text: app.sal1
            readonly: True
    BoxLayout:
        size_hint_y:0.3
        orientation: "vertical"
        Label:
            size_hint_y:0.2
            text: "version 2" 
        TextInput:
            text: app.sal2
            readonly: True
    BoxLayout:
        size_hint_y:0.3
        orientation: "vertical"
        Label:
            size_hint_y:0.2
            text: "version 3" 
        TextInput:
            text: app.sal3
            readonly: True
"""
class MiApp(App):
    sal2 = StringProperty("")
    sal1 = StringProperty("")
    sal3 = StringProperty("")
    error = StringProperty("")
    anterior = StringProperty("")
    savefile = StringProperty("datas/checksum.pyc")
    
    def writefile(self, text):
        fecha = datetime.now()
        text = f"{ str(fecha.timestamp()) }|{text}"
        text = base64.b64encode(text.encode()).decode()+"\n"
        with open(self.savefile,"at") as f:
            f.write(text)
        
    
    def readfile(self, text):
        if not Path(self.savefile ).exists():
            return("")
        histobin = ""
        with open(self.savefile , "rt") as fh:
            histtemp = fh.read().split("\n")
        for i in reversed(histtemp):
                dec = base64.b64decode(i.encode()).decode().split("|")
                if dec!= [""] and dec[1]== text:
                    fecha = datetime.fromtimestamp(float(dec[0])).strftime("%d/%m/%Y %I:%M:%S %p")
                    return  f"visto el {fecha}"
        return histobin
        
    def check(self):
        txt = self.root.ids.input.text     
        if not txt: return  
        self.anterior = self.readfile(txt)
        
        self.sal1 = cipher.CipherFernet(txt, "1")
        self.sal2 = cipher.CipherFernet(txt, "2")
        self.sal3 = cipher.CipherFernet(txt, "3")
        self.writefile(txt)
        
    def build(self):
        screen = Builder.load_string(KV)
        return screen

MiApp().run()
