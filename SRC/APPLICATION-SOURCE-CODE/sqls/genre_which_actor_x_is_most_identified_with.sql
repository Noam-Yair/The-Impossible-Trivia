SELECT
    CONCAT("What is the movie genre that actor ",actors.name, "is most identified with?") as question,
    genres.name AS answer,
    actors.profile_path as img,
    (SELECT a.name FROM genres as a WHERE a.rnd_token = MOD(genres.rnd_token + 1, (SELECT count(*) FROM genres))) as option1,
    (SELECT a.name FROM genres as a WHERE a.rnd_token = MOD(genres.rnd_token + 2, (SELECT count(*) FROM genres))) as option2,
    (SELECT a.name FROM genres as a WHERE a.rnd_token = MOD(genres.rnd_token + 3, (SELECT count(*) FROM genres))) as option3
FROM
	actors, genres, movie_actors, movie_genres
WHERE
	actors.id = movie_actors.actor_id AND
	movie_actors.movie_id = movie_genres.movie_id AND
	movie_genres.genre_id = genres.id AND
	actors.rnd_token = {actor_token}
GROUP BY genres.id
ORDER BY count(genres.id) DESC
LIMIT 1
