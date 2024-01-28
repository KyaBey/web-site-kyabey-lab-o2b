from flask import Flask, render_template
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

# Acesse as variáveis de ambiente
youtube_api_key = os.getenv("YOUTUBE_API_KEY")

app = Flask(__name__)

# Configure a sua chave de API do YouTube
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

def get_videos_from_playlist(playlist_id):
    playlist_items = youtube.playlistItems().list(part='snippet', playlistId=playlist_id, maxResults=50).execute()
    video_info = [
        {
            'title': video['snippet']['title'],
            'video_id': video['snippet']['resourceId']['videoId'],
            'artist': video['snippet'].get('videoOwnerChannelTitle', ''),
            'thumbnail_url': f'https://img.youtube.com/vi/{video["snippet"]["resourceId"]["videoId"]}/hqdefault.jpg'
        }
        for video in playlist_items['items']
    ]
    return video_info

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/tecnologia')
def tecnologia():
    playlist_id_tecnologia = 'PLhJX2ocKV9F36YDuKCsvlUMqhxLfjkcpt'
    videos_tecnologia = get_videos_from_playlist(playlist_id_tecnologia)
    return render_template('playlist.html', title='Tecnologia', videos=videos_tecnologia)

@app.route('/musica')
def musica():
    playlist_id_musica = 'PLhJX2ocKV9F2aoxd23VAYKFi1THeKFgml'
    videos_musica = get_videos_from_playlist(playlist_id_musica)
    return render_template('playlist.html', title='Música', videos=videos_musica)

if __name__ == '__main__':
    app.run(debug=True)
