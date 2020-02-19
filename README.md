# SpotifyRecommender
Your own personal music curator


Tired of having to listen to songs to figure out if you like them? Then you have reached the right place!

These simple scripts use machine learning to, well, learn what kind of songs you like and don't like. After that you send it a song and it'll tell you if you'd like it or dislike it

So first you need to scrape spotify for the songs you like

[Here](https://developer.spotify.com/console/get-current-user-contains-saved-tracks/) you can find a way to generate the token necesarry to scrape your liked songs from spotify. If you feel like that's not enough then you can create a text file called **good_playlist_urls.txt** and fill it with the ids of playlists you like. Make sure to generate the correct token if using private playlists.

Once the token is generated update the correct line with the correct token in **extract_liked.py** and **recommender.py**:
`token = ''`

Run **extract_liked.py** firs
Then run **train.py**
Then run **recommender.py** and when asked for track or playlist send the SPOTIFY URI. 

