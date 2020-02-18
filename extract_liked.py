import json

import requests

from SpotifyAPI import SpotifyAPI



def get_urls(track_ids):
    print('Preparing urls...')

    url = '/audio-features/?ids='
    urls = []
    count = 0
    current_url = url

    while track_ids:
        track_id = track_ids.pop()
        current_url += track_id + ','
        count += 1
        if count % 10 == 0:
            urls.append(current_url[:-1])
            current_url = url

    urls.append(current_url[:-1])
    return urls


def append_features(features, urls):
    print('Extracting features')

    for url in urls:
        track_features = spotify_api.request_data(url, token=token)
        audio_features = track_features['audio_features']
        for audio_feature in audio_features:
            if audio_feature is None:
                continue
            audio_feature.pop('type')
            audio_feature.pop('id')
            audio_feature.pop('uri')
            audio_feature.pop('track_href')
            audio_feature.pop('analysis_url')
            audio_feature.pop('duration_ms')
            audio_feature.pop('time_signature')
            audio_feature.pop('energy')
            audio_feature.pop('liveness')


            track_feature_list = []
            for key, feat in audio_feature.items():
                if key == key_t:
                    histogram_values.append(feat)
                track_feature_list.append(feat)
            features.append(track_feature_list)


spotify_api = SpotifyAPI()
token = ''
print('Getting Liked songs...')
liked_songs = spotify_api.get_liked_songs(token)
track_ids = []
next = liked_songs['next']

while next != 'null':
    for track in liked_songs['items']:
        track_id = track['track']['id']
        track_ids.append(track_id)
    header = {'Authorization': 'Bearer ' + token} if token else None
    if next is None:
        break
    response = requests.get(next, headers=header)
    liked_songs = json.loads(response.text)
    next = liked_songs['next']

playlists_ids = []
with open('good_playlist_urls.txt') as file:
    for line in file.readlines():
        playlists_ids.append(line)

print('Getting good playlists...')
for playlist_id in playlists_ids:
    tracks = spotify_api.get_playlist_tracks(token, playlist_id[:-1])['items']
    for track in tracks:
        track_id = track['track']['id']
        track_ids.append(track_id)

features = []
urls = get_urls(track_ids)
append_features(features, urls, token)
with open('features.csv', 'w') as csv:
    for feature in features:
        for val in feature:
            csv.write(str(val) + ',')
        csv.write('like')
        csv.write('\n')

playlists_ids = []
track_ids = []
with open('bad_playlist_urls.txt') as file:
    for line in file.readlines():
        playlists_ids.append(line)

print('Getting bad playlists...')
for playlist_id in playlists_ids:
    tracks = spotify_api.get_playlist_tracks(token, playlist_id[:-1])['items']
    for track in tracks:
        track_id = track['track']['id']
        track_ids.append(track_id)

features = []
urls = get_urls(track_ids)
append_features(features, urls, token)

with open('features.csv', 'a') as csv:
    for feature in features:
        for val in feature:
            csv.write(str(val) + ',')
        csv.write('dislike')
        csv.write('\n')

print('Done!')