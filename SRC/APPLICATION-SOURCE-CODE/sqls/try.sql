SELECT 
    CONCAT("What is the name of the ", ANY_VALUE(genres.name), " movie", " that the actor ", actors.name, " acted for the first time?") as question,
    title AS answer,
    ANY_VALUE(actors.profile_path) as img,
    (SELECT title FROM movies WHERE rnd_token = {movie_token1}) as option1,
    (SELECT title FROM movies WHERE rnd_token = {movie_token2}) as option2,
    (SELECT title FROM movies WHERE rnd_token = {movie_token3}) as option3
FROM
    actors
        LEFT JOIN
    movie_actors ON actors.id = movie_actors.actor_id
        LEFT JOIN
    movies ON movies.id = movie_actors.movie_id
        LEFT JOIN
    movie_genres ON movies.id = movie_genres.movie_id
        LEFT JOIN
    genres ON genres.id = movie_genres.genre_id
WHERE
    actors.rnd_token = {actor_token}
GROUP BY title , release_date
ORDER BY release_date
LIMIT 1
