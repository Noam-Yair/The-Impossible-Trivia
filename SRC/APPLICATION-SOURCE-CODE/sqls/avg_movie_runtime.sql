SELECT
    CONCAT("Given the average run time of all the movies that ", GROUP_CONCAT(sub.actors_name)
, " acted in (not necessarily together), what is the average of all the three averages?") as question,
    AVG(avg_runtime) AS answer,
    0 as img,
    0 as option1,
    1 as option2,
    2 as option3
FROM
(	SELECT AVG(movies.runtime) AS avg_runtime, actors.name as actors_name, 1 as g
	FROM movies, actors, movie_actors
	WHERE (actors.rnd_token={actor_token1}
	OR actors.rnd_token={actor_token2}
	OR actors.rnd_token={actor_token3})
	AND actors.id = movie_actors.actor_id
	AND movie_actors.movie_id = movies.id
    AND movies.runtime>0
	GROUP BY actors.id) sub





