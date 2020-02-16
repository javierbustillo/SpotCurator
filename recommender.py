import numpy
from joblib import load

from SpotifyAPI import SpotifyAPI

spotify_api = SpotifyAPI()
token = 'BQBuFgk04t4slN45Ym7vAcoYVwOgabqtFjoFePhL_2Tqafvib41wdSmSg5UJ6xAFZlxFZiJHqP2DcRUs8B6kfNRSA0LTGlZXBYaac3Adpj3zg-tXzZgz1MjvxEYj1JU1-sdwBasXw0e6aDiOyeri4aYTPYP5A7h1Ek_GTcrbbtNdcmuMltg0dKQ8WvZhvGSdJ43silHSkEs2gubHxJAryujMoxay95xUu7QE5i3MXrkPLw'
recommender = load('recommender.joblib')
print('Write the track id')
spotify_uri = input()
spotify_id = spotify_uri.split(':')[2]
audio_features = spotify_api.get_features(token, spotify_id)
audio_features.pop('type')
audio_features.pop('id')
audio_features.pop('uri')
audio_features.pop('track_href')
audio_features.pop('analysis_url')

feat = []
for value in audio_features.values():
    feat.append(value)

print(recommender.predict([numpy.array(feat)]))
