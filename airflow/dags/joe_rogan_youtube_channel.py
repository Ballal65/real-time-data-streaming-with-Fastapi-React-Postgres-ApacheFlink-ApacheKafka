from datetime import datetime, timedelta
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from googleapiclient.discovery import build
import csv
import isodate  # To parse ISO 8601 duration format

# Define the timezone
local_tz = pendulum.timezone("Asia/Kolkata")

def extract_guest_name(title):
    # Example logic for extracting guest name from title
    if '-' in title:
        return title.split('-')[-1].strip()
    return None

def fetch_video_details(youtube, video_ids):
    video_details = []
    video_request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=','.join(video_ids)
    )
    video_response = video_request.execute()
    
    for item in video_response['items']:
        details = {
            "Title": item['snippet']['title'],
            "Publish Date": item['snippet']['publishedAt'],
            "Duration": isodate.parse_duration(item['contentDetails']['duration']).total_seconds(),
            "Tags": item['snippet'].get('tags', []),
            "Category": item['snippet']['categoryId'],
            "Guest Name": extract_guest_name(item['snippet']['title']),
            "View Counts": int(item['statistics'].get('viewCount', 0)),
            "Like Counts": int(item['statistics'].get('likeCount', 0)),
            "Count Date": item['snippet']['publishedAt']
        }
        video_details.append(details)
    
    return video_details

def fetch_channel_videos(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    videos = []
    next_page_token = None

    # Get the uploads playlist ID
    channel_request = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    )
    channel_response = channel_request.execute()
    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    # Fetch videos from the uploads playlist
    while True:
        playlist_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()
        
        # Collect video IDs for further details
        video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_response['items']]
        videos.extend(fetch_video_details(youtube, video_ids))
        
        # Check if there are more pages
        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break

    return videos

import os

def save_to_csv(videos):
    keys = videos[0].keys()
    now = datetime.now(local_tz)
    today = now.strftime('%Y-%m-%d')
    directory = "/opt/airflow/extracted_data/youtube_data/"
    CSV_FILE = os.path.join(directory, f"jre_data_{today}.csv")
    
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Always overwrite the file for the day
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(videos)
    print(f"Data saved successfully to {CSV_FILE}")


def extract_jre_data():
    api_key = 'AIzaSyBqen81byB-vM9tDuUpBG3u9XHmSK4DlCs'
    channel_id = 'UCzQUP1qoWDoEbmsQxvdjxgQ'
    videos = fetch_channel_videos(api_key, channel_id)
    if videos:
        save_to_csv(videos)
        print(f"Saved {len(videos)} videos to CSV.")

# Define the DAG
default_args = {
    'owner': 'Ballal',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 4,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'joe_rogan_youtube_data',
    default_args=default_args,
    description='Fetch and save Joe Rogan Experience YouTube channel data daily at 11 PM',
    schedule_interval='0 23 * * *',  # Run daily at 11:00 PM
    start_date=pendulum.datetime(2025, 1, 6, tz="Asia/Kolkata"),
    catchup=False,
)

extract_task = PythonOperator(
    task_id='extract_jre_data',
    python_callable=extract_jre_data,
    dag=dag
)

# Set task dependencies
extract_task