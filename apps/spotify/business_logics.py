import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

credentials = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="838768b3bc9c48bd8d160baa756492e9",
                                                                    client_secret="390bd797fe464311a478e46af152d19c", ))


def retrieve_data_from_API(artist, countries):
    result = credentials.search(q=artist, type="artist", limit=1)
    artist_id = (result['artists']['items'][0]['id'])

    final_response_string = ""

    if len(countries) == 0:
        popular_tracks = credentials.artist_top_tracks(artist_id)
        audio = credentials.audio_analysis(popular_tracks["tracks"][0]["uri"])
        popular_tracks_list = []
        for idx, track in enumerate(popular_tracks["tracks"]):
            popular_tracks_list.append(f"{idx + 1}. {track['name']} | {track['popularity']}")

        final_response_string += "\n Top 10 Songs\n"

        for track in popular_tracks_list:
            final_response_string += track + "\n"

        return final_response_string

    for country in countries:
        popular_tracks = credentials.artist_top_tracks(artist_id, country=country)

        popular_tracks_list = []
        for idx, track in enumerate(popular_tracks["tracks"]):
            popular_tracks_list.append(f"{idx + 1}. {track['name']} | {track['popularity']}")

        final_response_string += "\n Top 10 Songs in " + country + "\n"

        for track in popular_tracks_list:
            final_response_string += track + "\n"

    return final_response_string


def color_gradation():
    # Define the colors in the desired order: black, blue, red, white
    colors = ['#000000', '#0000FF', '#FF0000', '#FFFF00', '#FFFFFF']

    # Create a colormap from the specified colors
    cmap = mcolors.LinearSegmentedColormap.from_list('custom_colormap', colors)

    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(6, 1))

    # Create a gradient image with the specified colormap
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.imshow(gradient, aspect='auto', cmap=cmap)

    # Save or display the color gradient
    plt.savefig('color_gradient.png', bbox_inches='tight')
    plt.show()
