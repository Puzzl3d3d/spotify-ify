file = open("ids.txt", "r")
data = [line.strip() for line in file.readlines()]

import spotipy
import spotipy.util as util
import re
import time
import json

scope = 'playlist-modify-public'
redirect_url = 'http://localhost:8080'

with open("credentials.json") as file:
    credentials = json.load(file)

print(credentials)

username, client_id, client_secret = credentials["username"], credentials["client_id"], credentials["client_secret"]

token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret,redirect_uri=redirect_url)

title = input("Title of playlist: ")

chunk_size = 50

def add_chunk(i):
    try:
        sp.playlist_add_items(playlist_id, data[i:i+chunk_size])
        print(f"Chunk {i/chunk_size} of {round(len(data) / chunk_size)} finished")
    except:
        print(f"Failed chunk {i/chunk_size}, retrying in 5 seconds")
        time.sleep(5)
        add_chunk(i)

if token:
    sp = spotipy.Spotify(auth=token)

    playlist = sp.user_playlist_create(username, title, public=True, collaborative=False, description="Made with the playlist generator by dootw and modified by puzzl3d")
    playlist_id = playlist["id"]

    print("Starting", playlist_id)

    #sp.playlist_add_items(playlist_id, data)

    for i in range(0, len(data), chunk_size):
        add_chunk(i)
    print("Completed!", playlist_id)
else:
    print('Cant get token for', username)
