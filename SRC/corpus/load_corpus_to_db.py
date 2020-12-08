#!/usr/bin/env python

import mysql.connector
import argparse
import math
import asyncio
import aiohttp
import aiofiles
import json

DELIMITER = " +++$+++ "
CORPUS_MOVIES_TABLE_INSERT = """INSERT INTO corpus_movies(id,title,release_year,imdb_rating,votes_count,rnd_token)
                                VALUES(%s,%s,%s,%s,%s,%s)"""
CORPUS_LINES_TABLE_INSERT = """INSERT INTO corpus_lines(id,character_id,movie_id,character_name,line,rnd_token)
                                VALUES(%s,%s,%s,%s,%s,%s)"""
TRANSACTION_ROW_COUNT = 1000

def convert_movie_row_to_correct_types(row):
    return [row[0], row[1], int(row[2].split("/")[0]), float(row[3]), int(row[4])]

def load_movie_titles_meta_data(db):
    counter = 0
    with open("movie_titles_metadata.txt", "r", errors="replace") as f:
        with db.cursor() as cur:
            for row in f:
                data = convert_movie_row_to_correct_types(row.split(DELIMITER)[:-1])
                data.append(counter)
                cur.execute(CORPUS_MOVIES_TABLE_INSERT, tuple(data))
                counter += 1
            db.commit()

def load_movie_lines_data(db):
    counter = 0
    with open("movie_lines.txt", "r", errors="replace") as f:
        with db.cursor() as cur:
            for row in f:
                data = row.split(DELIMITER)
                data.append(counter)
                cur.execute(CORPUS_LINES_TABLE_INSERT, tuple(data))
                counter += 1
                if counter % TRANSACTION_ROW_COUNT == 0:
                    db.commit()
                    print("Commited transaction..")
            db.commit()

def main(db_server, db_user, db_pass, db_name):
    db = mysql.connector.connect(host=db_server, user=db_user, password=db_pass, database=db_name)
    print("Uploading corpus movie data")
    load_movie_titles_meta_data(db)
    print("Uploading corpus lines")
    load_movie_lines_data(db)
    db.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", help="DB server")
    parser.add_argument("-u", "--user", help="DB User Name")
    parser.add_argument("-p", "--password", help="DB password")
    parser.add_argument("-d", "--database", help="DB name")
    args = parser.parse_args()
    main(args.server, args.user, args.password, args.database)
