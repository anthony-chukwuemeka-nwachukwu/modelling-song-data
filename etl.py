import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This procedure processes a song file whose filepath has been provided as an arugment.
    It extracts the song information in order to store it into the songs table.
    Then it extracts the artist information in order to store it into the artists table.

    INPUTS:
    * cur the cursor variable
    * filepath the file path to the song file
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    d = df.to_dict('records')[0]
    song_data = [d["song_id"], d["title"], d["artist_id"], d["year"], d["duration"]]
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = [d["artist_id"], d["artist_name"], d["artist_location"], d["artist_latitude"], d["artist_longitude"]]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This procedure processes a log file whose filepath has been provided as an arugment.
    It extracts the log information in order to store it into the user table and songPlay table.

    INPUTS:
    * cur the cursor variable
    * filepath the file path to the song file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    ts = pd.to_datetime(df['ts'], unit='ms')
    for t in ts:
        time_data = [t, t.hour, t.day, t.week, t.month, t.year, t.day_name()]
        cur.execute(time_table_insert, time_data)

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
        pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location,
        row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This procedure extracts files in a given file path.
    It then makes a call to provided function and executes it with the processed file.

    INPUTS:
    * cur the cursor variable
    * conn the connection variable
    * filepath the file path to the song file
    * func the function name
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    This procedure processes the process data for the song and log files.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()