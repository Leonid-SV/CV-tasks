# -*- conidng:utf-8 -*-
'''
Вопрос 2
Написать модуль на python, который получает с сайта https://habr.com/ru/ самые популярные посты за год.
Входные данные: число count - количество получаемых постов
Выходные данные: таблица , в каждой строке которой должны находиться:
заголовок поста,
короткое описание поста,
дата публикации,
имя автора поста
'''



from bs4 import BeautifulSoup
import datetime
from datetime import datetime
from datetime import timedelta
from datetime import date
import numpy as np
import pandas as pd
from pandas import ExcelWriter
import urllib

df_habr = pd.DataFrame(columns=[
    "post_header",
    "post_desc",
    "post_date",
    "post_author"
])

df_habr.loc[0] = ['bla-bla', 'Yahoooo', '01-01-19', 'balbes']

print(df_habr)

months = {'января':     1,
          'февраля':    2,
          'марта':      3,
          'апреля':     4,
          'мая':        5,
          'июня':       6,
          'июля':       7,
          'августа':    8,
          'сентября':   9,
          'октября':    10,
          'ноября':     11,
          'декабря':    12
          }

# date_ = '26 ноября 2019 в 09:15'
date_ = 'вчера в 23:06'

def get_date(str_date: str):
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    list_date = str_date.split()

    d = ''
    if list_date[0].lower() == 'сегодня':
        d = today
    elif list_date[0].lower() == 'вчера':
        d = yesterday
    else:
        d_day = int(list_date[0])
        d_month = months[list_date[1]]
        d_year = int(list_date[2])
        d = date(d_year, d_month, d_day)

    print(f'{d.day}/{d.month}/{d.year}')
        # print(f'{d_day}/{d_month}/{d_year}')
        # print(f'{type(d_day)}/{type(d_month)}/{type(d_year)}')
    return d

get_date(date_)

# получение текста страницы
def get_html(url):
    s = 'error'
    try:
        f = urllib.request.urlopen(url)
        s = f.read()
    except urllib.error.HTTPError:
        # s = 'connect error'
        s = False
    except urllib.error.URLError:
        s = False
    return s


def get_all():

    page_counter = 1
    flag_read = True

    while flag_read and page_counter < 2:
        url = f'https://habr.com/ru/all/page{page_counter}/'
        page = get_html(url)
        if page != False:
            flag_read = True
            page_counter += 1

        soup = BeautifulSoup(page, features="lxml")

        posts = soup.findAll('article', {'class': "post post_preview"})

        for post in posts:
            post_date = post.find('span', {'class': "post__time"}).text
            pass

        print(post_date)

get_all()

#
# def read_data(url):
#     # чтение таблицы со страницы urls
#     data = pd.read_html(urls, attrs={'class': 'tt'})
#     target_table = data[0]
#
#     # чтение Наззвания и ОГРН компании со страницы urls
#     html = get_html(url)
#     if html:
#         soup = BeautifulSoup(html, features="lxml")
#         data_ogrn = soup.find('span', title="Основной государственный регистрационный номер").parent.parent.text
#         company_name = soup.find('a', {"class": "upper"}).text
#         val_ogrn = data_ogrn.split()
#
#     # добавление строк с ИНН и КПП
#     target_table.loc[len(target_table)] = ['Полное юридическое наименование:', company_name]
#     inn_kpp = target_table.iloc[1][1]
#     target_table.loc[len(target_table)] = ['ИНН:', inn_kpp.split(' / ')[0]]
#     target_table.loc[len(target_table)] = ['КПП:', inn_kpp.split(' / ')[1]]
#
#     # добавление строки с ОГРН в таблицу DataFrame
#     target_table.loc[len(target_table)] = val_ogrn
#
#
#     #удаление ненужных данных
#     target_table.drop([1, 2, 3, 4], inplace=True)
#
#     target_table.index = np.arange(len(target_table))
#     print(target_table)
#
#     writer = ExcelWriter(f'company {target_table.iloc[3][1]}.xlsx')
#     target_table.to_excel(writer, 'Sheet1')
#     writer.save()
#
# if __name__ == '__main__':
#     urls = 'https://www.list-org.com/company/4868135'
#     # urls = 'file:///home/leonid/PL_projects/LP/HH_Infotec/%D0%9E%D0%9E%D0%9E%20_%D0%9A%D0%9E%D0%9D%D0%A2%D0%98%D0%9D%D0%95%D0%9D%D0%A2%D0%90%D0%9B%20%D0%9F%D0%9B%D0%AE%D0%A1_%20(%D0%9E%D0%9A%D0%9F%D0%9E_18520970).html'
#     read_data(urls)

