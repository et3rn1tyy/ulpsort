import concurrent.futures
from pathlib import Path
from tqdm import tqdm
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QProgressBar,
    QVBoxLayout, QHBoxLayout, QFileDialog, QSpinBox, QMessageBox
)

# Support me: https://t.me/et3rn1tybio/6
# LOLZ: zelenka.guru/members/892533/
# TG: t.me/@et3rn1ty_m
# Version 1.0.0.0 (20/10/23)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ULPSort by Eternity")
        self.file_label = QLabel("Файл:")
        self.file_edit = QLineEdit()
        self.file_button = QPushButton("Выбрать файл")
        self.keyword_label = QLabel("Ключевая фраза:")
        self.keyword_edit = QLineEdit()
        self.save_label = QLabel("Сохранить в:")
        self.save_edit = QLineEdit()
        self.save_button = QPushButton("Выбрать путь")
        self.thread_label = QLabel("Количество потоков:")
        self.thread_spinbox = QSpinBox()
        self.search_button = QPushButton("Найти")
        self.result_label = QLabel("Результат:")
        self.result_edit = QTextEdit()
        self.progress_bar = QProgressBar()
        self.link_label = QLabel('Code writen 10/20/2023 | <a href="https://zelenka.guru/members/892533/">LOLZTEAM</a>   |  <a href="https://t.me/@et3rn1ty_m">Telegram</a>')
        self.link_label.setOpenExternalLinks(True)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_edit)
        file_layout.addWidget(self.file_button)

        keyword_layout = QHBoxLayout()
        keyword_layout.addWidget(self.keyword_label)
        keyword_layout.addWidget(self.keyword_edit)

        save_layout = QHBoxLayout()
        save_layout.addWidget(self.save_label)
        save_layout.addWidget(self.save_edit)
        save_layout.addWidget(self.save_button)

        thread_layout = QHBoxLayout()
        thread_layout.addWidget(self.thread_label)
        thread_layout.addWidget(self.thread_spinbox)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.search_button)

        result_layout = QVBoxLayout()
        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.result_edit)
        result_layout.addWidget(self.progress_bar)

        link_layout = QHBoxLayout()
        link_layout.addWidget(self.link_label)

        main_layout = QVBoxLayout()
        main_layout.addLayout(file_layout)
        main_layout.addLayout(keyword_layout)
        main_layout.addLayout(save_layout)
        main_layout.addLayout(thread_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(result_layout)
        main_layout.addLayout(link_layout)

        self.setLayout(main_layout)

        self.file_button.clicked.connect(self.choose_file)
        self.save_button.clicked.connect(self.choose_save_path)
        self.search_button.clicked.connect(self.search)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл")
        self.file_edit.setText(file_path)

    def choose_save_path(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Выбрать путь")
        self.save_edit.setText(save_path)

    def search(self):
        file_path = self.file_edit.text()
        keyword = self.keyword_edit.text()
        save_path = self.save_edit.text()
        num_threads = self.thread_spinbox.value()

        if not Path(file_path).is_file():
            self.result_edit.setText("Файл не найден.")
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                results = [executor.submit(find_keyword, line, keyword) for line in lines]

                with open(save_path, 'w', encoding='utf-8') as save_file, tqdm(total=len(lines)) as progress_bar:
                    count = 0
                    for future in concurrent.futures.as_completed(results):
                        if future.result() is not None:
                            count += 1
                            save_file.write(future.result() + '\n')
                            self.result_edit.append(future.result())
                        progress_bar.update(1)
                        self.progress_bar.setValue(progress_bar.n)
                        QApplication.processEvents()

                    self.result_edit.append(f"Найдено строк: {count}")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
