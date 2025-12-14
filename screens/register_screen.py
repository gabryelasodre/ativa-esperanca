from kivy.uix.screenmanager import Screen
from models.user_model import User

class RegisterScreen(Screen):
    def register_user(self):
        name = self.ids.name.text
        email = self.ids.email.text
        password = self.ids.password.text
        User.register(name, email, password)
        self.manager.current = 'login'
