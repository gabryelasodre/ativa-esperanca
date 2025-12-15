from kivy.uix.screenmanager import Screen
from models.student_model import Student

class StudentsScreen(Screen):
    def on_pre_enter(self):
        self.ids.rv_students.data = [
            {"text": student[1], "on_release": lambda x=student: self.open_detail(x)}
            for student in Student.get_all()
        ]

    def open_detail(self, student):
        self.manager.get_screen("student_detail").load_student(student)
        self.manager.current = "student_detail"

