import json

class Parser:

    def  __init__(self, file):
        self._current_file = file
        self.all_article = set()
        self.data_product = []
        self.current_index = 0
        self.save_information = True

    def upload_data_json(self, file):
        """Загружает данные из файла"""
        if file:
            self._current_file = file
        else:
            print("Ошибка: необходимо указать файл")

            return None

        try:
            data = self.read_json(file)

            if isinstance(data, dict):
                self.data_product = [data]
            elif isinstance(data, list):
                self.data_product = data
            else:
                print(f"Ошибка: неподдерживаемый тип данных {type(data)}")

                return None

            self.all_article.clear()

            for product in self.data_product:
                if 'article_number' in product:
                    self.all_article.add(product['article_number'])

            self.current_index = 0

            print(f"Загружено {len(self.data_product)} товаров из файла {self._current_file}")

        except FileNotFoundError:
            print('Файл не найден.')

            return None
        except json.JSONDecodeError:
            print(f'Файл {file} json не может быть представлен в виде JSON.')

            return None

    def upload_data_txt(self, file):
        file = file.replace('.json', '.txt')
        try:
            self.data_product = self.read_txt(file)

            self.all_article.clear()
            for product in self.data_product:
                if 'article_number' in product:
                    self.all_article.add(product['article_number'])
            self.current_index = 0

            if self.save_information:
                self.write_json(file, self.data_product)
        except FileNotFoundError:
            print('Файл не найден')

            return

    def upload_data(self, file):
        """Автоматически определяет тип файла по расширению"""
        if not file:
            print("Ошибка. Необходимо указать файл.")

            return

        if file[-5:] == '.json':
            self.upload_data_json(file)
        elif file[-4:] == '.txt':
            self.upload_data_txt(file)
        else:
            print(f"Неподдерживаемый тип файла: {file}")

    @staticmethod
    def write_json(file,new_data) -> None:
        """Записывает объект в JSON файл

        Args:
            file: название файла.
            new_data: новые данные.
        """

        try:
            with open(file, 'w', encoding='utf-8') as fis:
                json.dump(new_data, fis, indent=4, ensure_ascii=False)
                print(f"Данные сохранены в файл {file}")

        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {file} не найден.")
        except PermissionError:
            raise PermissionError(f"Нет прав на запись в {file}.")
        except TypeError:
            raise TypeError("Данные не могут быть сериализованы в JSON.")

    @staticmethod
    def read_json(file) -> dict:
        """Открывает JSON файл"""
        try:
            with open(file, 'r', encoding='utf-8') as fis:
                data = json.load(fis)
            return data

        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {file} не найден.")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Файл {file} не может быть представлен в виде JSON.")
        except PermissionError:
            raise PermissionError(f"Нет прав на чтение файла {file}.")

    @staticmethod
    def read_txt(file) -> list:
        """Чтение из TXT"""

        all_data = []
        try:
            with open(file, 'r', encoding='utf-8') as fis:
                for number_line, line in enumerate(fis, 1):
                    line = line.strip()

                    if not line:
                        continue

                    if ',' in line:
                        parts = line.split(',')
                    elif ';' in line:
                        parts = line.split(';')
                    else:
                        parts = line.split(' ')

                    clean_parts = []

                    for part in parts:
                        cleared_line = part.strip()
                        if cleared_line != '':
                            clean_parts.append(cleared_line)

                    if len(clean_parts) >= 11:

                        try:
                            all_data.append({
                                'name': clean_parts[0],
                                'count': int(clean_parts[1]),
                                'manufacturer': clean_parts[2],
                                'cost': int(clean_parts[3]),
                                'region': int(clean_parts[4]),
                                'category': clean_parts[5],
                                'description': clean_parts[6],
                                'characteristic': clean_parts[7],
                                'weight': float(clean_parts[8]),
                                'article_number': int(clean_parts[9]),
                                'color': clean_parts[10],
                            })
                        except ValueError:
                            print(f"Ошибка в строке: {line}")

                    else:
                        print(f"Строка {number_line} содержит меньше 11 полей.")
        except FileNotFoundError:
            raise FileNotFoundError('Файл не найден')
        except PermissionError:
            raise PermissionError(f"Нет прав на чтение файла {file}.")

        print(f"Загружено {len(all_data)} товаров из файла {file}")

        return all_data

