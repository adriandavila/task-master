from googleapiclient.discovery import build
import json

api_key = "AIzaSyBhZXakezVrniHq4yte0THZiMOmoOL3KuE" #Key was put in this file for simplicity, best practice would be to put it elsewhere

youtube = build('youtube', 'v3', developerKey=api_key)

def get_video(keywords):
    request = youtube.search().list(
        part='snippet',
        type='video',
        q=keywords
    )
    
    response = request.execute()

    videoId = response["items"][0]["id"]["videoId"]
    videoUrl = "https://www.youtube.com/watch?v="+videoId
    thumbnail = response["items"][0]["snippet"]["thumbnails"]["default"]["url"] #width 120 height 90

    return videoUrl, thumbnail


youtube.close()