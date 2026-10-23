from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt
from captcha import PuzzleCaptcha


class LoginWindow(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ООО 'Ромашка' - Авторизация")
        self.setMinimumSize(420, 560)

        main_layout = QVBoxLayout()

        input_group = QGroupBox("Вход в систему")
        form_layout = QFormLayout()

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Введите пароль")

        form_layout.addRow("Логин:", self.login_input)
        form_layout.addRow("Пароль:", self.password_input)
        input_group.setLayout(form_layout)

        captcha_group = QGroupBox("Соберите пазл (капча)")
        captcha_layout = QVBoxLayout()
        self.captcha = PuzzleCaptcha([
            "piece1.png",
            "piece2.png",
            "piece3.png",
            "piece4.png"
        ])
        captcha_layout.addWidget(self.captcha, alignment=Qt.AlignmentFlag.AlignCenter)
        captcha_group.setLayout(captcha_layout)

        self.login_button = QPushButton("Войти")
        self.login_button.setMinimumHeight(40)
        self.login_button.clicked.connect(self.handle_login)

        main_layout.addWidget(input_group)
        main_layout.addWidget(captcha_group)
        main_layout.addWidget(self.login_button)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def handle_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        if not login or not password:
            QMessageBox.warning(
                self, "Ошибка ввода",
                "Поля 'Логин' и 'Пароль' обязательны для заполнения."
            )
            return

        if not self.captcha.is_solved():
            QMessageBox.warning(
                self, "Ошибка капчи",
                "Капча собрана неверно. Попробуйте еще раз."
            )
            self.captcha.reset()
            self.register_failed_attempt(login)
            return

        user = self.db.authenticate(login, password)

        if not user:
            QMessageBox.critical(
                self, "Ошибка авторизации",
                "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные"
            )
            self.register_failed_attempt(login)
            self.captcha.reset()
            return

        user_id, user_login, role, is_blocked, failed_attempts = user

        if is_blocked:
            QMessageBox.critical(
                self, "Блокировка",
                "Вы заблокированы. Обратитесь к администратору"
            )
            return

        QMessageBox.information(
            self, "Успех",
            "Вы успешно авторизовались"
        )
        self.db.reset_failed_attempts(login)
        self.open_workspace(user_id, user_login, role)

    def register_failed_attempt(self, login):
        if self.db.login_exists(login):
            self.db.increment_failed_attempts(login)

    def open_workspace(self, user_id, user_login, role):
        if role == "Администратор":
            from admin_window import AdminWindow
            self.admin_window = AdminWindow(self.db)
            self.admin_window.show()
        else:
            from user_window import UserWindow
            self.user_window = UserWindow(user_login, role)
            self.user_window.show()
        self.close()