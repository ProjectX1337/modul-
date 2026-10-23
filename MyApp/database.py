import sqlite3


class DatabaseManager:
    def __init__(self, db_name="app_database.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()
        self.ensure_default_admin()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                is_blocked INTEGER DEFAULT 0,
                failed_attempts INTEGER DEFAULT 0
            )
        """)
        self.connection.commit()

    def ensure_default_admin(self):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'Администратор'")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute(
                "INSERT INTO users (login, password, role) VALUES (?, ?, ?)",
                ("admin", "admin", "Администратор")
            )
            self.connection.commit()

    def login_exists(self, login):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE login = ?", (login,))
        return self.cursor.fetchone()[0] > 0

    def authenticate(self, login, password):
        self.cursor.execute(
            "SELECT id, login, role, is_blocked, failed_attempts FROM users WHERE login = ? AND password = ?",
            (login, password)
        )
        return self.cursor.fetchone()

    def get_user_by_login(self, login):
        self.cursor.execute(
            "SELECT id, login, role, is_blocked, failed_attempts FROM users WHERE login = ?",
            (login,)
        )
        return self.cursor.fetchone()

    def increment_failed_attempts(self, login):
        self.cursor.execute(
            "UPDATE users SET failed_attempts = failed_attempts + 1 WHERE login = ?",
            (login,)
        )
        self.connection.commit()
        self.cursor.execute(
            "UPDATE users SET is_blocked = 1 WHERE login = ? AND failed_attempts >= 3",
            (login,)
        )
        self.connection.commit()

    def reset_failed_attempts(self, login):
        self.cursor.execute(
            "UPDATE users SET failed_attempts = 0 WHERE login = ?",
            (login,)
        )
        self.connection.commit()

    def unblock_user(self, user_id):
        self.cursor.execute(
            "UPDATE users SET is_blocked = 0, failed_attempts = 0 WHERE id = ?",
            (user_id,)
        )
        self.connection.commit()

    def add_user(self, login, password, role):
        try:
            self.cursor.execute(
                "INSERT INTO users (login, password, role) VALUES (?, ?, ?)",
                (login, password, role)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_users(self):
        self.cursor.execute("SELECT id, login, role, is_blocked FROM users")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()