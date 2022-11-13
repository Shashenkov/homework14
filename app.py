from flask import Flask, jsonify
from utils import *


app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False


@app.route('/movie/<title>')
def get_movie_by_title(title):
    """ Выводит данные про фильм. """
    return movie_by_title(title)


@app.route('/movie/<int:year1>/to/<int:year2>')
def get_movie_by_years(year1, year2):
    """ Выводит список словарей из поиска по диапазону лет выпуска. """
    return jsonify(movie_by_years(year1, year2))


@app.route('/rating/<category>')
def get_movie_by_category(category):
    """ Выводит список фильмов по категориям:
    для детей, для семейного просмотра, для взрослых.
    Обрабатывает несколько маршрутов в соответствии с определенной группой.
    Выведит список словарей, содержащий информацию о названии, рейтинге и описании."""
    return jsonify(movie_by_rating(category))


@app.route('/genre/<genre>')
def get_movies_by_genre(genre):
    """Возвращает 10 самых свежих фильмов по названию жанра.
    В результате содержится название и описание каждого фильма."""
    return jsonify(movies_by_genre(genre))


if __name__ == "__main__":
    app.run(debug=True)
