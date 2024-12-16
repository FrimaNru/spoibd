import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QFileDialog, QListWidget, QLabel,
    QLineEdit, QFormLayout
)

class FileScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.button = QPushButton("Сканировать папку")
        self.button.clicked.connect(self.scan_folder)
        self.list_widget = QListWidget()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

    def scan_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            files = os.listdir(folder)
            self.list_widget.clear()
            self.list_widget.addItems(files)


class TextEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.open_button = QPushButton("Открыть файл")
        self.save_button = QPushButton("Сохранить файл")

        self.open_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_file)

        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as f:
                content = f.read()
                self.text_edit.setPlainText(content)

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.text_edit.toPlainText())


class BotFileEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.open_button = QPushButton("Открыть файл бота")
        self.save_button = QPushButton("Сохранить файл бота")

        self.open_button.clicked.connect(self.open_file)
        self.save_button.clicked.connect(self.save_file)

        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл бота", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as f:
                content = f.read()
                self.text_edit.setPlainText(content)

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл бота", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.text_edit.toPlainText())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение на PyQt")

        self.tabs = QTabWidget()

        # Создаем вкладки
        self.file_scanner_tab = FileScanner()
        self.text_editor_tab = TextEditor()
        self.bot_file_editor_tab = BotFileEditor()

        # Добавляем вкладки в TabWidget
        self.tabs.addTab(self.file_scanner_tab, "Сканировать папку")
        self.tabs.addTab(self.text_editor_tab, "Редактировать текст")
        self.tabs.addTab(self.bot_file_editor_tab, "Редактировать файл бота")

        # Устанавливаем центральный виджет
        self.setCentralWidget(self.tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())