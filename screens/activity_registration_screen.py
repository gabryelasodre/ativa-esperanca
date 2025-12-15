from kivy.uix.screenmanager import Screen
from models.activity_model import Activity


class ActivityRegistrationScreen(Screen):

    def save_activity(self):
        title = self.ids.title.text
        description = self.ids.description.text
        id_aluno = self.ids.id_aluno.text
        date = self.ids.date.text

        if not title or not date:
            return  # depois você pode mostrar popup

        id_atividade = Activity.create(title, description, None, date)
        Activity.register_presence(id_atividade, id_aluno, 1)

        # limpa campos
        self.ids.title.text = ""
        self.ids.description.text = ""
        self.ids.date.text = ""

        # volta pra home
        self.manager.current = "home"
