# Overview
This is the main directory of our code.
- The application code resides in the APPLICATION-SOURCE-CODE directory
- The corpus directory holds the database loader of the corpus tables
- API-DATA-RETRIEVE.py is the script that downloads the movies data from the API and loads it onto the database

# How to run the server
Make sure you have python3.7 installed on your machine.
Install the packages: flask, mysql.connector using the following command line:
```bash
python3.7 -m pip install mysql-connector flask
```

Got to the "APPLICATION-SOURCE-CODE" directory and run the following command line:
```bash
python3.7 server.py
```

Go to your browser and enter the following URL: http://localhost:40004 and enjoy the trivia

# How to run the API data retriever
Make sure you have python3.7 installed on your machine.
Install the packages: mysql-connectorm, aiohttp, aiofiles using the following command line:
```bash
python3.7 -m pip install mysql-connector aiohttp aiofiles
```

Before running the script make sure you created the relevant tables and all of them are empty. Don't run this script on our deployment db without speaking with your team leader.
run the following command (Substitute the parameters to match your database credentials):
```bash
python3.7 API-DATA-RETRIEVE.py -s [database_server] -u [database_username] -p [database_password] -d [database_name]
```

