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


class DataSaver(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout()
        self.elements = {}

        # Создаем 5 полей ввода
        for i in range(1, 6):
            key = f'Ключ {i}'
            value_input = QLineEdit()
            self.elements[key] = value_input
            self.layout.addRow(f'{key}:', value_input)

        self.save_button = QPushButton("Сохранить данные")
        self.save_button.clicked.connect(self.save_data)

        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def save_data(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить данные", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'a') as f:
                for i, (key, value) in enumerate(self.elements.items(), start=1):
                    f.write(f"{i}: {key} = {value.text()}n")
                f.write("n")  # Отделяем записи пустой строкой


class ListReader(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.list_widget = QListWidget()

        self.read_button = QPushButton("Читать файл")
        self.read_button.clicked.connect(self.read_file)

        self.layout.addWidget(self.read_button)
        self.layout.addWidget(self.list_widget)
        self.setLayout(self.layout)

    def read_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as f:
                lines = f.readlines()
                self.list_widget.clear()
                for line in lines:
                    self.list_widget.addItem(line.strip())

                if len(lines) >= 2:
                    second_element = lines[1].strip()
                    self.list_widget.addItem(f"Поле 2: {second_element}")

class FormSaver(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout()
        self.elements = {}

        # Создаем 5 полей ввода с разными ключами
        for i in range(1, 6):
            key = f'Элемент {i}'
            value_input = QLineEdit()
            self.elements[key] = value_input
            self.layout.addRow(f'{key}:', value_input)

        self.save_button = QPushButton("Сохранить в файл")
        self.save_button.clicked.connect(self.save_to_file)

        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def save_to_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить данные", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'a') as f:
                for i, (key, value) in enumerate(self.elements.items(), start=1):
                    f.write(f"{i}: {key} = {value.text()}n")
                f.write("n---n")  # Отделяем записи

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Приложение на PyQt")

        self.tabs = QTabWidget()

        # Создаем вкладки
        self.file_scanner_tab = FileScanner()
        self.text_editor_tab = TextEditor()
        self.data_saver_tab = DataSaver()
        self.list_reader_tab = ListReader()
        self.form_saver_tab = FormSaver()

        # Добавляем вкладки в TabWidget
        self.tabs.addTab(self.file_scanner_tab, "Сканировать папку")
        self.tabs.addTab(self.text_editor_tab, "Редактировать текст")
        self.tabs.addTab(self.data_saver_tab, "Сохранить данные")
        self.tabs.addTab(self.form_saver_tab, "Сохранить форму")
        self.tabs.addTab(self.list_reader_tab, "Читать файл")


        # Устанавливаем центральный виджет
        self.setCentralWidget(self.tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

