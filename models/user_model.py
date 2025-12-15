import sqlite3

from database.db_manager import connect_db


class User:
    """Gerencia o cadastro e autenticação de usuários (voluntários, educadores e coordenação)."""

    @staticmethod
    def register(name, email, password, role='volunteer'):
        """
        Cadastra um novo usuário no banco de dados.
        O papel (role) é 'volunteer' por padrão, mas pode ser definido como 'coordinator' ou 'educator'.
        """
        conn = connect_db()
        cursor = conn.cursor()

        # NOTE: O código original NÃO usa hashing de senha. Esta é uma melhoria crítica de segurança.
        # Para fins de demonstração, manterei a lógica original, mas em um projeto real,
        # a senha DEVE ser hasheada (e.g., usando bcrypt).

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                (name, email, password, role)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Email já existe
            return False
        finally:
            conn.close()

    @staticmethod
    def authenticate(email, password):
        """
        Autentica o usuário pelo email e senha.
        Retorna (id, name, email, password, role) ou None.
        """
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, password, role FROM users WHERE email = ? AND password = ?",
                       (email, password))
        user = cursor.fetchone()
        conn.close()
        return user