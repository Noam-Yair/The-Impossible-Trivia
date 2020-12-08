# Overview
This script generates the tables "corpus_movies" and "corpus_lines"

# How to run this script
- In order to run this script you need to go to the website: https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html
- Download the Zip file
- extract the files to the same directory as the python script

Then, run the following command (Substitute the parameters to match your database credentials):
```python
python3.7 load_corpus_to_db.py -s [database_server] -u [database_username] -p [database_password] -d [database_name]
```
