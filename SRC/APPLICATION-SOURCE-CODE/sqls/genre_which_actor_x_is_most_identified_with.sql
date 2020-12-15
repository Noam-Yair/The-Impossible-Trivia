SELECT
    CONCAT("What is the movie genre that actor ",ANY_VALUE(actors.name), "is most identified with?") as question,
    genres.name AS answer,
    ANY_VALUE(actors.profile_path) as img,
    (SELECT genres.name FROM genres WHERE rnd_token = {genre_token1}) as option1,
    (SELECT genres.name FROM genres WHERE rnd_token = {genre_token2}) as option2,
    (SELECT genres.name FROM genres WHERE rnd_token = {genre_token3}) as option3
FROM
	actors, genres, movie_actors, movie_genres
WHERE
	actors.id = movie_actors.actor_id AND
	movie_actors.movie_id = movie_genres.movie_id AND
	movie_genres.genre_id = genres.id AND
	actors.id = {actor_token}
GROUP BY genres.id
ORDER BY count(genres.id) DESC
LIMIT 1