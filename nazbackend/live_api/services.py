from googleapiclient.discovery import build
import pandas as pd
import requests
from bs4 import BeautifulSoup

#SETUP
API_KEY = "AIzaSyC1WItkrEre7bROgCRHw_rohVKwe8WHogk"
channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"
youtube = build("youtube","v3", developerKey = API_KEY)

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def name2channelID(youtube):
    names={}
    client_secrets_file = "client_secret.json"
    request = youtube.search().list(
        part="snippet",
        q="stormy shows",
        maxResults=30,
        type="channel"
    )
    response = request.execute()

    for i in range(30):
        key = response['items'][i]['snippet']['title']
        value = response['items'][i]['id']['channelId']
        names[key]=value
    print(names)
#gets basic channel statistics
def get_channel_stats(youtube, channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id = channel_id
    )
    response = request.execute()
    return response['items']

#gets all the video ids a channel has uploaded
def get_vids(youtube, uploads):
    vids = []
    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=uploads,
        maxResults=50
    )
    next = True
    while next:
        response = request.execute()
        data_items = response['items']
        for video in data_items:
            video_id = video['contentDetails']['videoId']
            if video_id not in vids:
                vids.append(video_id)

        if 'nextPageToken' in response.keys():
            next = True
            request = youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=uploads,
                maxResults=50
            )
        else:
            next= False
    return vids

#get video details of each video id
def get_vid_details(youtube, vids):
    stats_list=[]

    # Can only get 50 videos at a time.
    for i in range(0, len(vids), 50):
        request= youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=vids[i:i+50]
        )

        data = request.execute()
        for video in data['items']:
            title=video['snippet']['title']
            published=video['snippet']['publishedAt']
            description=video['snippet']['description']
            tag_count= len(video['snippet']['tags'])
            view_count=video['statistics'].get('viewCount',0)
            like_count=video['statistics'].get('likeCount',0)
            dislike_count=video['statistics'].get('dislikeCount',0)
            comment_count=video['statistics'].get('commentCount',0)
            stats_dict=dict(title=title, description=description, published=published, tag_count=tag_count, view_count=view_count, like_count=like_count, dislike_count=dislike_count, comment_count=comment_count)
            stats_list.append(stats_dict)

    return stats_list

def run(youtube):
    # channel_stats = get_channel_stats(youtube, channel_id)
    # upload_id = channel_stats[0]['contentDetails']['relatedPlaylists']['uploads']
    # video_list = get_vids(youtube, upload_id)
    # video_data = get_vid_details(youtube, video_list)

def scrape_wiki():
    likes_wikiurl = "https://en.wikipedia.org/wiki/List_of_most-liked_YouTube_videos"
    table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(likes_wikiurl)

    soup = BeautifulSoup(response.text, 'html.parser')
    likes_table = soup.find('table', {'class': "wikitable"})
    # print(str(table))
    df = pd.read_html(str(likes_table))

    df = pd.DataFrame(df[0])
    # print(df)
    likes_data = df.drop(["Notes", "Upload date"], axis=1)
    print(likes_data.to_string())
    likes_data.to_csv("most_likes.csv")

    subs_wikiurl = "https://en.wikipedia.org/wiki/List_of_most-subscribed_YouTube_channels"
    subs_table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(subs_wikiurl)

    soup = BeautifulSoup(response.text, 'html.parser')
    subs_table = soup.find('table', {'class': "wikitable"})
    # print(subs_table)
    sdf = pd.read_html(str(subs_table))

    sdf = pd.DataFrame(sdf[0])
    # print(sdf)
    print(list(sdf))
    subs_data = sdf.drop(["Primarylanguage(s)", "Contentcategory[6]"], axis=1)
    print(subs_data.to_string())
    subs_data.to_csv("most_subs.csv")

    dislikes_wikiurl = "https://en.wikipedia.org/wiki/List_of_most-disliked_YouTube_videos"
    table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(dislikes_wikiurl)

    soup = BeautifulSoup(response.text, 'html.parser')
    dislikes_table = soup.find('table', {'class': "wikitable"})
    # print(str(table))
    df = pd.read_html(str(dislikes_table))

    df = pd.DataFrame(df[0])
    # print(df)
    dislikes_data = df.drop(["Notes", "Upload date"], axis=1)
    print(dislikes_data.to_string())
    dislikes_data.to_csv("most_dislikes.csv")

    views_wikiurl = "https://en.wikipedia.org/wiki/List_of_most-viewed_YouTube_channels"
    table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(views_wikiurl)

    soup = BeautifulSoup(response.text, 'html.parser')
    views_table = soup.find('table', {'class': "wikitable"})
    # print(str(table))
    df = pd.read_html(str(views_table))

    df = pd.DataFrame(df[0])
    # print(df)
    # views_data = df.drop(["Notes", "Upload date"], axis=1)
    print(df.to_string())
    df.to_csv("most_views.csv")

    comments_url = "https://youtube.fandom.com/wiki/Most-Commented_YouTube_Videos"
    table_class = "article-table liked-paragraph"
    response = requests.get(comments_url)

    soup = BeautifulSoup(response.text, 'html.parser')
    comment_table = soup.find('table', {'class': "article-table"})
    # print(str(table))
    df = pd.read_html(str(comment_table))

    df = pd.DataFrame(df[0])
    # views_data = df.drop(["Notes", "Upload date"], axis=1)
    print(df.to_string())
    df.to_csv("most_comment.csv")