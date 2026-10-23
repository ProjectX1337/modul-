import sys
from PyQt6.QtWidgets import QApplication
from database import DatabaseManager
from login_window import LoginWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    db = DatabaseManager()

    window = LoginWindow(db)
    window.show()

    exit_code = app.exec()
    db.close()
    sys.exit(exit_code)