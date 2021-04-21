## Purpose of the Database
This database is a built to help Sparkify migrate the data which is in JSON file into Postreg database. Also it will help to bring more structure to their database and make querying it easy and more efficient. It will also make analytics easy.


### Schema for Song Play Analysis
A star schema will optimize queries on song play analysis. The fact table will contain the ids of the various dimensions tables which will make query more efficient. Below are the tables.

### Fact Table
1. songplays - records in log data associated with song plays i.e. records with page NextSong
- songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables
2. users - users in the app  
- user_id, first_name, last_name, gender, level
3. songs - songs in music database
- song_id, title, artist_id, year, duration
4. artists - artists in music database
- artist_id, name, location, latitude, longitude
5. time - timestamps of records in songplays broken down into specific units
- start_time, hour, day, week, month, year, weekday
   
## Sample query
%sql SELECT * FROM users LIMIT 5;

user_id|first_name|last_name|gender|level

91     |Jayden    |Bell     |M     |free  
73     |Jacob     |Klein    |M     |paid
