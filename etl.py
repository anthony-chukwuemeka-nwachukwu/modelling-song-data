import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
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
    pass


def process_data(cur, conn, filepath, func):
    pass


def main():
    pass


if __name__ == "__main__":
    main()
