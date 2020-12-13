import utils

def genre_x_where_y_played_for_the_first_time(db):
    d = utils.run_sql_file(db,
                           "sqls/try.sql",
                           movie_token1=utils.get_random_movie_token(),
                           movie_token2=utils.get_random_movie_token(),
                           movie_token3=utils.get_random_movie_token(),
                           actor_token=utils.get_random_actor_token())
    return {
        "question": d[0],
        "answer": d[1],
        "img": d[2],
        "option1": d[3],
        "option2": d[4],
        "option3": d[5],
    }

