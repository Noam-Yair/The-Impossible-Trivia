import random

def run_sql_file(db, sql_path, **fmt):
    cur = db.cursor()
    with open(sql_path, "r") as f:
        cur.execute(f.read().format(**fmt))
        result = cur.fetchone()
    cur.close()
    return result

def get_random_actor_token():
    return random.randint(0, 1000)

def get_random_movie_token():
    return random.randint(0, 1000)
