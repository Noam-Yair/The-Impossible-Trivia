#!/usr/bin/env python

import mysql.connector
import argparse
import math
import asyncio
import aiohttp
import aiofiles
import json

API_URL = "https://api.themoviedb.org/3/discover/movie?page={}&append_to_response=images&include_adult=false&region=US&vote_average.lte=10&vote_count.gte=10&language=en&sort_by=popularity.desc&vote_average.gte=1&api_key=d7968a4878331fa01877eaca1a6a24da"
MOVIE_DATA_API_URL = "https://api.themoviedb.org/3/movie/{}?append_to_response=images%2Ckeywords%2Ccredits%2Ctrailers%2Crelease_dates&language=en&api_key=d7968a4878331fa01877eaca1a6a24da"
MAX_CONCURRENT_TASKS = 20
PAGES_CHUNKS = 40
MOVIE_TABLE_INSERT = """INSERT INTO movies(id,imdb_id,title,original_title,overview,popularity,poster_path,release_date,status,tagline,vote_average,vote_count)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
ACTOR_TABLE_INSERT = """INSERT INTO actors(id,name,popularity,profile_path)
                        VALUES(%s,%s,%s,%s)"""
MOVIE_ACTORS_TABLE_INSERT = """INSERT INTO movie_actors(movie_id,actor_id,character_name)
                               VALUES(%s,%s,%s)"""
GENRES_TABLE_INSERT = """INSERT INTO genres(id,name)
                         VALUES(%s,%s)"""
MOVIE_GENRES_TABLE_INSERT = """INSERT INTO movie_genres(movie_id,genre_id)
                               VALUES(%s,%s)"""
MAXIMUM_ROW_EXECUTE_MANY = 400

MAXIMUM_MOVIES_PER_COMMIT = 1000

async def download_movie_data(sem, session, movie_id):
    async with sem:
        async with session.get(MOVIE_DATA_API_URL.format(movie_id)) as r:
            return await r.json()

async def download_page(sem, session, page):
    async with sem:
        print(f"Downloading page {page}")
        async with session.get(API_URL.format(page)) as r:
            return await r.json()

async def download_page_results(sem, session, page):
    results = (await download_page(sem, session, page))["results"]
    tasks = [download_movie_data(sem, session, movie["id"]) for movie in results]
    return await asyncio.gather(*tasks)

async def get_page_count(sem, session):
    data = await download_page(sem, session, 1)
    return data["total_pages"]

async def download_data(output_path):
    sem = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
    async with aiohttp.ClientSession() as session:
        page_count = await get_page_count(sem, session)
        print(f"Downloading {page_count} pages")
        async with aiofiles.open(output_path, "w") as f:
            for i in range(1, page_count + 1, PAGES_CHUNKS):
                tasks = [download_page_results(sem, session, page) for page in range(i, min(i + PAGES_CHUNKS, page_count + 1))]
                data = await asyncio.gather(*tasks)
                print("Saving data to json file")
                for page_results in data:
                    for movie_data in page_results:
                        await f.write(json.dumps(movie_data)+"\n")
        print("Done!")

def get_image_url(image_id):
    if image_id is None:
        return None
    return f"https://image.tmdb.org/t/p/w1280{image_id}"

async def fill_database(db_server, db_user, db_pass, db_name, output_path):
    db = mysql.connector.connect(host=db_server, user=db_user, password=db_pass, database=db_name)
    actors_mask = set()
    genres_mask = set()
    counter = 0
    with db.cursor() as cur:
        async with aiofiles.open(output_path, "r") as f:
            async for movie_json in f:
                counter += 1
                movie_data = json.loads(movie_json)
                # Uploading movie data
                cur.execute(MOVIE_TABLE_INSERT, 
                            (movie_data["id"],
                             movie_data["imdb_id"],
                             movie_data["title"],
                             movie_data["original_title"],
                             movie_data["overview"],
                             movie_data["popularity"],
                             get_image_url(movie_data['poster_path']),
                             movie_data["release_date"],
                             movie_data["status"],
                             movie_data["tagline"],
                             movie_data["vote_average"],
                             movie_data["vote_count"]))

                # Uploading genres data
                movie_genres_mask = set()
                for genre in movie_data["genres"]:
                    if genre["id"] not in genres_mask:
                        cur.execute(GENRES_TABLE_INSERT, (genre["id"], genre["name"]))
                        genres_mask.add(genre["id"])
                    if (movie_data["id"], genre["id"]) not in movie_genres_mask:
                        cur.execute(MOVIE_GENRES_TABLE_INSERT, (movie_data["id"], genre["id"]))
                        movie_genres_mask.add((movie_data["id"], genre["id"]))

                # Uploading actors data
                movie_actors_mask = set()
                for actor in movie_data["credits"]["cast"]:
                    if actor["id"] not in actors_mask:
                        cur.execute(ACTOR_TABLE_INSERT, ((actor["id"], actor["name"], actor["popularity"], get_image_url(actor['profile_path']))))
                        actors_mask.add(actor["id"])
                    if (movie_data["id"], actor["id"]) not in movie_actors_mask:
                        cur.execute(MOVIE_ACTORS_TABLE_INSERT, ((movie_data["id"], actor["id"], actor["character"])))
                        movie_actors_mask.add((movie_data["id"], actor["id"]))

                # Need to commit changes every once in a while because if transaction is too large it throws an error
                if counter % MAXIMUM_MOVIES_PER_COMMIT == 0:
                    print("Commiting changes..")
                    db.commit()
    db.commit()
    db.close()


async def main(db_server, db_user, db_pass, db_name):
    #await download_data("output.json")
    await fill_database(db_server, db_user, db_pass, db_name, "output.json")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", help="DB server")
    parser.add_argument("-u", "--user", help="DB User Name")
    parser.add_argument("-p", "--password", help="DB password")
    parser.add_argument("-d", "--database", help="DB name")
    args = parser.parse_args()
    asyncio.run(main(args.server, args.user, args.password, args.database))
