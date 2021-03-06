import utils

def movie_from_genre_x_where_y_played_for_the_first_time(db):
    d = utils.run_sql_file(db,
                           "sqls/movie_from_genre_x_where_y_played_for_the_first_time.sql",
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


def genre_which_actor_x_is_most_identified_with(db):
    d = utils.run_sql_file(db,
                           "sqls/genre_which_actor_x_is_most_identified_with.sql",
                           actor_token=utils.get_random_actor_token())
    return {
        "question": d[0],
        "answer": d[1],
        "img": d[2],
        "option1": d[3],
        "option2": d[4],
        "option3": d[5],
    }

def avg_movie_runtime(db):
    d = utils.run_sql_file(db,
                           "sqls/avg_movie_runtime.sql",
                           actor_token1=utils.get_random_actor_token(),
                           actor_token2=utils.get_random_actor_token(),
                           actor_token3=utils.get_random_actor_token(),)

    return {
        "question": d[0],
        "answer": d[1],
        "img": None,
        "option1":  d[1]-1,
        "option2": d[1]+2,
        "option3": d[1]+1,
    }

def which_of_actors_x_y_played_in_movie_with_rating_more_than_z(db):
    options = [0, 1, 2, 3]
    actor_token1 = utils.get_random_actor_token()
    actor_token2 = utils.get_random_actor_token()
    if actor_token1 == actor_token2:
        actor_token2 = (actor_token2 + 1) % utils.NUMBER_OF_ACTORS_IN_DB
    rating_token = round(utils.random.random() * 5.5 + 4, 1)
    d = utils.run_sql_file(db,
                           "sqls/which_of_actors_x_y_played_in_movie_with_rating_more_than_z.sql",
                           actor_token1=actor_token1,
                           actor_token2=actor_token2,
						   rating_token=rating_token)
    return {
        "question": d[-1],
        "answer": d[options.pop(int(d[-2]))],
        "img": None,
        "option1": d[options.pop()],
        "option2": d[options.pop()],
        "option3": d[options.pop()],
    }

def num_of_actors_from_gender_x_who_played_in_lead_roles_in_movie_y(db):
    options = [0, 1, 2, 3]
    movies_token = utils.get_random_movie_token()
    gender_token = utils.get_random_gender_token()
    d = utils.run_sql_file(db,
                           "sqls/num_of_actors_from_gender_x_who_played_in_lead_roles_in_movie_y.sql",
                           movies_token=movies_token,
                           gender_token=gender_token)
    if d[0]:
        return {
            "question": d[0],
            "answer": options.pop(d[1]),
            "img": d[2],
            "option1": options.pop(),
            "option2": options.pop(),
            "option3": options.pop(),
        }
    else:
        return num_of_actors_from_gender_x_who_played_in_lead_roles_in_movie_y(db)

def in_which_movie_does_the_actor_of_the_character_played_first(db):
    d = utils.run_sql_file(db,
                           "sqls/in_which_movie_does_the_actor_of_the_character_played_first.sql",
                           movie_token=utils.get_random_movie_token(),
                           movie_token1=utils.get_random_movie_token(),
                           movie_token2=utils.get_random_movie_token(),
                           movie_token3=utils.get_random_movie_token())
    return {
            "question": d[0],
            "answer": d[2],
            "img": d[3],
            "option1": d[4],
            "option2": d[5],
            "option3": d[6],
        }
