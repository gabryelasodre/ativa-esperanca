from database.db_manager import connect_db
import datetime


class Student:
    """Gerencia o cadastro e operações relacionadas aos alunos."""

    @staticmethod
    def register(name, birth_date, enrollment_date=None):
        conn = connect_db()
        cursor = conn.cursor()

        if enrollment_date is None:
            # Define a data de hoje como a data de matrícula padrão
            enrollment_date = datetime.date.today().isoformat()

        try:
            cursor.execute(
                "INSERT INTO students (name, birth_date, enrollment_date) VALUES (?, ?, ?)",
                (name, birth_date, enrollment_date)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao cadastrar aluno: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """Retorna uma lista de todos os alunos cadastrados."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, birth_date, enrollment_date, status FROM students ORDER BY name")
        students = cursor.fetchall()
        conn.close()
        return students

    @staticmethod
    def get_by_id(student_id):
        """Retorna os dados de um aluno específico."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, birth_date, enrollment_date, status FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        conn.close()
        return student