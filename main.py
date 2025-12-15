from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from database.db_manager import create_tables
from screens.activity_registration_screen import ActivityRegistrationScreen
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.home_screen import HomeScreen
from screens.student_register_screen import StudentRegisterScreen  # Importação da nova tela
from kivy.lang import Builder

from screens.students_screen import StudentsScreen

class MainApp(App):
    # Armazena as informações do usuário logado globalmente
    logged_user = None

    def build(self):
        create_tables()
        Builder.load_file('assets/style.kv')
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(StudentsScreen(name='student_detail'))
        sm.add_widget(StudentRegisterScreen(name='student_register'))  # Adição da nova tela
        sm.add_widget(ActivityRegistrationScreen(name="activity_register"))

        return sm


if __name__ == '__main__':
    # Garante que o usuário 'coordinator' inicial exista para testes
    from models.user_model import User
    MainApp().run()

    if not User.authenticate('coord@esperanca.org', '123'):
        User.register('Coordenador Teste', 'coord@esperanca.org', '123', 'coordinator')

