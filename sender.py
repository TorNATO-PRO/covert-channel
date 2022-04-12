import os
import random
import time
import requests
import pandas as pd

from typing import List, Optional

# define global constants
ACCESS_TOKEN = ''
PLAYLIST_DB = pd.read_csv('gigachad_playlist.csv')
PLAYLIST_DB = PLAYLIST_DB[~PLAYLIST_DB['Track URI'].str.contains('^spotify:local', regex=True, na=False)]
PLAYLIST_DB.reset_index(inplace=True)
TRACK_DICT = {row['Track URI']: row['Track Name'] for _, row in PLAYLIST_DB.iterrows()}
TRACK_URIS = PLAYLIST_DB['Track URI']
TIMEOUT_FLOOR = 5
TIMEOUT_CEILING = 20

def add_tracks_to_playlist(track_list: List[str], playlist_id: str) -> None:
    """
    Adds a list of tracks to a spotify playlist.

    :param track_list: A list of tracks.
    :type track_list: List[str]
    :param playlist_id: The playlist id.
    :type playlist_id: str

    :return: Nothing, a network I/O operation.
    """
    # sets the current status code
    index = 0
    while index < len(track_list):
        current_timeout = random.uniform(TIMEOUT_FLOOR, TIMEOUT_CEILING)
        print(f'Adding track: {track_list[index]}')
        req = requests.post(
            f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {ACCESS_TOKEN}'
            },
            json={
                'uris': [track_list[index]]
            }
        )

        if req.status_code == 201:
            index += 1

            # avoid waiting
            if index == len(track_list):
                break
        elif req.status_code == 400:
            print(f'No idea what 400 means since it isn\'t documented, but that is the status code')
        elif req.status_code == 401:
            print('Expired token! Please retrieve another access token')
            break
        elif req.status_code == 403:
            print('Bad OAuth request, wrong consumer key or expired timestamp. :(')
            break
        elif req.status_code == 429:
            print(f'Being rate limited, retrying in {current_timeout} seconds')

        print(req.json())

        time.sleep(current_timeout)

    print('Message posted successfully')


def create_playlist(name: str) -> Optional[str]:
    """
    Creates a playlist with a given name.

    :param name: The new playlist's name.
    :type name: str

    :return: The ID of the newly created playlist.
    """
    status_code = 0
    playlist_id = None
    while status_code != 201:
        current_timeout = random.uniform(TIMEOUT_FLOOR, TIMEOUT_CEILING)
        response = requests.post(
            'https://api.spotify.com/v1/users/piano_l0rd/playlists',
            headers={
                'Authorization': f'Bearer {ACCESS_TOKEN}'
            },
            json={
                'name': name,
                'public': False,
                'description': 'Definitely Not Sus'
            }
        )

        status_code = response.status_code
        if status_code == 201:
            playlist_id = response.json()['id']
        elif status_code == 401:
            print('Expired token! Please retrieve another access token')
            break
        elif status_code == 403:
            print('Bad OAuth request, wrong consumer key or expired timestamp. :(')
            break
        elif status_code == 429:
            print(f'Being rate limited, retrying in {current_timeout} seconds')
            time.sleep(current_timeout)


    return playlist_id

# get the user input
message = input('Enter the secret message: ')

# convert it to a decodable format for transmission
message_track_ids = (ord(c) + 255 * random.randint(0, len(PLAYLIST_DB) // 255 - 1) for c in message)

# query the tracks at that index
tracks = [TRACK_URIS[index] for index in message_track_ids]

# # create a new playlist to add to the track
playlist_id = create_playlist('amogus')

if playlist_id is not None:
    # adds tracks to the playlist
    add_tracks_to_playlist(tracks, playlist_id)
    
    # display the decoded message
    print(''.join([chr(c % 255) for c in message_track_ids]))
else:
    print('Something went wrong!')
