import numpy
from joblib import load

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


def append_features(features, urls, token):
    print('Extracting features...')

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
            for feat in audio_feature.values():
                track_feature_list.append(feat)
            features.append(track_feature_list)


spotify_api = SpotifyAPI()
token = 'BQC3dRvY1fUE-TVMAWe_SiV1oA58pK70rfEv9QanozwhNjnoJBSiEuXdhNbdCMA6f3EhQqS2e-4eLnirQUydyVc9YPqHRIxqnR3JlFmMVgsLM5keYMRbhRBFpZYENzXsvm1SDXLsOr8bVQQ-RA9lcLOTiAhaMHXO4krn34jS2LoasbUnMV_u1NBhe8PDctm9hTldrhiZrzWW9slDJr7zKEOqEtgNucDle0t3zIh_yROoLw'
recommender = load('recommender.joblib')

print('1. Playlist\n2. Track')
option = input()

if option == '1':
    print('Write the playlist URI')
    spotify_uri = input()
    spotify_id = spotify_uri.split(':')[2]
    tracks = spotify_api.get_playlist_tracks(token, spotify_id)['items']
    track_ids = []
    track_names = []
    for track in tracks:
        track_id = track['track']['id']
        track_name = track['track']['name']
        track_ids.append(track_id)
        track_names.append(track_name)

    features = []
    urls = get_urls(track_ids)
    append_features(features, urls, token)

    for index, feature in enumerate(features):
        print("You will " + recommender.predict([numpy.array(feature)])[0] + ' %s' % track_names[index])


else:
    print('Write the track id')
    spotify_uri = input()
    spotify_id = spotify_uri.split(':')[2]
    audio_features = spotify_api.get_features(token, spotify_id)
    audio_features.pop('type')
    audio_features.pop('id')
    audio_features.pop('uri')
    audio_features.pop('track_href')
    audio_features.pop('analysis_url')
    audio_features.pop('key')
    audio_features.pop('duration_ms')
    audio_features.pop('time_signature')
    audio_features.pop('mode')

    feat = []
    for value in audio_features.values():
        feat.append(value)

    print(recommender.predict([numpy.array(feat)]))



