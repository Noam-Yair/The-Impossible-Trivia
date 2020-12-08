# Overview
This is the main directory of our code.
- The application code resides in the APPLICATION-SOURCE-CODE directory
- The corpus directory holds the database loader of the corpus tables
- API-DATA-RETRIEVE.py is the script that downloads the movies data from the API and loads it onto the database

# How to run the server
Make sure you have python3.7 installed on your machine.
install the packages: flask, mysql.connector using the following command line:
```bash
python3.7 -m pip install mysql-connector flask
```

Got to the "APPLICATION-SOURCE-CODE" directory and run the following command line:
```bash
python3.7 server.py
```

Go to your browser and enter the following URL: http://localhost:40004 and enjoy the trivia
