import random
from flask import Flask, render_template, request
import config
import utils
import mysql.connector
from trivia_questions import movie_from_genre_x_where_y_played_for_the_first_time
from trivia_questions import genre_which_actor_x_is_most_identified_with

app = Flask(__name__)

QUESTIONS = [movie_from_genre_x_where_y_played_for_the_first_time, genre_which_actor_x_is_most_identified_with]
TRIVIA_QUESTIONS_COUNT = 20
RIGHT_ANSWER_POINTS = 10
WRONG_ANSWER_POINTS = -3

def connect_to_db():
    return mysql.connector.connect(host=config.DB_SERVER, user=config.DB_USERNAME, password=config.DB_PASSWORD, database=config.DB_SCHEMA)

def randomly_select_question():
    db = connect_to_db()
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
    return render_template('help.html')

@app.route('/', methods=['GET', 'POST'])
def index():
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
    question, answer, img, options = randomly_select_question()
    print("Right answer is:", answer)
    return render_template('index.html', question=question, img=img, options=options, score=score, questions_count=questions_count, message=message, message_color=message_color, trivia_questions_count=TRIVIA_QUESTIONS_COUNT)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="40004", debug=True)
