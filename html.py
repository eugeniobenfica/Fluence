import os
import re

class HTML:
    def __init__(self, html_file: str, html_folder: str = 'htmls', html_sync: bool = True):
        if not os.path.isfile(html_file):
            raise FileNotFoundError(f"'{html_file}' não encontrado.")

        self.file = html_file
        self.file_name, self.file_extension = os.path.splitext(os.path.basename(html_file))
        self.html_file = os.path.join(html_folder, f"{self.file_name}.html")
        self.html_content = ''
        self.html_sync = html_sync
        self.html_folder = html_folder

        if not os.path.exists(html_folder):
            os.makedirs(html_folder)

        if not os.path.exists(self.html_file):
            with open(self.html_file, 'w', encoding='utf-8') as f, open(self.file, 'r', encoding='utf-8') as file:
                self.html_content = file.read()
                f.write(self.html_content)
        else:
            with open(self.html_file, 'r', encoding='utf-8') as f:
                self.html_content = f.read()

    def insert(self, **kwargs):
        if self.html_sync:
            with open(self.file, 'r', encoding='utf-8') as f:
                html_content = f.read()
        else:
            with open(f'{self.html_folder}\\{self.file_name}{self.file_extension}', 'r', encoding='utf-8') as f:
                html_content = f.read()

        if self.html_sync:
            for key, value in kwargs.items():
                html_content = html_content.replace(f"## {key} ##", value)

            if html_content != self.html_content:
                with open(f'{self.html_folder}\\{self.file_name}{self.file_extension}', 'w', encoding='utf-8') as file:
                    file.write(self.html_content)

        if self.html_sync:
            with open(self.html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

        self.html_content = html_content
        return self.html_content

    def export(self):
        if self.html_sync:
            with open(self.html_file, 'r', encoding='utf-8') as file:
                origin = file.read()

            if origin != self.html_content:
                with open(f'{self.html_folder}\\{self.file_name}{self.file_extension}', 'w', encoding='utf-8') as file:
                    file.write(self.html_content)

        return self.html_content