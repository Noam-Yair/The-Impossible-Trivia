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
    return f"https://image.tmdb.org/t/p/w1280{image_id}",

async def fill_database(db_server, db_user, db_pass, db_name, output_path):
    db = mysql.connector.connect(host=db_server, user=db_user, password=db_pass, database=db_name)
    m = 0
    actors = set()
    with db.cursor() as cur:
        async with aiofiles.open(output_path, "r") as f:
            async for movie_json in f:
                movie_data = json.loads(movie_json)
                #  m = max(m, len(movie_data["tagline"]))
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
                for actor in movie_data["credits"]["cast"]:
                    actors.add((actor["id"], actor["name"], actor["popularity"], get_image_url(actor['profile_path'])))
        import ipdb;ipdb.set_trace()
        cur.executemany(ACTOR_TABLE_INSERT, list(actors))
    #  print(m)
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
