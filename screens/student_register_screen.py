from kivy.uix.screenmanager import Screen
from models.student_model import Student
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import datetime


class StudentRegisterScreen(Screen):
    """Tela para cadastrar novos alunos no sistema."""

    def save_student(self):
        name = self.ids.student_name.text
        birth_date_str = self.ids.birth_date.text

        # Validação básica de campos
        if not name or not birth_date_str:
            self.show_popup('Erro', 'Preencha todos os campos.')
            return

        # Tentativa de validar o formato da data
        try:
            # Garante que a data está no formato esperado (AAAA-MM-DD)
            datetime.date.fromisoformat(birth_date_str)
        except ValueError:
            self.show_popup('Erro', 'Formato de Data de Nascimento inválido. Use AAAA-MM-DD.')
            return

        # O enrollment_date é opcional no método register e assume o dia atual
        success = Student.register(name, birth_date_str)

        if success:
            self.show_popup('Sucesso', f'Aluno "{name}" cadastrado com sucesso!')
            # Limpa os campos após o cadastro
            self.ids.student_name.text = ''
            self.ids.birth_date.text = ''
            self.manager.current = 'home'
        else:
            self.show_popup('Erro', 'Falha ao cadastrar aluno. Tente novamente.')

    def show_popup(self, title, message):
        Popup(title=title, content=Label(text=message), size_hint=(0.7, 0.4)).open()