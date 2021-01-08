import random
import sys
from flask import Flask, render_template, request
import config
import utils
import mysql.connector
from trivia_questions import movie_from_genre_x_where_y_played_for_the_first_time
from trivia_questions import genre_which_actor_x_is_most_identified_with
from trivia_questions import avg_movie_runtime
from trivia_questions import num_of_actors_from_gender_x_who_played_in_lead_roles_in_movie_y
from trivia_questions import which_of_actors_x_y_played_in_movie_with_rating_more_than_z
from trivia_questions import in_which_movie_does_the_actor_of_the_character_played_first


app = Flask(__name__)

QUESTIONS = [
    in_which_movie_does_the_actor_of_the_character_played_first,
    movie_from_genre_x_where_y_played_for_the_first_time,
    genre_which_actor_x_is_most_identified_with,
    num_of_actors_from_gender_x_who_played_in_lead_roles_in_movie_y,
    avg_movie_runtime,
    which_of_actors_x_y_played_in_movie_with_rating_more_than_z
]
TRIVIA_QUESTIONS_COUNT = 20
RIGHT_ANSWER_POINTS = 10
WRONG_ANSWER_POINTS = -3

def connect_to_db():
    if (len(sys.argv) > 1):
	    return mysql.connector.connect(port=int(sys.argv[1]), user=config.DB_USERNAME, password=config.DB_PASSWORD, database=config.DB_SCHEMA)
    return mysql.connector.connect(host=config.DB_SERVER, user=config.DB_USERNAME, password=config.DB_PASSWORD, database=config.DB_SCHEMA)

def randomly_select_question(db):
    question_data = random.choice(QUESTIONS)(db)
    db.close()
    options = [
        {"option_indicator": "right", "value": question_data["answer"]},
        {"option_indicator": "wrong", "value": question_data["option1"]},
        {"option_indicator": "wrong", "value": question_data["option2"]},
        {"option_indicator": "wrong", "value": question_data["option3"]},
    ]
    random.shuffle(options)
    return question_data["question"], question_data["answer"], question_data["img"], options

@app.route('/help', methods=['GET', 'POST'])
def help():
    movies, actors = [], []
    db = connect_to_db()
    if request.method == "POST":
        res = utils.run_sql_file_fetchall(db, "sqls/full_text_search.sql", query=request.form.get("query"))
        for row in res:
            if row[0] == "movie":
                movies.append(row[1])
            else:
                actors.append(row[1])
    db.close()
    
    return render_template('help.html', movies=movies, actors=actors, query=request.form.get("query"))

@app.route('/', methods=['GET', 'POST'])
def index():
    db = connect_to_db()
    message = ""
    score = int(request.form.get("score", 0))
    questions_count = int(request.form.get("questions_count", 0)) + 1
    if questions_count >= TRIVIA_QUESTIONS_COUNT:
        return render_template("done.html", score=score)
    message_color = "black"
    if request.method == "POST":
        if "right" in request.form:
            message = "Right Answer :)"
            message_color = "Green"
            score += RIGHT_ANSWER_POINTS
        else:
            message = "Wrong Answer :("
            message_color = "Red"
            score += WRONG_ANSWER_POINTS
    question, answer, img, options = randomly_select_question(db)
    db.close()
    return render_template('index.html', question=question, img=img, options=options, score=score, questions_count=questions_count, message=message, message_color=message_color, trivia_questions_count=TRIVIA_QUESTIONS_COUNT)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="40004", debug=True)
