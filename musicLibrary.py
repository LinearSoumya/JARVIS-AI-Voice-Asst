# musicLibrary.py
import requests

YOUTUBE_API_KEY = "AIzaSyAlyYMac-VMmNdqQUwE_vGyF1lJz7QPSmg"

def get_youtube_link(song_name):
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={song_name}&type=video&key={YOUTUBE_API_KEY}"
    response = requests.get(search_url)
    data = response.json()

    if "items" in data and len(data["items"]) > 0:
        video_id = data["items"][0]["id"]["videoId"]
        youtube_link = f"https://www.youtube.com/watch?v={video_id}"
        return youtube_link
    else:
        return None
