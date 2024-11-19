#!/usr/bin/env python3
import mysql.connector
import os
from mysql.connector import Error
from fastapi import FastAPI

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "esd4uq"

#bring all of these elements together into a single DB connection string, and create a cursor using that
db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

app = FastAPI()

def read_root():
    return {"message": "Hello, FastAPI!"}

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    
@app.get('/songs')
def get_songs():
    query = """
    SELECT 
        songs.title AS title, 
        songs.album AS album, 
        songs.artist AS artist, 
        songs.year AS year, 
        songs.file AS file, 
        songs.image AS image,
        genres.genre AS genre
    FROM 
        songs
    JOIN 
        genres ON songs.genre = genres.genreid
    ORDER BY
        songs.title;
    """
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = [dict(zip(headers, result)) for result in results]
        return json_data
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}