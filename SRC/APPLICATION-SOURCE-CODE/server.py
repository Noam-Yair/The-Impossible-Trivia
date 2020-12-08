from flask import Flask, render_template, request
import config
import utils
import mysql.connector

db = mysql.connector.connect(host=config.DB_SERVER, user=config.DB_USERNAME, password=config.DB_PASSWORD, database=config.DB_SCHEMA)
app = Flask(__name__)

@app.route('/search')
def search_return_html():
    query = request.args.get('query')
    # with connector get to your mysql server and query the DB
    # return the answer to number_of_songs var.
    number_of_songs = 5 #should be retrieved from the DB
    return render_template('searchResults.html', count=5, query=query)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    message_color = "black"
    if request.method == "POST":
        if "answer1" in request.form:
            message = "Right Answer :)"
            message_color = "Green"
        else:
            message = "Wrong Answer :("
            message_color = "Red"
    d = utils.run_sql_file(db,
                           "sqls/try.sql",
                           movie_token1=utils.get_random_movie_token(),
                           movie_token2=utils.get_random_movie_token(),
                           movie_token3=utils.get_random_movie_token(),
                           actor_token=utils.get_random_actor_token())
    return render_template('index.html', question=d[0], answer1=d[1], answer2=d[2], answer3=d[3], answer4=d[4], message=message, message_color=message_color)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="40004", debug=True)
