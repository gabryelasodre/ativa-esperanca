from kivy.uix.screenmanager import Screen
from models.user_model import User

class LoginScreen(Screen):
    def login_user(self):
        email = self.ids.email.text
        password = self.ids.password.text
        user = User.authenticate(email, password)
        if user:
            self.manager.current = 'home'
        else:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            Popup(title='Erro', content=Label(text='Usuário ou senha inválidos.'), size_hint=(0.6, 0.4)).open()
