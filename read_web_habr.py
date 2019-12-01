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


# получение даты из строки
def get_date(str_date: str):
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    list_date = str_date.split()

    months = {'января': 1,
              'февраля': 2,
              'марта': 3,
              'апреля': 4,
              'мая': 5,
              'июня': 6,
              'июля': 7,
              'августа': 8,
              'сентября': 9,
              'октября': 10,
              'ноября': 11,
              'декабря': 12
              }

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

    d_str = d.strftime("%m/%d/%Y")
    return d_str


# проверка того, что дата старше года
def date_check(date_txt, today):
    try:
        dt = datetime.datetime.strptime(date_txt, '%d/%m/%Y')
        print(dt)
        if (datetime.timedelta(days=365) > today - dt):
            return True
        else:
            return False
    except:
        return False


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


# получение данных
def get_all(url_habr, count):
    # создание DataFrame для хранения данных
    df_habr = pd.DataFrame(columns=[
        "Заголовок",
        "Краткое описание",
        "Дата публикации",
        "Автор",
        "Рейтинг",
    ])

    # получение сегодняшней даты
    today = datetime.today()

    page_counter = 1
    flag_read = True

    while flag_read:

        url = ''.join([url_habr, str(page_counter)])
        print(url)
        page = get_html(url)
        if page != False:
            flag_read = True
            page_counter += 1
        else:
            break

        soup = BeautifulSoup(page, features="lxml")

        posts = soup.findAll('article', {'class': "post post_preview"})

        # Cчитывание постов со страницы
        for post in posts:
            post_date = get_date(post.find('span', {'class': "post__time"}).text)

            if date_check(post_date, today):
                flag_read = False

            post_title = post.find('a', {'class': "post__title_link"}).text
            post_description = post.find('div', {'class': "post__text post__text-html js-mediator-article"}).text
            post_author = post.find('a', {'class': "post__user-info user-info"}).text
            try:
                post_rate_text = post.find('span', {'class': "post-stats__result-counter"}).text
                if post_rate_text[0] == '–': post_rate_text[0] = '-'
                post_rate = int(post_rate_text)

            except (TypeError, ValueError):
                post_rate = 0

            # создание вектора значений для записи в DataFrame
            line = [post_title, post_description, post_date, post_author, post_rate]
            df_habr.loc[len(df_habr)] = line

    # Сортировка по рейтингу
    df_habr.sort_values(by=['Рейтинг'], ascending=False, inplace=True)

    # Срез по количеству заданных первых значений
    df_habr_result = df_habr.iloc[:count]
    df_habr_result.index = np.arange(len(df_habr_result))

    # Запись в excel-файл. Реализована замена существующего без проверки.
    writer = ExcelWriter('habr_posts.xlsx')
    df_habr_result.to_excel(writer, 'Sheet1')
    writer.save()

    return df_habr_result


if __name__ == '__main__':
    urls = 'https://habr.com/ru/top/yearly/page'
    result = get_all(urls, 1000)

'''
requirements.txt:

beautifulsoup4==4.8.1
certifi==2019.9.11
chardet==3.0.4
et-xmlfile==1.0.1
html5lib==1.0.1
idna==2.8
jdcal==1.4.1
lxml==4.4.2
numpy==1.17.4
openpyxl==3.0.2
pandas==0.25.3
python-dateutil==2.8.1
pytz==2019.3
requests==2.22.0
six==1.13.0
soupsieve==1.9.5
urllib3==1.25.7
webencodings==0.5.1
'''