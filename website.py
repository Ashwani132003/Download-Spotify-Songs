import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import Search
from pytube import YouTube

from dotenv import load_dotenv
import os

load_dotenv()

playlist = st.text_input('Enter Playlist url: ')

if playlist:
    
    try:

        # Set your Spotify API credentials

        client_id = os.getenv('client_id')
        client_secret = os.getenv('client_secret')

        # client_id = '6d7408ab588744b1abf0f4fd26d3a9ef'
        # client_secret = '1f88c0c309d142ef8cc7f4d16a46e3c1'

        # Initialize the Spotify client
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

        # playlist_id = '6fzm3nkSSoKLsx0TA9ZuiS'
        playlist_id = playlist.split('playlist/')[1].split('?')[0]

                
        limit = 100

        offset = 0  # Change this value as needed

        # List to store tracks
        tracks_details=[]
        while True:
            playlist = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
            tracks = playlist['items']
            if not tracks:
                break

            for track in tracks:
                try:
                    name = track['track']['name']
                    artists = [artist['name'] for artist in track['track']['artists']]
                    tracks_details.append({name: ', '.join(artists)})
                except Exception as e:
                    print(f"Error processing track: {e}")

            offset += limit
        for track_detail in tracks_details:
            for name, artist in track_detail.items():
                print("Track Name:", name)
                print("Artists:", artist)
                print()  # Separate tracks with an empty line


    

        downloaded=[]
        type=st.selectbox('Select Type:',('None','Video','Audio'))

        if type!='None':
            for i in tracks_details:
                try:
                    i=list(i.items())[0]
                    search_term = i[0] +' '+ i[1] + 'lyrics'

                    s = Search(search_term)
                    first_match_id = s.results[0].video_id

                    video_id = first_match_id

                    # Create a YouTube object with the video URL
                    url = f'https://www.youtube.com/watch?v={video_id}'
                    yt = YouTube(url)

                    # Get the video stream with the highest resolution (or any other stream you prefer)
                    if type=='Video':
                        video_stream = yt.streams.get_highest_resolution()

                        # Download the video to a specified directory
                        download_directory = 'Downloaded'
                        video_stream.download(output_path=download_directory,filename=f"{i[0]} | {i[1]}.mp4")
                    if type=='Audio':
                        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

                        # Specify the download directory
                        download_directory = 'Downloaded'

                        # Download the audio as MP3 with the desired filename
                        audio_stream.download(output_path=download_directory, filename=f"{i[0]} | {i[1]}.mp3")
                        # print('done')
                    # You can also access various attributes of the video, such as title, description, author, etc.
                    print(f"Video Title: {yt.title}")
                    # print(f"Video Description: {yt.description}")
                    # print(f"Video Author: {yt.author}")

                    downloaded.append(i[0])
                except:pass
            st.write('Download Complete')    
    except Exception as e:
        print(e)
        pass        
else:
    st.write('Invalid Playlist Url')
