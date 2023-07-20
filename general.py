#AIzaSyDl4xdPFbXYvjk5Ck32YOMrK1al4l_59Qg
from googleapiclient.discovery import build
from pytube import YouTube
import os

# Замените "YOUR_API_KEY" на ваш собственный API ключ
API_KEY = "AIzaSyDl4xdPFbXYvjk5Ck32YOMrK1al4l_59Qg"


youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_music(query):
    try:
        # Выполняем поиск видео по запросу
        search_response = youtube.search().list(
            q=query,
            type='video',
            part='id, snippet',
            maxResults=1
        ).execute()

        # Получаем первое найденное видео
        if 'items' in search_response and len(search_response['items']) > 0:
            video_id = search_response['items'][0]['id']['videoId']
            video_title = search_response['items'][0]['snippet']['title']
            return video_id, video_title
        else:
            return None, None
    except KeyError as e:
        print("Ошибка при поиске видео:", e)
        return None, None
    except Exception as e:
        print("Неизвестная ошибка:", e)
        return None, None

def download_video(video_id):
    try:
        link = f"https://youtu.be/{video_id}"
        youtube_object = YouTube(link)
        youtube_stream = youtube_object.streams.get_highest_resolution()
        youtube_stream.download()
        print("Загрузка успешно завершена.")
        
        # Конвертирование видео в mp3
        video_file = youtube_object.title + ".mp4"
        audio_file = youtube_object.title + ".mp3"
        os.rename(video_file, audio_file)
    
        print("Конвертация в mp3 и удаление оригинального файла завершены.")
    except Exception as e:
        print("Ошибка при загрузке видео:", e)

def main():
    query = input("Введите название песни: ")
    video_id, video_title = search_music(query)

    if video_id and video_title:
        print(f"Найдено видео: {video_title}")
        download_video(video_id)
    else:
        print("Песня не найдена.")

if __name__ == "__main__":
    main()