from flask import Flask, request
import logging
import json
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# создаём словарь, в котором ключ — название города, а значение — массив,
# где перечислены id картинок, которые мы записали в прошлом пункте.
cities = {
    'кино',
    'музыка',
    'книги'
}

genres_cinema = {'военный':
 [['Семнадцать мгновений весны', 9.00, 'https://www.kinopoisk.ru/film/89540/'],
 ['Великая война', 9.00, 'https://www.kinopoisk.ru/film/503264/'],
 ['В бой идут одни "старики"', 9.00, 'https://www.kinopoisk.ru/film/25108/']],
 'боевик':
 [['Игра Престолов', 9.50, 'https://www.kinopoisk.ru/film/464963/'],
 ['Место встречи изменить нельзя', 8.90, 'https://www.kinopoisk.ru/film/77202/'],
 ['Последний мужик', 9.00, 'https://www.kinopoisk.ru/film/1008970/']],
 'мелодрама':
 [['Друзья', 8.90, 'https://www.kinopoisk.ru/film/77044/'],
 ['Игра Престолов', 9.50, 'https://www.kinopoisk.ru/film/464963/'],
 ['Форрест Гамп', 8.80, 'https://www.kinopoisk.ru/film/448/']],
 'комедия':
 [['Возмутительный класс', 9.40, 'https://www.kinopoisk.ru/film/71028/'],
 ['Рик и Морти', 9.30, 'https://www.kinopoisk.ru/film/685246/'],
 ['Марафонцы бегут круг почёта', 9.00, 'https://www.kinopoisk.ru/film/84473/']],
 'триллер':
 [['Во все тяжкие', 9.50, 'https://www.kinopoisk.ru/film/404900/'],
 ['Крёстный отец', 9.50, 'https://www.kinopoisk.ru/film/260992/'],
 ['Шерлок', 9.20, 'https://www.kinopoisk.ru/film/502838/']],
 'фильм ужасов':
 [['Сумеречная зона', 9.00, 'https://www.kinopoisk.ru/film/229159/'],
 ['Очень странные дела', 8.90, 'https://www.kinopoisk.ru/film/915196/'],
 ['Молчание ягнят', 8.60, 'https://www.kinopoisk.ru/film/345/']],
 'мультфильм':
 [['Рик и Морти', 9.30, 'https://www.kinopoisk.ru/film/685246/'],
 ['Аватар: Легенда об Аанге', 9.20, 'https://www.kinopoisk.ru/film/401152/'],
 ['Тетрадь смерти', 9.00, 'https://www.kinopoisk.ru/film/406148/']],
 'драма':
 [['Игра Престолов', 9.50, 'https://www.kinopoisk.ru/film/464963/'],
 ['Крёстный отец', 9.50, 'https://www.kinopoisk.ru/film/260992/'],
 ['Во все тяжкие', 9.50, 'https://www.kinopoisk.ru/film/404900/']]}

genres_music = {}
# создаём словарь, где для каждого пользователя мы будем хранить его имя
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        # созда\м словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'first_name': None,
            'item': None,
            'vibor': None
        }
        return

    # если пользователь не новый, то попадаем сюда.
    # если поле имени пустое, то это говорит о том,
    # что пользователь ещё не представился.
    if sessionStorage[user_id]['first_name'] is None:
        # в последнем его сообщение ищем имя.
        first_name = get_first_name(req)
        # если не нашли, то сообщаем пользователю что не расслышали.
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        # если нашли, то приветствуем пользователя.
        # И спрашиваем какой город он хочет увидеть.
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response'][
                'text'] = 'Приятно познакомиться, ' + first_name.title() + '. Что я могу тебе посоветовать?'
            # получаем варианты buttons из ключей нашего словаря cities
            res['response']['buttons'] = [
                {
                    'title': city.title(),
                    'hide': True
                } for city in cities
            ]
            sessionStorage[user_id]['vibor'] = req['request']['original_utterance']
    # если мы знакомы с пользователем и он нам что-то написал,
    # то это говорит о том, что он уже говорит о городе, что хочет увидеть.
    else:
        if sessionStorage[user_id]['vibor'].lower() not in cities:
            item = sessionStorage[user_id]['vibor']
            if item.lower() == 'кино':
                sessionStorage[user_id]['vibor'] = 'кино'
            elif item.lower() == 'книга':
                sessionStorage[user_id]['vibor'] = 'книга'
            elif item.lower()== 'музыка':
                sessionStorage[user_id]['vibor'] = 'музыка'
        else:
            if sessionStorage[user_id]['vibor'] == 'кино':
                res['response']['text'] = 'Какой жанр кино ты хочешь посмотреть?'
                genre = req['request']['original_utterance']
                if genre != '':
                    a = get_cinema(genre)
                    res['response']['text'] = 'Мой совет: ' + a[0] + '. Его IMBd рейтинг: ' + a[1] + '. Ссылка на кинопоиск: ' + a[2] + '. Приятного просмотра!'
                else:
                    res['response']['text'] = 'Я какая-то шутка для тебя?'
            elif sessionStorage[user_id]['vibor'] == 'книга':
                res['response']['text'] = 'Какой жанр книг ты хочешь почитать?'
            elif sessionStorage[user_id]['vibor'] == 'музыка':
                res['response']['text'] = 'Какую музыку ты хочешь послушать?'
            else:
                res['response']['text'] = \
                'Прости, но я не могу дать тебе совет по этой теме!'


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)

def get_cinema(genre):
    if genre.lower() in genres_cinema.items():
        return random.choice(genres_cinema[genre.lower()])
    else:
        return '1Я не знаю такого жанра!'


if __name__ == '__main__':
    app.run()
