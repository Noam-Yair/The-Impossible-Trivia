SELECT "Neither" AS option0,
       (SELECT actors.name FROM actors WHERE actors.rnd_token = {actor_token1}) AS option1,
       "Both" AS option2,
       (SELECT actors.name FROM actors WHERE actors.rnd_token = {actor_token2}) AS option3,
       IF(COUNT(actors.rnd_token) <> 1, COUNT(actors.rnd_token), IF(MIN(actors.rnd_token) = {actor_token1}, 1, 3)) AS answer,
       CONCAT("Which of these actors played in a movie that was rated more than ", {rating_token}, " on imdb?") AS question
FROM actors
WHERE (actors.rnd_token = {actor_token1} OR actors.rnd_token = {actor_token2}) AND
	  EXISTS (SELECT movies.vote_average
			  FROM movie_actors, movies
			  WHERE actors.id = movie_actors.actor_id AND movies.id = movie_actors.movie_id
					AND vote_average > {rating_token}
			 )