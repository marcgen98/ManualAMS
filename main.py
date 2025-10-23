from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtGui import QIcon
from PyQt6 import uic
import sys
import os


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('main_window.ui'), self)
        self.setWindowIcon(QIcon(resource_path('icon.ico')))

        self.select_button.clicked.connect(self.select_file)
        self.update_button.clicked.connect(self.update_file)

        self.file_path = None
        self.file_lines = []

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Select file',
            '',
            'G-code Files (*.gcode)'
        )

        if file_path:
            self.file_path = file_path
        else:
            self.status_label.setText('No file selected')
            return

        try:
            self.file_lines = open(file_path, 'r').readlines()
            file_name = os.path.basename(file_path)
            self.status_label.setText(f'Selected file: {file_name}')
        except Exception as e:
            self.status_label.setText(f'Error reading file: {e}')

    def update_file(self):
        if not self.file_path or not self.file_lines:
            self.status_label.setText('Select a file first')
            return

        modified_lines = []

        for index, line in enumerate(self.file_lines):
            if line.strip() == '; CP TOOLCHANGE WIPE':
                if index == 0 or self.file_lines[index-1].strip() != 'M400 U1':
                    modified_lines.append('M400 U1\n')
            modified_lines.append(line)

        try:
            with open(self.file_path, 'w') as file:
                file.writelines(modified_lines)
            self.status_label.setText('Operation completed successfully!')
        except Exception as e:
            self.status_label.setText(f'Error writing file: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
