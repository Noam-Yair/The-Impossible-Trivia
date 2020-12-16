import random

NUMBER_OF_ACTORS_IN_DB = 131788
NUMBER_OF_MOVIES_IN_DB = 10000
NUMBER_OF_GENRES_IN_DB = 18

def run_sql_file(db, sql_path, **fmt):
    cur = db.cursor()
    with open(sql_path, "r") as f:
        cur.execute(f.read().format(**fmt))
        result = cur.fetchone()
    cur.close()
    return result

def get_random_actor_token():
    return random.randint(0, NUMBER_OF_ACTORS_IN_DB)

def get_random_movie_token():
    return random.randint(0, NUMBER_OF_MOVIES_IN_DB)

def get_random_genre_token():
    return random.randint(0, NUMBER_OF_GENRES_IN_DB)
