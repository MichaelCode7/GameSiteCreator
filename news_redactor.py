from data import db_session
import datetime
from data.news import News
from general_funcs import GeneralFuncs as gf
from general_vars import *
import sys


def add_news():
    db_sess = db_session.create_session()
    print('Синтаксис новости:\nЗаголовок\nКонтент')
    arr = list(map(lambda x: x.strip(), sys.stdin))
    if len(arr) > 2:
        print('Синтаксическая ошибка!')
        return
    news = News()
    news.title, news.content = arr
    db_sess.add(news)
    db_sess.commit()
    return f'Новость:\n{news.title}\n{news.content}\nУспешно занесена в базу!'

def edit_news():
    db_sess = db_session.create_session()
    news_id = int(input('Введите id изменяемой новости: '))
    news = db_sess.query(News).filter(News.id == news_id).first()
    if news:
        print('Синтаксис новости:\nЗаголовок\nКонтент')
        arr = list(map(lambda x: x.strip(), sys.stdin))
        if len(arr) > 2:
            print('Синтаксическая ошибка!')
            return
        news.title, news.content = arr
        news.last_update_date = datetime.datetime.now()
        db_sess.commit()
        return f'Новость с id {news_id}:\n{news.title}\n{news.content}\nУспешно изменена!'
    else:
        return 'Такой записи нет в базе!'

def news_delete():
    db_sess = db_session.create_session()
    news_id = int(input('Введите id удаляемой новости: '))
    news = db_sess.query(News).filter(News.id == news_id).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
        return f'Новость с id {news_id} успешно удалена!'
    else:
        return 'Такой записи нет в базе!'

def main():
    db_session.global_init("db/gshopdata.db")
    while True:
        answ = input('''Выберите один из предложенных вариантов:\n1 - добавить новость.
2 - изменить новость.\n3 - удалить новость.\n4 - выход.\n''')
        match answ:
            case '1':
                print(add_news())
            case '2':
                print(edit_news())
            case '3':
                print(news_delete())
            case '4':
                sys.exit()
            case _:
                print('Нет такого варианта.')


if __name__ == '__main__':
    main()