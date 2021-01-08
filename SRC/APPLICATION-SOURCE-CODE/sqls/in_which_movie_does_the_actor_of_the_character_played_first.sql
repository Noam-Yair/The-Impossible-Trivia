SELECT
    CONCAT("In what movie does the actor of the character '", ANY_VALUE(movie_actors.character_name),
    "' in the movie '", ANY_VALUE(movies.title), "' has made his first appearance?") as question,
    actor_id AS our_ACTOR_id,
    (SELECT movies.title
	FROM
		movies, movie_actors
	WHERE
		movies.id = movie_actors.movie_id AND
        movie_actors.actor_id = our_ACTOR_id
	ORDER BY release_date
	LIMIT 1 ) as answer,
    actors.profile_path AS img,
    (SELECT movies.title FROM movies WHERE movies.rnd_token = {movie_token1}) as option1,
    (SELECT movies.title FROM movies WHERE movies.rnd_token = {movie_token2}) as option2,
    (SELECT movies.title FROM movies WHERE movies.rnd_token = {movie_token3}) as option3
    
FROM
	actors
        LEFT JOIN
    movie_actors ON actors.id = movie_actors.actor_id
        LEFT JOIN
    movies ON movies.id = movie_actors.movie_id
WHERE
movies.rnd_token = {movie_token}
ORDER BY release_date
LIMIT 1

