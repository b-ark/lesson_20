# Functionality of Phonebook application:
#
# Add new entries
# Search by first name
# Search by last name
# Search by full name
# Search by telephone number
# Search by city or state
# Delete a record for a given telephone number
# Update a record for a given telephone number
# An option to exit the program
#
# The first argument to the application should be the name of the phonebook. Application should load JSON data,
# if it is present in the folder with application, else raise an error. After the user exits,
# all data should be saved to loaded JSON.
import json
from typing import Union


def choose_operation() -> str:
    """Функция по выбору необходимой операции"""
    while True:
        try:
            answer = input('''1 - посмотреть доступные контакты в телефонной книге
2 - добавить новый контакт
3 - поиск контакта
4 - удалить контакт
5 - изменить контакт
6 - выход
Выберите необходимую операцию: ''')
            if not answer.isdigit() or (int(answer) > 6 or int(answer) < 1):
                raise ValueError
        except ValueError:
            print('Данная операция недоступна! Попробуйте ещё раз!')
        else:
            return answer


def add_new_contact() -> None:
    """Добавляем новый контакт"""
    print('Создание нового контакта')
    number = get_phone_number(False)
    if not search_number(number):
        print('Создаем новый контакт!')
        phonebook.update({number: {
            "first_name": get_str_from_user('first_name').title(),
            "last_name": get_str_from_user('last_name').title(),
            "city": get_str_from_user('city').title()}})
    else:
        print('Данный номер уже записан в телефонной книге! Чтобы изменить его, воспользуйтесь функцией \"5\"')


def get_phone_number(blank_string: bool) -> Union[None, str]:
    """Получаем номер от пользователя. Переменная blank_string необходима для
    возможности получения пустой строки для функции search()"""
    while True:
        number = input('Номер телефона: ')
        if len(number) == 10 and number.isdigit():
            return number
        elif blank_string and number == '':
            return number
        else:
            print('Номер телефона должен состоять из 10 цифр')


def get_str_from_user(description: str, blank_string=False) -> Union[None, str]:
    """Функция для ввода города, имени и фамилии"""
    while True:
        available_line = input(f'{description}: ')
        if len(available_line) < 3 and (available_line != '' or not blank_string):
            print('Введите как минимум 3 символа')
        elif blank_string:
            return available_line
        else:
            return available_line


def search_number(number: str) -> bool:
    """Функция для поиска номера в словаре"""
    if number in phonebook:
        print(f'Номер: {number}, {json.dumps(phonebook[number], indent=2)}')
        return True
    print('По Вашему запросу не найдено совпадений!')
    return False


def search_info(temp_str: str, temp_key: str) -> None:
    """Функция для поиска по имени и фамилии отдельно, а так же для города"""
    counter = 0
    for key, i in phonebook.items():
        if i[temp_key].lower() == temp_str.lower():
            counter += 1
            print(f'Номер - {key}, {json.dumps(i, indent=2)}')
    if counter == 0:
        print('По вашему запросу не найдено совпадений!')


def search_info_extended(temp_str1: str, temp_str2: str, temp_key1: str, temp_key2: str) -> None:
    """Функция для поиска по имени и фамилии одновременно"""
    counter = 0
    for key, i in phonebook.items():
        if i[temp_key1].lower() == temp_str1.lower() and i[temp_key2].lower() == temp_str2.lower():
            counter += 1
            print(f'Номер: {key}, {json.dumps(i, indent=2)}')
    if counter == 0:
        print('По вашему запросу не найдено совпадений!')


def search() -> None:
    """Функция для поиска по словам, необходимым для пользователя. Реализовал в таком виде,
    чтобы у пользователя было больше вариантов найти нужную информацию, а не выбирать метод"""
    print('Если вы не хотите искать по предложенному параметру, нажмите \'Enter\'')

    number = get_phone_number(True)
    if number != '':
        search_number(number)
        return None

    name = get_str_from_user('first_name', True)
    surname = get_str_from_user('last_name', True)
    if name != '':
        if surname != '':
            search_info_extended(name, surname, 'first_name', 'last_name')
        else:
            search_info(name, 'first_name')
        return None
    elif surname != '':
        search_info(surname, 'last_name')
        return None

    city = get_str_from_user('city', True)
    if city != '':
        search_info(city, 'city')
        return None


def delete_contact() -> None:
    """Удаление контакта по номеру телефона"""
    print('Для отмены опереации нажмите \"Enter\"')
    number = get_phone_number(True)
    if number == '':
        print('Отмена операции')
    else:
        if search_number(number):
            phonebook.pop(number)
            print('Контакт успешно удалён!')


def get_update_contact() -> None:
    """Изменение существующего контакта (основа работы)"""
    number = get_phone_number(False)
    if search_number(number):
        print('Если вы не хотите изменять определённую информацию, нажмите \"Enter\"')
        update_contact(number, "first_name")
        update_contact(number, "last_name")
        update_contact(number, "city")
    else:
        print('По Вашему запросу не было найдено сохранённых контактов. '
              'Воспользуйтесь функцией \"1\" чтобы создать новый контакт')


def update_contact(number: str, temp_key: str) -> None:
    """Изменение существующего контакта (вспомогательная)"""
    temp_str = get_str_from_user(temp_key, True).title()
    if temp_str != '':
        phonebook[number][temp_key] = temp_str


def main_phonebook() -> None:
    """Основная функция работы телефонной книжки"""
    operation = 'temp'
    while operation != '6':
        operation = choose_operation()
        if operation == '1':
            print(json.dumps(phonebook, indent=2))
        elif operation == '2':
            add_new_contact()
        elif operation == '3':
            search()
        elif operation == '4':
            delete_contact()
        elif operation == '5':
            get_update_contact()

    with open('phonebook.json', 'w', encoding='utf-8') as file_object_new:
        json.dump(phonebook, file_object_new, ensure_ascii=False, indent=2)


DEF_PB = 'phonebook.json'
try:
    with open(DEF_PB, 'r') as file_object:
        phonebook = json.load(file_object)
        print(f'Используется телефонный справочник {DEF_PB}')
        main_phonebook()
except FileNotFoundError:
    print(f'Файла {DEF_PB} нет в дериктории')
