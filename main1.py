import re


# читаем адресную книгу в формате CSV в список contacts_list
import csv

from main import logger1

with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


# TODO 1: выполните пункты 1-3 ДЗ
# ваш код
""" Паттерн для поиска телефона """
pattern_t1 = r"""
    \+?(?P<country>\d{1})   # Код страны (Группа country)
    \s?\(?                  # Возможные разделители(пробел, ( )
    (?P<city>\d{3})         # Код города (3 цифры)
    [)-]?\s?                # Возможные разделители( ), -, пробел)
    (?P<t1>\d{3})           # Первые три цифры номера телефона
    \-?                     # Возможный разделитель (-)
    (?P<t2>\d{2})           # Вторые две цифры номера телефона
    \-?                     # Возможный разделитель (-)
    (?P<t3>\d{2})           # Последние две цифры номера телефона
    \s?\(?(доб.)?\s?        # Возможный разделитель перед добавочным номером
    (?P<ad>\d{4})?\)?       # Возможный добавочный номер (доб. 9999)
"""


""" Паттерн для перевода номера телефона в формат +7(999)999-99-99"""
replace_t1 = r"+7(\g<city>)\g<t1>-\g<t2>-\g<t3>"

""" Паттерн для перевода номера телефона в формат +7(999)999-99-99 доб.9999"""
replace_t2 = r"+7(\g<city>)\g<t1>-\g<t2>-\g<t3> доб.\g<ad>"


"""Сравнивает два списка. Если первые два элемента у них равны, то возвращает список, 
   содержащий недостающие значения, взятые из первого или второго списка.
    Если  совпадения отсутствуют или длины списков разные функция возвращает False"""
@logger1('main1.log')
def comp_rec(rec1, rec2):
    rec = []
    if len(rec1) != len(rec2):
        return False
    if (rec1[0] == rec2[0]) and (rec1[1] == rec2[1]):
        for i in range(len(rec1)):
            if rec1[i] == rec2[i]:
                rec.append(rec1[i])
            elif rec1[i] == '':
                rec.append(rec2[i])
            elif rec2[i] == '':
                rec.append(rec1[i])
        return rec
    else:
        return False


"""Удаляет из списка дублирующие элементы (списки, у которых совпадают первые и вторые элементы)"""
@logger1('main1.log')
def comp_rec_2(rec):
    result = []
    i = 0
    """ Проверяем список списков на наличие дубликатов по равенству первых двух элементов списков"""
    while i < len(rec):
        for j in range(i+1, len(rec)):
            if not comp_rec(rec[i], rec[j]):
                continue
            else:
                rec[i] = comp_rec(rec[i], rec[j])
                rec[j][0] = ''
        result.append(rec[i])
        i += 1
    i = 0
    """ Удаляем из конечного списка списки, в которых значение первого элемента равно '' """
    result1 = [item for item in result if item[0] != '']

    return result1


result_list = []
for row in contacts_list:
    fio = " ".join(row[:3]).split()
    if len(fio) == 3:
        row[0], row[1], row[2] = fio[0], fio[1], fio[2]
    elif len(fio) == 2:
        row[0], row[1] = fio[0], fio[1]

    match = re.search(pattern_t1, row[5], flags=re.VERBOSE)
    if match and match.group('ad'):
        row[5] = re.sub(pattern_t1, replace_t2, row[5], flags=re.VERBOSE)
    elif match:
        row[5] = re.sub(pattern_t1, replace_t1, row[5], flags=re.VERBOSE)

    result_list.append(row)

new_result_list = comp_rec_2(result_list)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(new_result_list)