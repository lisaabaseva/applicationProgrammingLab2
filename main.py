import json
import argparse
import re
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('input', help="Откуда считываются данные(название файла)")
parser.add_argument('output', help="Куда сохраняются валидные данные(название файла)")
args = parser.parse_args()

"""
Поля для проверки:
---Тел.номер(telephone)                          ___ check_telephone
---рост(height)                                  ___ check_height
---ИНН(inn)                                      ___ check_inn
---Серия паспорта(passport_series)               ___ check_passport_series
---Университет(university)                       ___ check_university
---Возраст(age)                                  ___ check_age
---Политические взгляды(political_views)         ___ check_political_views
---Мировоззрение(worldview)                      ___ check_worldview
---Адрес(address)                                ___ check_address
"""


# класс Validator ничего не хранит т.к. он только для проверки
class Validator:
    def __init__(self):
        pass

# /^[\d]{1}\ \([\d]{2,3}\)\ [\d]{2,3}-[\d]{2,3}-[\d]{2,3}$/

    def check_telephone(telephone: str) -> bool:
        if re.match(r"^((\+?7|8)[ \-] ?)?((\(\d{3}\))|(\d{3}))?([ \-])?(\d{3}[\- ]?\d{2}[\- ]?\d{2})$", telephone):
            return True
        return False

    def check_height(height: str) -> bool:
        if re.match(r"(?<=\s)[-]?\d+[.]\d*(?:[eE][+-]\d+)?(?=\s)", height):
            if 0.2 < int(height) < 2.3:
                return True
        return False

    def check_inn(inn: str) -> bool:
        if re.match(r"[\d]{12}", inn):
            return True
        return False

    def check_passport_series(passport_series: str) -> bool:
        if re.match(r"\d\d[ ]\d\d", str(passport_series)):
            return True
        return False

    def check_university(university: str) -> bool:
        if re.match(r"^\d+", str(university)):
            if 0 < int(university) < 300:
                return True
        return False

    def check_age(age: int) -> bool:
        if re.match(r"^\d+", str(age)) is not None:
            if 0 < int(age) < 123:
                return True
        return False

    def check_political_views(political_views: str) -> bool:
        if re.match(r"^\D+$", political_views):
            return True
        return False

    def check_worldview(worldview: str) -> bool:
        if re.match(r"^\D+$", worldview):
            return True
        return False

    def check_address(address: str) -> bool:
        if re.match(r"[а-яА-Я.\s\d-]+\s+[0-9]+$", address):
            return True
        return False


data = json.load(open(args.input, encoding='windows-1251'))
validate_data = list()

telephone = 0
height = 0
inn = 0
passport_series = 0
university = 0
age = 0
political_views = 0
worldview = 0
address = 0

with tqdm(total=len(data)) as progressbar:
    for person in data:
        field = True
        if not Validator.check_telephone(person['telephone']):
            telephone += 1
            field = False
        if not Validator.check_height(person['height']):
            height += 1
            field = False
        if not Validator.check_inn(person['inn']):
            inn += 1
            field = False
        if not Validator.check_passport_series(person['passport_series']):
            passport_series += 1
            field = False
        if not Validator.check_university(person['university']):
            university += 1
            field = False
        if not Validator.check_age(person['age']):
            age += 1
            field = False
        if not Validator.check_political_views(person['political_views']):
            political_views += 1
            field = False
        if not Validator.check_worldview(person['worldview']):
            worldview += 1
            field = False
        if not Validator.check_address(person['address']):
            address += 1
            field = False
        if field:
            validate_data.append(person)
        progressbar.update(1)

output_file = open(args.output, 'w')
data_file = json.dumps(validate_data)
output_file.write(data_file)
output_file.close()

print("Количество валидных записей: ", len(validate_data))
print("Количество невалидных записей: ", len(data)-len(validate_data))
print(f'Количество невалидных телефонных номеров: {telephone}')
print(f'Количество невалидного роста: {height}')
print(f'Количество невалидного ИНН: {inn}')
print(f'Количество невалидных серий паспортов: {passport_series}')
print(f'Количество невалидных названий университета: {university}')
print(f'Количество невалидного возраста: {age}')
print(f'Количество невалидныъ политических взглядов: {political_views}')
print(f'Количество невалидного вероисповедания: {worldview}')
print(f'Количество невалидного адреса: {address}')




