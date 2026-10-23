from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QComboBox, QMessageBox, QGroupBox, QFormLayout
)


class AdminWindow(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        self.load_users()

    def init_ui(self):
        self.setWindowTitle("ООО 'Ромашка' - Панель администратора")
        self.setMinimumSize(750, 550)

        main_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Логин", "Роль", "Заблокирован"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        add_group = QGroupBox("Добавление пользователя")
        form_layout = QFormLayout()

        self.new_login = QLineEdit()
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_role = QComboBox()
        self.new_role.addItems(["Пользователь", "Администратор"])

        form_layout.addRow("Логин:", self.new_login)
        form_layout.addRow("Пароль:", self.new_password)
        form_layout.addRow("Роль:", self.new_role)
        add_group.setLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Добавить пользователя")
        self.btn_add.clicked.connect(self.add_user)

        self.btn_unblock = QPushButton("Разблокировать выбранного")
        self.btn_unblock.clicked.connect(self.unblock_user)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_unblock)

        main_layout.addWidget(self.table)
        main_layout.addWidget(add_group)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def load_users(self):
        users = self.db.get_all_users()
        self.table.setRowCount(len(users))
        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(str(user[0])))
            self.table.setItem(row, 1, QTableWidgetItem(user[1]))
            self.table.setItem(row, 2, QTableWidgetItem(user[2]))
            self.table.setItem(row, 3, QTableWidgetItem("Да" if user[3] else "Нет"))

    def add_user(self):
        login = self.new_login.text().strip()
        password = self.new_password.text().strip()
        role = self.new_role.currentText()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return

        if self.db.login_exists(login):
            QMessageBox.critical(
                self, "Ошибка добавления",
                "Пользователь с таким логином уже существует."
            )
            return

        if self.db.add_user(login, password, role):
            QMessageBox.information(self, "Успех", "Пользователь успешно добавлен.")
            self.load_users()
            self.new_login.clear()
            self.new_password.clear()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить пользователя.")

    def unblock_user(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(
                self, "Предупреждение",
                "Выберите пользователя для разблокировки."
            )
            return

        user_id = int(self.table.item(row, 0).text())
        self.db.unblock_user(user_id)
        QMessageBox.information(self, "Успех", "Пользователь разблокирован.")
        self.load_users()