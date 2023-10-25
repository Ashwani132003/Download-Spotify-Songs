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

        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')

        

       

        # Initialize the Spotify client
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

        playlist_id = playlist.split('playlist/')[1].split('?')[0]

                
        limit = 100

        offset = 0  # Change this value as needed

        # List to store tracks
        tracks_details=[]
        while True:
            playlist = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
            st.write('valid playlist')
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

        st.write(len(tracks_details))
    

        downloaded=[]
        type = st.selectbox('Select Type:', ('None', 'Video', 'Audio'))

        if type != 'None':
            for i in tracks_details:
                i = list(i.items())[0]
                search_term = i[0] + ' ' + i[1] + ' lyrics'
        
                for _ in range(5):  # Try up to 5 times in case of rate limiting
                    try:
                        s = Search(search_term)
                        if len(s.results) > 0:
                            first_match_id = s.results[0].video_id
                            video_id = first_match_id
                            
                            url = f'https://www.youtube.com/watch?v={video_id}'
                            yt = YouTube(url)
        
                            if type == 'Video':
                                video_stream = yt.streams.get_highest_resolution()
                                video_stream.download()
                            if type == 'Audio':
                                audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
                                audio_stream.download()
        
                            # Log and indicate a successful download
                            st.write(f"Downloaded: {i[0]} - {i[1]}")
                            downloaded.append(i[0])
                            
                            # Break the retry loop if the download was successful
                            break
                        else:
                            st.error(f"No matching video found for: {search_term}")
                            break  # Exit the retry loop
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                        # Wait before retrying
                        time.sleep(60)  # Wait for 60 seconds before retrying
                else:
                    st.error(f"Max retries reached for: {search_term}")
        
            st.write('Download Complete')

    except Exception as e:
        print(e)
        pass        
else:
    st.write('Invalid Playlist Url')
