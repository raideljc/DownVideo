#Pydroid run terminal

from kivy.properties import NumericProperty,ListProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.popup import Popup
import sys, os, tempfile, string, random
import base64
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
#from android.permissions import request_permissions, Permission
#request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
#from kivymd.uix.boxlayout import MDBoxLayout
#from kivymd.uix.button import MDIconButton
#from kivy.metrics import dp

class FilePopup(Popup):
    filter = StringProperty('*')
    texto = StringProperty('')
    dir_mode = BooleanProperty(False)
    start_path = StringProperty('/sdcard/')
    callback = ObjectProperty(None)    
    def aceptar(self, fc):
        if self.dir_mode:
            if self.callback: 
                if fc.selection:
                    self.callback(fc.selection[0])
                else:
                    self.callback(fc.path)
        else:
            if  self.callback: 
                if not(fc.selection and fc.selection[0]):
                    return None
                self.callback(fc.selection[0])
        self.dismiss()

def open_selector( title='', is_folder=True, path= '/storage/emulated/0/', callback = None):
        #MDSnackbar
        popup = FilePopup(
            dir_mode=is_folder,
            start_path=path,
            title="seleccione " +('la carpeta' if is_folder else 'el archivo'),
            texto = title,
            filter='' if is_folder else '*.*'
        )
        popup.callback = callback
        popup.open()
        


def showmessage(mensaje, tipo="info", icono=None):
    colores = {
        "succes": (0.2, 0.8, 0.3, 0.85),
        "error": (0.9, 0.2, 0.2, 0.85),
        "info":  (0.5, 0.5, 0.5 ,0.85),
    }
    Snackbar=MDSnackbar(
        MDLabel(
            text=str(mensaje),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
        ),
        md_bg_color=colores.get(tipo, colores["info"]),
        y="26dp",
        pos_hint={"center_x": 0.5},
        size_hint_x=0.96,
    )
    Clock.schedule_once(lambda dt: Snackbar.open())


def get_default_paths():
        datas = os.path.join(os.getcwd(), 'Datas')
        if sys.platform == 'android':
            from android.storage import primary_external_storage_path
            base = primary_external_storage_path()
            #datas = os.getcwd()
        elif sys.platform == 'win32':
            base = os.environ['USERPROFILE']
        elif os.path.isdir('/storage/emulated/0'):
            base = '/storage/emulated/0'
        else:
            base = os.path.expanduser('~')
        temp = tempfile.gettempdir()
        download = os.path.join(base, 'Download', "DownTube")
        os.makedirs(download, exist_ok=True)
        return {
                'base' : base,
                'download': download,
                'temp': temp,
                'datas' : datas,
            }

def makecode():
    xorcode =  b'unhIKvDPTH7Ur7GKpqz29mp7EXB8tWKBWhvbTvS42f4='
    asletter= string.ascii_letters+string.digits
    code = sys.platform
    if sys.platform == 'android':
       pass
    else:
        import uuid
        #return len(str(uuid.uuid4()))
    lcode = len(code[:64])
    fcode = asletter[lcode]+"".join(random.choice(asletter) for i in range(0, 64-lcode))
    resultado = bytes(x ^ y for x, y in zip(fcode.encode(), xorcode))
    return base64.b64encode(resultado).decode()
    
