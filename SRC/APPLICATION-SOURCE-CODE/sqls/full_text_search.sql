(SELECT "movie" as row_type, any_value(corpus_movies.title) as row_value
FROM corpus_lines 
JOIN corpus_movies ON corpus_lines.movie_id = corpus_movies.id
WHERE MATCH (line) AGAINST("+{query}" IN BOOLEAN MODE)
group by movie_id
ORDER BY count(movie_id) DESC
LIMIT 5)

UNION ALL 

(SELECT "actor" as row_type, actors.name as row_value
FROM movies
JOIN movie_actors ON movies.id = movie_actors.movie_id
JOIN actors ON actors.id = movie_actors.actor_id
WHERE MATCH (overview) AGAINST("+{query}" IN BOOLEAN MODE)
AND actor_rank = 0
LIMIT 5)
