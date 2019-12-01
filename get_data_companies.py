# -*- conidng: utf-8 -*-
'''Вопрос 1
Написать модуль на python, который получает с сайта list-org описание компании.
Входные данные: ссылка на компанию (например https://www.list-org.com/company/4868135)
Выходные данные: таблица , в каждой строке которой должны находиться:
Полное юридическое наименование,
Руководитель,
Дата регистрации,
Статус,
ИНН,
КПП,
ОГРН,'''

import numpy as np
import pandas as pd
import os.path
import urllib
from bs4 import BeautifulSoup
from pandas import ExcelWriter


def swap_rows(df, i1, i2):
    # меняем строки местами
    a, b = df.iloc[i1, :].copy(), df.iloc[i2, :].copy()
    df.iloc[i1, :], df.iloc[i2, :] = b, a
    return df

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
    data = pd.read_html(url, attrs={'class': 'tt'})
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
    target_table.drop([1, 2, 3], inplace=True)
    swap_rows(target_table, 0, 2)
    swap_rows(target_table, 1, 2)
    target_table.index = np.arange(len(target_table))

    print(target_table)

    return target_table


if __name__ == '__main__':
    # urls = 'https://www.list-org.com/company/4868135'
    urls = 'https://www.list-org.com/company/1268806'

    df = read_data(urls)

    file_name = f'company {df.iloc[3][1]}.xlsx'

    if not os.path.isfile(file_name):
        write = ExcelWriter(file_name)
        df.to_excel(write)
        write.save()

'''
requirements.txt:
beautifulsoup4==4.8.1
bs4==0.0.1
et-xmlfile==1.0.1
jdcal==1.4.1
lxml==4.4.2
numpy==1.17.4
openpyxl==3.0.2
pandas==0.25.3
python-dateutil==2.8.1
pytz==2019.3
six==1.13.0
soupsieve==1.9.5
'''

