from dotenv import load_dotenv
from flask import Flask, request, Response
from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
from flask import Flask, render_template
from prometheus_client.exposition import MetricsHandler  # Adicionada esta importação
import time
import os
from googleapiclient.discovery import build

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

# Acesse as variáveis de ambiente
youtube_api_key = os.getenv("YOUTUBE_API_KEY")

app = Flask(__name__)

# Métrica para contar erros
error_count = Counter('app_errors_total', 'Total number of errors')

# Métrica para contar requisições
request_count = Counter('app_requests_total', 'Total number of requests')

# Métrica para medir o tempo de resposta das rotas
request_duration = Histogram('app_request_duration_seconds', 'Request duration in seconds', ['route'])

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
    request_count.inc()
    with request_duration.labels(route='home').time():
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

# Rota para gerar erros intencionalmente
@app.route('/generate-error')
def generate_error():
    try:
        # Simulando uma exceção
        1 / 0
    except Exception as e:
        # Incrementando a métrica de erros
        error_count.inc()
        return f"Erro gerado: {str(e)}", 500

# Rota para expor métricas do Prometheus com quebras de linha
@app.route('/metrics')
def metrics():
    metrics_data = generate_latest(REGISTRY)
    return Response(metrics_data, content_type='text/plain; version=0.0.4')

# Rota para mostrar métricas no formato prometheus
@app.route('/metrics-text')
def metrics_text():
    return MetricsHandler(REGISTRY).do_GET()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
