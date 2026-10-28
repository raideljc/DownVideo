"""
DownVideo - Simple Kivy App
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class DownVideoApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text='DownVideo',
            font_size='28sp',
            size_hint_y=0.4
        )
        layout.add_widget(header)
        
        # Botón
        btn = Button(
            text='Descargar Video',
            size_hint_y=0.3
        )
        btn.bind(on_press=self.on_download)
        layout.add_widget(btn)
        
        # Status
        self.status = Label(
            text='Listo',
            font_size='16sp',
            size_hint_y=0.3
        )
        layout.add_widget(self.status)
        
        return layout
    
    def on_download(self, instance):
        self.status.text = '✅ Funcionando desde GitHub Actions!'
        print("Download button pressed")

if __name__ == '__main__':
    DownVideoApp().run()
