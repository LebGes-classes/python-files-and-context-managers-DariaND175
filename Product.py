import random
import json
from Parser import Parser


class Product(Parser):
    """Класс для карточки товара"""

    all_article = set()

    def __init__(self, file) -> None:
        """Инициализатор класса.

            Args:
                file: файл с данными о товарах

        """

        super().__init__(file)
        self.upload_data(file)

    def add_line_info(self,line) -> None:
        """Добавить данные из строки"""

        keys = [
            'name', 'count', 'manufacturer', 'cost',
            'region', 'category', 'description', 'characteristic',
            'weight', 'article_number', 'color'
        ]
        values = [part.strip() for part in line.split(';')]

        if len(values) != len(keys):
            print(f"Ошибка: ожидалось {len(keys)} полей, получено {len(values)}")
            return

        new_product = {}
        for key, value in zip(keys, values):
            if key in ['name', 'manufacturer', 'category', 'description', 'characteristic', 'color']:
                new_product[key] = value if value else ''

            elif key == 'count':
                try:
                    if value and value.strip():
                        count_val = int(value)
                        if count_val >= 0:
                            new_product[key] = count_val
                        else:
                            print('Количество не может быть отрицательным')
                            new_product[key] = 0
                    else:
                        new_product[key] = 0
                except ValueError:
                    print('Вводить можно только целые неотрицательные числа')
                    new_product[key] = 0

            elif key == 'cost':
                try:
                    if value and value.strip():
                        cost_str = value.split()[0]
                        cost_val = int(cost_str)
                        if cost_val > 0:
                            new_product[key] = cost_val
                        else:
                            print('Стоимость должна быть положительным числом')
                            new_product[key] = 0
                    else:
                        new_product[key] = 0
                except ValueError:
                    print('Вводить можно только целые положительные числа')
                    new_product[key] = 0

            elif key == 'weight':
                try:
                    if value and value.strip():
                        clean_value = value.split()[0]
                        clean_value = clean_value.replace(',', '.')
                        weight_val = float(clean_value)
                        if weight_val >= 0:
                            new_product[key] = weight_val
                        else:
                            print('Вес не может быть отрицательным')
                            new_product[key] = 0.0
                    else:
                        new_product[key] = 0.0
                except ValueError:
                    print('Вводить можно только неотрицательные числа')
                    new_product[key] = 0.0

            elif key == 'region':
                try:
                    if value and value.strip():
                        region_val = int(value)
                        if 1 <= region_val <= 99 or region_val == 100:
                            new_product[key] = region_val
                        else:
                            print('Такого региона не существует (укажите 1-99 или 100 для зарубежной доставки)')
                            new_product[key] = 0
                    else:
                        new_product[key] = 0
                except ValueError:
                    print('Вводить можно только целые числа')
                    new_product[key] = 0

            elif key == 'article_number':
                if not value or not value.strip():
                    new_product[key] = None
                    print('Артикул будет создан автоматически.')
                else:
                    try:
                        article = int(value)
                        if 10000000 <= article <= 99999999:
                            new_product[key] = article
                        else:
                            print(
                                'Введённый артикул не подходит под параметры. Новый артикул будет создан автоматически')
                            new_product[key] = None
                    except ValueError:
                        print('Вводить можно только числа.')
                        new_product[key] = None

        self.data_product.append(new_product)
        self.current_index = len(self.data_product) - 1
        print(f"Товаров в списке: {len(self.data_product)}")  # Отладка
        print(f"save_information = {self.save_information}")

        if 'article_number' not in new_product or new_product['article_number'] is None:
            self.set_article_number(None)
        else:
            article = new_product['article_number']
            if article not in self.all_article:
                self.data_product[self.current_index]['article_number'] = article
                self.all_article.add(article)
            else:
                print(f'Артикул {article} уже существует. Создаем новый.')
                self.set_article_number(None)


        self.write_json(self._current_file, self.data_product)
        print('Добавлен новый товар.')

    def add_information(self) -> None:
        """Добавить информацию о товаре"""

        new_product = {
            'name': '',
            'count': 0,
            'manufacturer': '',
            'cost': 0,
            'region': 0,
            'category': '',
            'description': '',
            'characteristic': '',
            'weight': 0,
            'article_number': 0,
            'color': ''}

        self.data_product.append(new_product)
        self.current_index = len(self.data_product) - 1

        self.save_information = False
        self.set_name(input("Введите название товара: "))
        self.set_count(int(input("Введите количество товара: ")))
        self.set_manufacturer(input("Введите производителя: "))
        self.set_cost(int(input("Введите стоимость: ")))
        self.set_region(int(input("Введите код региона: ")))
        self.set_category(input("Введите категорию: "))
        self.set_description(input("Введите описание: "))
        self.set_characteristic(input("Введите характеристику: "))
        self.set_weight(float(input("Введите вес (кг): ")))
        self.set_article_number(None)
        self.set_color(input("Введите цвет: "))

        self.save_information = True
        self.write_json(self._current_file,self.data_product)

    def set_name(self, name: str) -> None:
        """ Сеттер для названия товара

        Args:
            name: Наименование товара
        """

        if len(name) == 0:
            print('Введите название товара.')

            self.data_product[self.current_index]["name"] = ''
        else:
            self.data_product[self.current_index]["name"] = name
            if self.save_information:
                self.write_json(self._current_file,self.data_product)

    def set_count(self, count) -> None:
        """ Сеттер для количества товара

        Args:
            count: Количество товара
        """

        try:
            count = int(count)

            if count <= 0:
                print('Введите положительное число.')

                self.data_product[self.current_index]["count"] = 0
            elif count > 10 ** 4:
                print('Введено слишком большое число.')

                self.data_product[self.current_index]["count"] = 0
            else:
                self.data_product[self.current_index]["count"] = count
                if self.save_information:
                    self.write_json(self._current_file,self.data_product)
        except ValueError:
            raise ValueError('Ошибка. Введите корректное количество товара')
        except TypeError:
            raise TypeError('Ошибка типа данных.')

    def set_manufacturer(self, manufacturer: str) -> None:
        """ Сеттер для информации о производителе товара.

        Args:
            manufacturer: Производитель товара
        """

        if len(manufacturer) > 15:
            print('Имя производителя не должно превышать 14 символов.')

            self.data_product[self.current_index]["manufacturer"] = ''
        else:
            self.data_product[self.current_index]["manufacturer"] = manufacturer
            if self.save_information:
                self.write_json(self._current_file,self.data_product)

    def set_cost(self, cost) -> None:
        """ Сеттер для информации о стоимости товара.

        Args:
            cost: Стоимость товара
        """

        try:
            num = float(cost)

            if num != int(num):
                print('Цена должна быть целым числом.')

                self.data_product[self.current_index]["cost"] = 0

                return

            cost = int(cost)

            if cost <= 0:
                print('Пожалуйста, введите положительное число.')

                self.data_product[self.current_index]["cost"] = 0
            elif cost > 10 ** 7:
                print('Введена слишком большая цена.')

                self.data_product[self.current_index]["cost"] = 0
            else:
                self.data_product[self.current_index]["cost"] = cost
                if self.save_information:
                    self.write_json(self._current_file,self.data_product)
        except ValueError:
            raise ValueError('Ошибка.Можно использовать только цифры.')
        except TypeError:
            raise TypeError('Ошибка типа данных.')

    def set_region(self, region) -> None:
        """Сеттер для региона доставки товара

        Args:
            region: Регион, из которого доставляется товар
        """

        try:
            region = int(region)
            if 1 <= region <= 99 or region == 100:
                self.data_product[self.current_index]["region"] = region
                if self.save_information:
                    self.write_json(self._current_file,self.data_product)
            else:
                print('Ошибка! Код региона должен быть от 1 до 99 (или 100- зарубежная доставка)')

                self.data_product[self.current_index]["region"] = 0
        except ValueError:
            print('Введите корректное число.')

            self.data_product[self.current_index]["region"] = 0
        except TypeError:
            print('Ошибка типа данных.')

            self.data_product[self.current_index]["region"] = 0

    def set_category(self, category: str) -> None:
        """Сеттер для категории товара

        Args:
            category: Категория товара
        """

        try:
            if category and category.replace(' ', '').isalpha():
                self.data_product[self.current_index]["category"] = category
                if self.save_information:
                    self.write_json(self._current_file,self.data_product)
            else:
                print('Категория не добавлена. Можно использовать только буквы.')

                self.data_product[self.current_index]["category"] = ''
        except AttributeError:
            print('Объект не имеет метода replace/isalpha.')

            self.data_product[self.current_index]["category"] = ''
        except TypeError:
            print('Ошибка типа данных.')

            self.data_product[self.current_index]["category"] = ''

    def set_description(self, description: str) -> None:
        """Сеттер для описания товара.

        Args:
            description: Описание товара.
        """

        try:
            if description is None or len(description.strip()) == 0:
                print('У товара отсутствует описание.')

                self.data_product[self.current_index]["description"] = ""
            elif len(description) <= 10 ** 4:
                self.data_product[self.current_index]["description"] = description
                if self.save_information:
                    self.write_json(self._current_file,self.data_product)
            else:
                print('Описание не должно содержать больше 10.000 символов.')

                self.data_product[self.current_index]["description"] = ""
        except TypeError:
            print('Ошибка! Можно вводить только текст.')

            self.data_product[self.current_index]["description"] = ""

    def set_characteristic(self, characteristic: str) -> None:
        """Сеттер для характеристики товара.

        Args:
            characteristic: Характеристика товара.
        """

        try:
            if characteristic is None or len(characteristic.strip()) == 0:
                print('У товара отсутствует характеристика.')

                self.data_product[self.current_index]["characteristic"] = ""
            elif len(characteristic) <= 10 ** 4:
                self.data_product[self.current_index]["characteristic"] = characteristic
                if self.save_information:
                    self.write_json(self._current_file,self.data_product)
            else:
                print('Характеристика не должна содержать больше 10.000 символов.')

                self.data_product[self.current_index]["characteristic"] = ""
        except TypeError:
            print('Ошибка! Можно вводить только текст.')
            self.data_product[self.current_index]["characteristic"] = ""

    def set_weight(self, weight) -> None:
        """Сеттер для веса товара.

        Args:
            weight: Вес товара(в кг).
        """

        try:
            weight = float(weight)

            if weight > 1000:
                print('Введен слишком большой вес.')

                self.data_product[self.current_index]["weight"] = 0
            elif weight < 0:
                print('Вес не может быть отрицательным.')

                self.data_product[self.current_index]["weight"] = 0
            else:
                self.data_product[self.current_index]["weight"] = weight
                if self.save_information:
                    self.write_json(self._current_file,self.data_product)
        except TypeError:
            print('Ошибка типа данных.')

            self.data_product[self.current_index]["weight"] = 0
        except ValueError:
            print('Вводить можно только числа.')

            self.data_product[self.current_index]["weight"] = 0

    def set_article_number(self, article_number) -> None:
        """Сеттер для артикула товара.

        Args:
            article_number: Артикул товара.
        """

        if article_number is None:
            random_art = random.randint(10000000, 99999999)

            while random_art in Product.all_article:

                random_art += 1

                if random_art > 99999999:
                    random_art = 10000000

            self.data_product[self.current_index]["article_number"] = random_art
            if self.save_information:
                self.write_json(self._current_file,self.data_product)

            Product.all_article.add(random_art)

            return

        else:
            try:
                article_number = int(article_number)
                if article_number in Product.all_article:
                    print('Такой артикул уже существует.')

                    self.data_product[self.current_index]["article_number"] = 0
                elif len(str(article_number)) == 8:
                    self.data_product[self.current_index]["article_number"] = article_number
                    if self.save_information:
                        self.write_json(self._current_file,self.data_product)

                    Product.all_article.add(article_number)
                else:
                    print('Артикул должен состоять из 8 цифр!')

                    self.data_product[self.current_index]["article_number"] = 0
            except TypeError:
                print('Ошибка типа данных.')

                self.data_product[self.current_index]["article_number"] = 0
            except ValueError:
                print('Некорректное значение.')

                self.data_product[self.current_index]["article_number"] = 0

    def set_color(self, color):
        """Сеттер для цвета товара

        Args:
            color: Цвет товара."""

        colors = ('Красный', 'Жёлтый', 'Зелёный', 'Оранжевый', 'Синий', 'Голубой', 'Фиолетовый', 'Розовый')

        if color.capitalize() in colors:
            self.data_product[self.current_index]["color"] = color.capitalize()
            if self.save_information:
                self.write_json(self._current_file,self.data_product)
        else:
            self.data_product[self.current_index]["color"] = 'Другое'
            if self.save_information:
                self.write_json(self._current_file,self.data_product)

    def get_name(self) -> str:
        """Геттер для наименования товара.

        Returns:
                name: Наименование товара
        """

        return self.data_product[self.current_index].get("name", 'Нет информации.')

    def get_count(self) -> int:
        """Геттер для количества товара.

        Returns:
                count: Количество товара
        """

        return self.data_product[self.current_index].get("count", 0)

    def get_manufacturer(self) -> str:
        """Геттер для производителя товара.

        Returns:
                manufacturer: Производитель товара
        """

        return self.data_product[self.current_index].get("manufacturer", 'Нет информации.')

    def get_cost(self) -> int:
        """Геттер для стоимости товара.

        Returns:
                manufacturer: Стоимость товара
        """

        return self.data_product[self.current_index].get('cost', 0)

    def get_region(self) -> int:
        """Геттер для региона, из которого доставляется товар.

        Returns:
                region: Регион, из которого доставляется товар.
        """

        return self.data_product[self.current_index].get("region", 0)

    def get_category(self) -> str:
        """Геттер для категории товара.

        Returns:
                category: Категория товара.
        """

        return self.data_product[self.current_index].get("category", 'Нет информации.')

    def get_description(self) -> str:
        """Геттер для описания товара.

        Returns:
                description: Описание товара.
        """

        return self.data_product[self.current_index].get("description", 'Нет информации.')

    def get_characteristic(self) -> str:
        """Геттер для характеристики товара.

        Returns:
                characteristic: Характеристика товара.
        """

        return self.data_product[self.current_index].get("characteristic", 'Нет информации.')

    def get_weight(self) -> float:
        """Геттер для веса товара.

        Returns:
                weight: Вес товара(в кг).
        """

        return self.data_product[self.current_index].get("weight", 0)

    def get_article_number(self) -> int:
        """Геттер для веса товара.

        Returns:
                article_number: Артикул товара.
        """

        return self.data_product[self.current_index].get("article_number", 0)

    def get_color(self) -> str:
        """Геттер для цвета товара.

        Returns:
                color: Цвет товара.
        """

        return self.data_product[self.current_index].get("color", 'Нет информации.')

    def condition_product(self) -> None:
        """Состояние товара."""

        if self.get_count() == 0:
            print(f'Товара {self.get_name()} нет в наличии.')
        elif self.get_count() <= 10:
            print(f'Внимание! Товара {self.get_name()} осталось в наличии {self.get_count()} штук.')
        else:
            print(f'Товар {self.get_name()} есть в наличии (осталось {self.get_count()} штук) ')

    def delete_product(self) -> None:
        """Удаление карточки товара."""

        if self.current_index < len(self.data_product):
            article = self.get_article_number()

            if article in Product.all_article:
                Product.all_article.remove(article)

            del self.data_product[self.current_index]

            if self.current_index >= len(self.data_product):
                self.current_index = len(self.data_product) - 1
            elif self.current_index < 0 and self.data_product:
                self.current_index = 0

            self.write_json(self._current_file,self.data_product)
            print("Товар удалён")
        else:
            print("Нет товара для удаления")

    def reduce_count(self, number_reduction) -> None:
        """Уменьшить количество товара.

        Args:
             number_reduction: число, на которое нужно уменьшить количество товара.
        """

        try:
            number_reduction = int(number_reduction)

            if number_reduction <= 0 or number_reduction > self.get_count():
                print('Ошибка. Количество товара не может быть уменьшено на это число.')
            else:
                new_count = self.get_count() - number_reduction

                self.set_count(new_count)
        except ValueError:
            print('Введите корректное число.')
        except TypeError:
            print('Ошибка типа данных.')

        finally:
            print(f'Текущее количество товара: {self.get_count()}')

    def increase_count(self, number_increase) -> None:
        """Увеличить количество товара.

        Args:
             number_increase: число, на которое нужно увеличить количество товара.
        """

        try:
            number_increase = int(number_increase)

            if number_increase <= 0:
                print('Ошибка. Количество товара может быть увеличено только на положительное число.')
            elif number_increase > 10 ** 5:
                print('Ошибка. Слишком большое значение.')
            else:
                new_count = self.get_count() + number_increase

                self.set_count(new_count)
        except ValueError:
            print('Введите корректное число.')
        except TypeError:
            print('Ошибка типа данных.')

        finally:
            print(f'Текущее количество товара: {self.get_count()}')

    def type_of_delivery(self) -> None:
        """Тип доставки."""

        if self.get_region() == 100:
            print('Зарубежная доставка.')
        elif self.get_region() is None:
            print('Тип доставки не указан.')
        elif 0 < self.get_region() < 100:
            print('Доставка по России.')
        else:
            print(f'Неизвестный код региона: {self.get_region()}')

    def display_information(self) -> None:
        """Вывод информации о товаре."""

        print(f"\n--- Товар {self.current_index + 1} ---")
        print(f' Наименование товара: {self.get_name()}')
        print(f' Количество товара: {self.get_count()}')
        print(f' Производитель товара: {self.get_manufacturer()}')
        print(f' Стоимость товара: {self.get_cost()}')
        print(f' Регион доставки: {self.get_region()}')
        print(f' Категория товара: {self.get_category()}')
        print(f' Описание товара: {self.get_description()}')
        print(f' Характеристика товара: {self.get_characteristic()}')
        print(f' Вес товара (в кг): {self.get_weight()}')
        print(f' Артикул товара: {self.get_article_number()}')
        print(f' Цвет товара: {self.get_color()}')

    def show_all_products(self) -> None:
        """Показать все продукты."""

        if not self.data_product:
            print("Список товаров пуст")
            return

        print("\n" + "=" * 50)
        print("СПИСОК ТОВАРОВ:")
        print("-" * 50)

        for i, product in enumerate(self.data_product, 1):
            name = product.get('name', 'Без названия')
            article = product.get('article_number', 'Нет артикула')
            print(f"{i}. {name} (Артикул: {article})")

        print("=" * 50)
