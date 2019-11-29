# -*- conidng:utf-8 -*-
'''Вопрос 1
Написать модуль на python, который получает с сайта list-org описание компании.
Входные данные: ссылка на компанию (например https://www.list-org.com/company/4868135)
Выходные данные: таблица , в каждой строке которой должны находиться:

Полное юридическое наименование,
Руководитель, Дата регистрации,
Статус,
ИНН,
КПП,
ОГРН,'''


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from pandas import ExcelWriter
import urllib

#  функция перемещение на 0-ю позицию
# def sort_up(df, pos):
#     df_m = df
#     try:
#         for i in range(pos, 0, -1):
#             df_m.loc[i], df_m.loc[i-1] = df_m.loc[i-1], df_m.loc[i]
#         df = df_m
#     except ValueError('Ошибка при перестановке'):
#         return df
#     finally:
#         return df


# получение текста страницы
def get_html(url):
    s = 'error'
    try:
        f = urllib.request.urlopen(url)
        s = f.read()
    except urllib.error.HTTPError:
        s = 'connect error'
    except urllib.error.URLError:
        s = 'url error'
    return s


def read_data(url):
    # чтение таблицы со страницы urls
    data = pd.read_html(urls, attrs={'class': 'tt'})
    target_table = data[0]

    # чтение Наззвания и ОГРН компании со страницы urls
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, features="lxml")
        data_ogrn = soup.find('span', title="Основной государственный регистрационный номер").parent.parent.text
        company_name = soup.find('a', {"class": "upper"}).text
        val_ogrn = data_ogrn.split()

    # добавление строк с ИНН и КПП
    target_table.loc[len(target_table)] = ['Полное юридическое наименование:', company_name]
    inn_kpp = target_table.iloc[1][1]
    target_table.loc[len(target_table)] = ['ИНН:', inn_kpp.split(' / ')[0]]
    target_table.loc[len(target_table)] = ['КПП:', inn_kpp.split(' / ')[1]]

    # добавление строки с ОГРН в таблицу DataFrame
    target_table.loc[len(target_table)] = val_ogrn


    #удаление ненужных данных
    target_table.drop([1, 2, 3, 4], inplace=True)

    target_table.index = np.arange(len(target_table))
    print(target_table)

    writer = ExcelWriter(f'company {target_table.iloc[3][1]}.xlsx')
    target_table.to_excel(writer, 'Sheet1')
    writer.save()

if __name__ == '__main__':
    urls = 'https://www.list-org.com/company/4868135'
    # urls = 'file:///home/leonid/PL_projects/LP/HH_Infotec/%D0%9E%D0%9E%D0%9E%20_%D0%9A%D0%9E%D0%9D%D0%A2%D0%98%D0%9D%D0%95%D0%9D%D0%A2%D0%90%D0%9B%20%D0%9F%D0%9B%D0%AE%D0%A1_%20(%D0%9E%D0%9A%D0%9F%D0%9E_18520970).html'
    read_data(urls)