def geticon(nombre):
    if not nombre or '.' not in nombre:
        return 'file'
    ext = nombre.rsplit('.', 1)[-1].lower()
    mapa = {
        # ---------- DOCUMENTOS ----------
        'pdf':  'file-pdf-box',
        'doc':  'file-word-box',      'docx': 'file-word-box',
        'odt':  'file-document',      'rtf':  'file-document',
        'txt':  'file-document-outline',
        'md':   'language-markdown',  'markdown': 'language-markdown',
        'tex':  'file-document',      'log':  'file-document-outline',
        'epub': 'book-open-page-variant',
        'mobi': 'book-open-page-variant',
        'djvu': 'book-open-page-variant',
  # ---------- HOJAS DE CÁLCULO ----------
        'xls':  'file-excel-box',  'xlsx': 'file-excel-box',
        'xlsm': 'file-excel-box',  'ods':  'file-chart',
        'csv':  'file-delimited',  'tsv':  'file-delimited',
      # ---------- PRESENTACIONES ----------
        'ppt':  'file-powerpoint-box', 'pptx': 'file-powerpoint-box',
        'odp':  'file-powerpoint-box', 'key':  'file-powerpoint-box',
        # ---------- IMÁGENES ----------
        'jpg':  'file-image', 'jpeg': 'file-image',
        'png':  'file-image', 'gif':  'file-image',
        'bmp':  'file-image', 'tiff': 'file-image', 'tif': 'file-image',
        'webp': 'file-image', 'svg':  'svg',         'ico': 'file-image',
        'heic': 'file-image', 'raw':  'file-image',  'psd': 'file-image',
        'ai':   'file-image', 'xcf':  'file-image',
        # ---------- AUDIO ----------
        'mp3':  'file-music', 'wav':  'file-music',
        'flac': 'file-music', 'aac':  'file-music',
        'ogg':  'file-music', 'oga':  'file-music',
        'm4a':  'file-music', 'wma':  'file-music',
        'opus': 'file-music', 'mid':  'file-music', 'midi': 'file-music',
        'aiff': 'file-music',
        # ---------- VIDEO ----------
        'mp4':  'file-video', 'avi':  'file-video',
        'mkv':  'file-video', 'mov':  'file-video',
        'wmv':  'file-video', 'flv':  'file-video',
        'webm': 'file-video', 'm4v':  'file-video',
        'mpg':  'file-video', 'mpeg': 'file-video',
        '3gp':  'file-video', 'ts':   'file-video',
        # ---------- COMPRIMIDOS ----------
        'zip':  'zip-box',    'rar':  'zip-box',
        '7z':   'zip-box',    'tar':  'zip-box',
        'gz':   'zip-box',    'bz2':  'zip-box',
        'xz':   'zip-box',    'tgz':  'zip-box',
        'iso':  'disc',       'img':  'disc',
        # ---------- CÓDIGO / DESARROLLO ----------
        'py':   'language-python',      'pyw': 'language-python',
        'ipynb':'language-python',
        'js':   'language-javascript',  'mjs': 'language-javascript',
        'ts':   'language-typescript',
        'jsx':  'react',                'tsx': 'react',
        'html': 'language-html5',       'htm': 'language-html5',
        'css':  'language-css3',        'scss':'language-css3',
        'sass': 'language-css3',        'less':'language-css3',
        'c':    'language-c',           'h':   'language-c',
        'cpp':  'language-cpp',         'hpp': 'language-cpp',
        'cc':   'language-cpp',         'cxx': 'language-cpp',
        'cs':   'language-csharp',
        'java': 'language-java',
        'kt':   'language-kotlin',      'kts': 'language-kotlin',
        'swift':'language-swift',
        'go':   'language-go',
        'rs':   'language-rust',
        'php':  'language-php',
        'rb':   'language-ruby',
        'pl':   'language-perl',        'pm':  'language-perl',
        'lua':  'language-lua',
        'r':    'language-r',
        'dart': 'language-dart',
        'scala':'language-scala',
        'hs':   'language-haskell',
        'clj':  'language-clojure',
        'sh':   'bash',                 'bash':'bash',
        'zsh':  'bash',                 'fish':'bash',
        'ps1':  'powershell',           'bat': 'console',
        'cmd':  'console',
        'sql':  'database',
        'json': 'code-json',            'yaml':'file-code',
        'yml':  'file-code',            'toml':'file-code',
        'xml':  'file-xml',             'ini': 'file-cog',
        'cfg':  'file-cog',             'conf':'file-cog',
        'env':  'file-cog',
        # ---------- EJECUTABLES / SISTEMA ----------
        'exe':  'application',      'msi': 'application',
        'apk':  'android',           'aab': 'android',
        'app':  'apple',             'dmg': 'apple',
        'deb':  'linux',             'rpm': 'linux',
        'appimage': 'linux',        'bin': 'application',
        'dll':  'application',       'so':  'application',
        'o':    'application',       'class':'application',
        # ---------- FUENTES ----------
        'ttf':  'format-font', 'otf': 'format-font',
       'woff': 'format-font', 'woff2': 'format-font',
        'eot':  'format-font',
        # ---------- DATOS / BASES DE DATOS ----------
        'db':   'database', 'sqlite': 'database',
        'sqlite3': 'database', 'mdb': 'database',
        'accdb':'database',
        # ---------- 3D / CAD ----------
        'obj':  'cube-outline', 'stl': 'cube-outline',
        'fbx':  'cube-outline', 'blend': 'blender',
       'dae':  'cube-outline', '3ds': 'cube-outline',
        'dwg':  'vector-square', 'dxf': 'vector-square',
        # ---------- DISEÑO / OTROS ----------
        'fig':  'vector-square', 'sketch': 'vector-square',
        'xd':   'vector-square', 'indd': 'file-document',
        # ---------- CERTIFICADOS / SEGURIDAD ----------
        'pem':  'file-lock', 'crt':  'file-lock',
        'cer':  'file-lock', 'key':  'key',
        'p12':  'file-lock', 'pfx':  'file-lock',
        # ---------- TORRENT / RED ----------
        'torrent': 'download-network',
        'ovpn':    'vpn',
    }
    return mapa.get(ext, 'file')
    
    
def savehelp(obj):
    with open("help.txt") as f:
        f.write(help(obj))
        #print(help(MDApp.theme_cls))