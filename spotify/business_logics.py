import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

credentials = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="838768b3bc9c48bd8d160baa756492e9"
                                                                    , client_secret="390bd797fe464311a478e46af152d19c"))


def retrieve_data_from_API(artist, countries):
    result = credentials.search(q=artist, type="artist", limit=1)
    artist_id = (result['artists']['items'][0]['id'])

    final_response_string = ""

    for country in countries:
        popular_tracks = credentials.artist_top_tracks(artist_id, country=country)

        popular_tracks_list = []
        for idx, track in enumerate(popular_tracks["tracks"]):
            popular_tracks_list.append(f"{idx + 1}. {track['name']} | {track['popularity']}")

        final_response_string += "\n Top 10 Songs in " + country + "\n"

        for track in popular_tracks_list:
            final_response_string += track + "\n"

    return final_response_string


def test_numpy():
    ecom = pd.read_csv("C:\\Projects\\JupyterNotebook\\Py-DS-ML-Bootcamp-master\\Refactored_Py_DS_ML_Bootcamp-master"
                       "\\04-Pandas-Exercises\\Ecommerce Purchases")
    print(ecom.info())

    return "DONE!"


def test_matplotlib():
    x = np.linspace(0, 5, 11)
    y = x ** 2

    fig = plt.figure()
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.plot(x, y)
    axes.set_xlabel("X")
    axes.set_ylabel("Y")
    axes.set_title("X Y Relation")
    fig.show()

    return "DONE!"
