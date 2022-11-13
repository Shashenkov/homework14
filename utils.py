import sqlite3
from collections import Counter


class DbConnect:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()


def movie_by_title(title):
    """ Поиск по названию. Если результатов несколько, то выведит самый свежий по году выпуска.
    """
    db_connect = DbConnect('netflix.db')
    db_connect.cur.execute(
        f"""SELECT title, country, release_year, listed_in, description
        from netflix 
        where title like '%{title}%'
        order by release_year desc
        limit 1""")
    result = db_connect.cur.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }


def movie_by_years(year1, year2):
    """ Поиск по диапазону лет выпуска. Принимает два года и возвращает данные."""
    db_connect = DbConnect('netflix.db')
    query = f"SELECT title, release_year from netflix where release_year between '{year1}' and '{year2}' limit 100"
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "release_year": movie[1]})
    return result_list


def movie_by_rating(rating):
    """ Возвращает список фильмов в соответствии с допустимым рейтингом:
    для детей, для семейного просмотра, для взрослых. """
    db_connect = DbConnect('netflix.db')
    rating_parameters = {
                        "children": "'G'",
                        "family": "'G', 'PG', 'PG-13'",
                        "adult": "'R', 'NC-17'"
    }
    if rating not in rating_parameters:
        return "Переданной группы не существует."
    query = f"""select title, rating, description
            from netflix 
            where rating in ({rating_parameters[rating]})"""
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "rating": movie[1],
                            "description": movie[2]})
    return result_list


def movies_by_genre(genre):
    """ Получает название жанра в качестве аргумента и возвращает 10 самых свежих фильмов.
    """
    db_connect = DbConnect('netflix.db')
    query = f"""select title, description 
            from netflix 
            where listed_in like '%{genre}%'
            order by release_year desc
            limit 10;"""
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "description": movie[1]
                            })
    return result_list


def cast_partners(actor1, actor2):
    """ Получает в качестве аргумента имена двух актеров,
    сохраняет всех актеров из колонки cast и возвращает список тех,
    кто играет с ними в паре больше 2 раз. """
    db_connect = DbConnect('netflix.db')
    query = f"""select `cast`
            from netflix 
            where `cast` like '%{actor1}%' 
            and `cast` like '%{actor2}%'"""
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    actor_list = []
    for cast in result:
        actor_list.extend(cast[0].split(", "))
    counter = Counter(actor_list)
    result_list = []
    for actor, count in counter.items():
        if actor not in [actor1, actor2] and count > 2:
            result_list.append(actor)
    return result_list


def movie_by_type_release_year_and_genre(movie_type, release_year, genre):
    """ Принимает тип картины (фильм или сериал), год выпуска и ее жанр
    и получать на выходе список названий картин с их описаниями."""
    db_connect = DbConnect('netflix.db')
    query = f"""select title, description
            from netflix 
            where type = '{movie_type}'
            and release_year = '{release_year}' 
            and listed_in like '%{genre}%'
            """
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                           "description": movie[1]})
    return result_list
