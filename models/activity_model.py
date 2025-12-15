from database.db_manager import connect_db
import datetime


class Activity:
    """Gerencia o registro de atividades e a presença dos alunos."""

    @staticmethod
    def create(title, description, volunteer_id, date=None):
        conn = connect_db()
        cursor = conn.cursor()

        if date is None:
            date = datetime.date.today().isoformat()

        try:
            cursor.execute(
                "INSERT INTO activities (title, description, volunteer_id, date) VALUES (?, ?, ?, ?)",
                (title, description, volunteer_id, date)
            )
            conn.commit()
            return cursor.lastrowid  # Retorna o ID da nova atividade
        except sqlite3.Error as e:
            print(f"Erro ao criar atividade: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """Retorna todas as atividades registradas."""
        conn = connect_db()
        cursor = conn.cursor()
        # Join com a tabela users para mostrar o nome do voluntário
        cursor.execute("""
                       SELECT a.id,
                              a.title,
                              a.date,
                              u.name as volunteer_name
                       FROM activities a
                                JOIN users u ON a.volunteer_id = u.id
                       ORDER BY a.date DESC
                       """)
        activities = cursor.fetchall()
        conn.close()
        return activities

    @staticmethod
    def register_presence(activity_id, student_id, is_present=1):
        """Registra a presença de um aluno em uma atividade."""
        conn = connect_db()
        cursor = conn.cursor()
        date = datetime.date.today().isoformat()

        try:
            cursor.execute(
                "INSERT INTO presence_records (activity_id, student_id, date, is_present) VALUES (?, ?, ?, ?)",
                (activity_id, student_id, date, is_present)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao registrar presença: {e}")
            return False
        finally:
            conn.close()