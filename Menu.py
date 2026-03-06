from Product import Product

class Menu(Product):

    def __init__(self,file):
        """Инициализатор класса.

            Args:
                file: файл с данными о товарах

        """

        super().__init__(file)

    def change_information(self, parameter) -> None:
        """"Изменить информацию о товаре.

        Args:
            parameter:выбор того, что нужно изменить.
        """

        try:
            if parameter == 1:
                name = input("Введите новое имя товара")

                self.set_name(name)

                print(f"Имя товара изменено на {self.get_name()}")
            elif parameter == 2:
                count = int(input("Введите новое количество товара"))

                self.set_count(count)

                print(f"Количество товара изменено на {self.get_count()}")
            elif parameter == 3:
                manufacturer = input("Введите нового производителя товара")

                self.set_manufacturer(manufacturer)

                print(f"Имя производителя товара изменено на {self.get_manufacturer()}")
            elif parameter == 4:
                cost = int(input("Введите новую стоимость товара"))

                self.set_cost(cost)

                print(f"Стоимость товара изменена на {self.get_cost()}")
            elif parameter == 5:
                region = int(input("Введите новое регион, из которого доставляется товар."))

                self.set_region(region)

                print(f"Регион, из которого доставляется товар изменен на {self.get_region()}")
            elif parameter == 6:
                category = input("Введите новую категорию товара")

                self.set_category(category)

                print(f"Категория товара изменена на {self.get_category()}")
            elif parameter == 7:
                description = input("Введите новое описание товара")

                self.set_description(description)

                print(f"Описание товара изменено на {self.get_description()}")
            elif parameter == 8:
                characteristic = input("Введите новую характеристику товара")

                self.set_characteristic(characteristic)

                print(f"Характеристика товара изменена на {self.get_characteristic()}")
            elif parameter == 9:
                weight = input("Введите новый вес товара (в кг)")

                self.set_weight(weight)

                print(f"Вес товара изменен на {self.get_weight()}")
            elif parameter == 10:
                article_number = int(input("Введите новый артикул товара."))

                self.set_article_number(article_number)

                print(f"Артикул товара изменен на {self.get_article_number()}")
            elif parameter == 11:
                color = input("Введите новый цвет товара.")

                self.set_color(color)

                print(f"Цвет товара изменен на {self.get_color()}")
            else:
                print('Введено неверное число.')

        except ValueError:
            print('Ошибка!Вводить можно только числа.')
        except TypeError:
            print('Ошибка типа данных.')

    def choose_another_product(self, number_product) -> None:
        """"Выбрать другой товар.

        Args:
            number_product:номер продукта.
        """

        try:
            number = int(number_product)

            if 0 < number <= len(self.data_product):
                self.current_index = number - 1
                print(f"Выбран товар {number}: {self.get_name()}")
            else:
                print(f'Введите число от 1 до {len(self.data_product)}')
        except ValueError:
            print('Введите корректное число.')
        except TypeError:
            print('Ошибка типа данных.')
        except KeyError:
            print('Такого товара не существует.')

    def menu(self) -> None:
        """Меню программы."""

        job = True

        while job:

            print("=" * 30)
            print("""
                        MENU
            0. Добавить файл.
            1. Показать информацию по товару.
            2. Увеличить количество товара.
            3. Уменьшить количество товара.
            4. Проверить наличие товара.
            5. Удалить информацию о товаре.
            6. Тип доставки.
            7. Выход из программы.
            8. Изменить информацию о товаре.
            9. Выбрать другой товар.
            10. Добавить данные о товаре.
            """)

            try:
                choice = int(input("Выберите задачу..."))

                match choice:
                    case 1:
                        self.display_information()

                        input("\nНажмите Enter для продолжения...")
                    case 2:
                        number_increase = input("Введите число, на которое нужно увеличить товар.")

                        self.increase_count(number_increase)

                        input("\nНажмите Enter для продолжения...")
                    case 3:
                        number_reduction = input("Введите число, на которое нужно уменьшить товар.")

                        self.reduce_count(number_reduction)

                        input("\nНажмите Enter для продолжения...")
                    case 4:
                        self.condition_product()

                        input("\nНажмите Enter для продолжения...")
                    case 5:
                        self.delete_product()

                        input("\nНажмите Enter для продолжения...")
                    case 6:
                        self.type_of_delivery()

                        input("\nНажмите Enter для продолжения...")
                    case 7:
                        job = False
                    case 8:
                        parameter = int(input("""Выберите параметр, который вы хотите изменить:
                            1. Имя товара
                            2. Количество товара
                            3. Производитель товара
                            4. Стоимость товара
                            5. Регион, из которого доставляется товар
                            6. Категория товара
                            7. Описание товара
                            8. Характеристика товара
                            9. Вес товара(в кг)
                            10.Артикул товара
                            11.Цвет товара

                            """))

                        self.change_information(parameter)
                    case 9:
                        self.show_all_products()

                        if self.data_product:
                            number_product = input('Введите номер товара')

                            self.choose_another_product(number_product)
                    case 0:
                        file = input('Введите имя файла:')

                        self.upload_data(file)
                    case 10:
                        print("\nВыберите способ ввода:")
                        print("1 - Ввести строку с данными (поля через точку с запятой)")
                        print("0 - Последовательно вводить каждое поле")

                        choice = int(input("Ваш выбор: "))

                        if choice == 1:
                            print("\nФормат строки: название;количество;производитель;стоимость;регион;категория;описание;характеристика;вес;артикул;цвет")

                            line = input('Введите строку:')

                            self.add_line_info(line)
                        elif choice == 0:
                            self.add_information()
                        else:
                            print('Выбрано некорректное значение')



            except ValueError:
                print('Ошибка!Вводить можно только числа.')
            except TypeError:
                print('Ошибка типа данных.')


if __name__ == "__main__":
    product = Menu("file")
    product.menu()
