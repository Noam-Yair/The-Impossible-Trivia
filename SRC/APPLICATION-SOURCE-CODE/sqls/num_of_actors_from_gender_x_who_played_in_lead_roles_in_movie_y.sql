SELECT
    CONCAT("How many " , IF(actors.gender = 1, "female actresses ", "male actors ")
    , "play in the top three leading roles in the movie ", movies.title, " ?") as question,
    COUNT(actors.id) AS answer,
    ANY_VALUE(movies.poster_path) as img,
    0 as option1,
    1 as option2,
    2 as option3
FROM
    movies
    LEFT JOIN
        movie_actors ON movies.id = movie_actors.movie_id
    LEFT JOIN
    actors ON actors.id = movie_actors.actor_id
WHERE
    movies.rnd_token = {movies_token}
    AND actors.gender={gender_token}
    AND movie_actors.actor_rank<3
ORDER BY movie_actors.actor_rank




