import spotipy
import spotipy.util as util
import re
import time
import json

sentence = str(input('Sentence to create a playlist from? '))
sentence = sentence.replace("-", " ")
sentence = re.sub('[!.,"?()“”‘’]','',sentence) #replaces punctuation with nothing as i've seen the program have trouble with them before
converted_sentence = sentence.lower().split()

results = []
ids = []

#title = str(input('Enter a title for your playlist. '))

scope = 'playlist-modify-public'
redirect_url = 'http://localhost:8080'

with open("credentials.json") as file:
    credentials = json.load(file)

print(credentials)

username, client_id, client_secret = credentials["username"], credentials["client_id"], credentials["client_secret"]

token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret,redirect_uri=redirect_url)

def start(sp):
    sp.trace = False

    for word in converted_sentence:
        data = search(word)
        for id in data:
            if id == None: continue
            ids.append(id)

    print("Fully generared IDs!")

    print(ids)

    file = open("ids.txt", "w")
    string = ""
    for id in ids:
        if id != None:
            string += id+"\n"
    file.write(string)
    file.close()

    # Call our other module
    import GeneratePlaylistFromFile

def search(word):
    try:
        song_names = set()
        i = -1
        while len(song_names) == 0 or word.lower() not in song_names:
            i += 1
            if i <= 15:
                #print(i)
                results = sp.search(word, limit=50, offset=i*50, type='track', market=None)
                for item in results['tracks']['items']:
                    song_names.add(item['name'].lower())
                    
                #print(song_names)
            else: # splitting if searched 750 results, otherwise it'll just hit the max searches and end
                split = list(word)
                ids = []
                if len(split) == 1: break
                for letter in split:
                    ids.append(*search(letter))
                return ids
                break

        for item in results['tracks']['items']:
            if item['name'].lower() == word:
                #print(song_ids)
                print(word)

                return [item["id"]]
    except:
        print(f"Search failed for word \"{word}\", retrying in 5 seconds")
        time.sleep(5)
        return search(word)

if token:
    sp = spotipy.Spotify(auth=token)
    start(sp)
else:
    print('Cant get token for', username)