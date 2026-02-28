import requests
import json

import os
from dotenv import load_dotenv
from utils import cal_time_taken_dec

load_dotenv(dotenv_path="./.env")
API_KEY = os.getenv("API_KEY")


CHANNEL_HANDLE = 'FaizYah'
maxResult = 5


url_playlist_id = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

@cal_time_taken_dec
def get_playlist_id(url):
    
    try:
        response = requests.get(url)
        
        response.raise_for_status()
        
        data = response.json()
        
        channel_items = data["items"][0]
        
        playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        
        print(f'Completed getting playlist_id of: {playlistId}')
        
        return playlistId
    
    except requests.exceptions.RequestException as e:
        raise e
        
@cal_time_taken_dec
def get_video_ids(playlistId):
    
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResult}&playlistId={playlistId}&key={API_KEY}"
    
    video_ids = []
    pageToken = None
    count = 1
    
    try:
        while True:
            url = base_url
            
            # If pageToken exist, this part will be True, so we add in the actual pageToken value
            if pageToken:
                url += f"&pageToken={pageToken}"

            # Or else the initial run will use the base url without pageToken 
            response = requests.get(url)
            
            response.raise_for_status()
            
            data = response.json()
            
            print(f"Obtained data for the {count} page")
            
            # Since the videoId output is more than once, we loop through each one and append to the main list
            # for i in range(len(data["items"])):
            #     video_id = data["items"][i]["contentDetails"]["videoId"]
            #     video_ids.append(video_id)

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            
            # Update the pageToken with current's page information to proceed to next page
            pageToken = data.get('nextPageToken')
            
            count += 1
            
            # If at the last page where there is no more pagetoken
            if not pageToken:
                break
            
        return video_ids
        
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == '__main__':
    playlistID = get_playlist_id(url_playlist_id)
    video_id_list = get_video_ids(playlistID)
    
    print(f"Total videos: {len(video_id_list)}")
    print(f"List of top 5 videos: {video_id_list[:5]}")
