from googleapiclient.discovery import build

# Replace this with your own API key
YOUTUBE_API_KEY = 'your_youtube_api_key'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def search_youtube(query, max_results=5):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)

    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=max_results
    )

    response = request.execute()

    for item in response['items']:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"{title}: {url}")

# Example usage
if __name__ == "__main__":
    search_youtube("smart healthcare IoT")
