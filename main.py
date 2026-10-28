from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        label = Label(
            text='GitHub Actions APK Builder',
            font_size='24sp'
        )
        layout.add_widget(label)
        
        btn = Button(text='Presionar', size_hint_y=0.3)
        btn.bind(on_press=lambda x: print("✅ Funcionando!"))
        layout.add_widget(btn)
        
        return layout

if __name__ == '__main__':
    TestApp().run()

