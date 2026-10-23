from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLabel,
    QGroupBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class UserWindow(QWidget):
    def __init__(self, login, role):
        super().__init__()
        self.login = login
        self.role = role
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ООО 'Ромашка' - Рабочий стол пользователя")
        self.setMinimumSize(450, 300)

        main_layout = QVBoxLayout()

        welcome = QLabel(f"Добро пожаловать, {self.login}!")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")

        info_group = QGroupBox("Информация об учетной записи")
        info_layout = QFormLayout()
        info_layout.addRow("Логин:", QLabel(self.login))
        info_layout.addRow("Роль:", QLabel(self.role))
        info_layout.addRow("Статус:", QLabel("Активен"))
        info_group.setLayout(info_layout)

        btn_refresh = QPushButton("Обновить данные")
        btn_refresh.clicked.connect(self.refresh_data)

        btn_logout = QPushButton("Выйти")
        btn_logout.clicked.connect(self.close)

        main_layout.addWidget(welcome)
        main_layout.addWidget(info_group)
        main_layout.addWidget(btn_refresh)
        main_layout.addWidget(btn_logout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def refresh_data(self):
        QMessageBox.information(
            self, "Информация",
            "Данные успешно обновлены."
        )