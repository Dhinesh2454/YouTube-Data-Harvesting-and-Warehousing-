# YouTube-Data-Harvesting-and-Warehousing-
YouTube Data Harvesting and Warehousing is a project designed to collect,  store, and analyze data from YouTube using the YouTube Data API.  The collected data includes channel details, video information, playlist details, and comments,  which are stored in a MySQL database for future analysis. A user-friendly Streamlitdashboard is provided to interact with the data, allowing users to input channel IDs and query the database for insights
# YouTube Data Harvesting and Warehousing using SQL and Streamlit
This project allows users to collect data from YouTube using the YouTube Data API, store it in a MySQL database, and analyze it through a user-friendly Streamlit dashboard. It offers various functionalities for querying and analyzing the collected data.
# Installation
To install the necessary dependencies for this project, follow these steps:
1.	Clone this repository to your local machine.
2.	git clone https://github.com/your_username/your_repository.git
3.	Navigate to the project directory.
    cd youtube-data-project
4.	Install the required Python packages using pip.
pip install -r requirements.txt

# Set up MySQL Database
Before running the project, you need to set up a MySQL database. Follow these steps:
1.	Install MySQL Server on your machine if you haven't already.
2.	Create a new MySQL database for this project.
3.	Update the config.py file with your MySQL database credentials.
	
# Obtain YouTube Data API Key
To fetch data from YouTube, you need to obtain an API key. Follow these steps:
1.	Go to the Google Cloud Console.
2.	Create a new project (if you haven't already).
3.	Enable the YouTube Data API v3 for your project.
4.	Create credentials for the API and obtain your API key.
5.	Update the config.py file with your YouTube Data API key.
# Usage
After completing the installation and setting up the MySQL database and API key, you can run the project by executing the main Python script.
                    Python youtube.py
This will start the Streamlit server, and you can access the dashboard in your web browser.
# Features
# Data Collection:
•	Functions: Several Python functions are implemented to collect various types of data from YouTube, such as channel          details, video IDs, video information, comments, and playlist information.
•	Get channel detail: retrieves details about a youtube  channel.
•	Get video ids: fetches the ids of all videos uploaded to a specified channel.
•	Get video information: collects information about each video.
•	Get comment information: retrieves details of comments made on each video.
•	Get playlist information: gathers information about playlists associated with a given channel.
# Mysql database 
•	Purpose: Stores the collected data from YouTube for future analysis and querying.
•	Integration: Utilizes MySQL as the database management system to store structured data efficiently.
•	Configuration: Users need to set up a MySQL database and update the config.py file with the database credentials.
# Data Analysis
•	Queries: Provides various SQL queries to analyze the stored data, such as finding the most viewed videos, channels with     the highest number of videos, average video duration per channel and more.
•	Visualization: Uses interactive visualizations like bar charts to display query results, enhancing data understanding  for users.
# Dependencies
•	Python Packages: Required Python packages are installed using pip, including Pandas for data manipulation, Google API Client Library for interacting with YouTube Data API, MySQL Connector for communication with MySQL database, Streamlit for building the dashboard, and Matplotlib for creating visualizations.

# Overview
The project comprises several Python  functions, each serving a specific purpose:

# Get  Channnel  Detail

This function retrieves details about a YouTube channel, including its name, ID, subscriber count, view count, playlist ID, description, and total video count.
	def get_channel_details(channel_id):
	    response=youtube.channels().list(
	    id=channel_id,
	    part="snippet,statistics,contentDetails")
	    
	    channel_data=response.execute()
	    channel_details=[]
	    
	    for i in channel_data["items"]:
	    data=dict(channel_name=i["snippet"]["title"],
	    channel_id=i["id"],
	    subscriber=i["statistics"]["subscriberCount"],
	    views = i ["statistics"] ["viewCount"],
	    playlist_id=i["contentDetails"]["relatedPlaylists"]["uploads"],
	    channel_Description=i["snippet"]["description"],
	    Total_video=i["statistics"]["videoCount"])
	    channel_details.append(data)
	    return channel_details

# Get Video Ids

This function fetches the Ids of all videos uploaded to a specified channel.
	def get_video_id(channel_id):
	    videos_ids=[]
	    response=youtube.channels().list(
	    id=channel_id,
	    part="contentDetails").execute()
	    playlist_id=response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
	    
	    next_page_token = None
	    while True:
	    request=youtube.playlistItems().list(part="snippet",
	    playlistId=playlist_id,
	    maxResults=50,
	    pageToken=next_page_token).execute()
	    for i in range(len(request["items"])):
	    videos_ids.append(request["items"][i]["snippet"][ 'resourceId']['videoId'])
	    next_page_token=request.get("nextPageToken")
	    
	    if next_page_token is None:
	    break
	    return videos_ids

# Get Video Information

Given a list of video IDs, this function collects information about each video, such as its title, description, thumbnail URL, tags, publication date, duration, views, likes, comments, favorite count, definition, and caption status.

def get_video_info(video_Ids):
    video_data=[]
    
    for video_id in video_Ids:
    request=youtube.videos().list(
    part="snippet,contentDetails,statistics",
    id=video_id
    )
    response=request.execute()
    
    for item in response["items"]:
    data=dict(channel_name=item["snippet"][ 'channelTitle'],
    channel_id=item['snippet'][ 'channelId'],
    Video_Id=item["id"],
    Title = item["snippet"]["title"],
    Description=item["snippet"].get('description'),
    Thumbnail=item['snippet']['thumbnails']['default']['url'],
    Tags=item["snippet"].get("tags"),
    Published_date=item[ 'snippet']['publishedAt'],
    Duration=item['contentDetails']['duration'],
    Views=item['statistics'].get('viewCount'),
    Likes=item['statistics'].get('likeCount'),
    Comments=item['statistics'].get('commentCount'),
    Favorite_Count=item['statistics']['favoriteCount'],
    Definition=item[ 'contentDetails'][ 'definition'],
    Caption_status=item["contentDetails"]["caption"]
    
    
    )
    video_data.append(data)
    return video_data
    
# Get Comment Information

For a list of video IDs, this function retrieves details of comments made on each video, including comment ID, video ID, comment text, author name, and publication date.

def get_comment_info(video_Ids):
    comment_info=[]
    try:
    for video_id in video_Ids:
    comment_request=youtube.commentThreads().list(
    part="snippet",
    videoId= video_id,
    maxResults=100
    )
    comment_response=comment_request.execute()
    
    for item in comment_response["items"]:
    comment_data=dict(comment_id=item['snippet']['topLevelComment'][ 'id'],
    Video_Id=item['snippet']['topLevelComment'][ 'snippet']['videoId'],
    comment_Text=item['snippet']['topLevelComment'][ 'snippet'][ 'textDisplay'],
    comment_author=item['snippet']['topLevelComment'][ 'snippet']['authorDisplayName'],
    comment_PublishedAt=item[ 'snippet'][ 'topLevelComment'][ 'snippet']['publishedAt']
    )
    comment_info.append(comment_data)
    except:
    pass
    return comment_info

# Get Playlist Information

This function gathers information about playlists associated with a given channel, including playlist ID, channel ID, title, channel name, publication date, and video count.

def get_Playlist_info(channel_id):
    playlist_data=[]
    
    next_page_Token= None
    request=youtube.playlists().list(
    part='snippet,contentDetails',
    channelId=channel_id,
    maxResults=50,
    pageToken=next_page_Token
    
    )
    while True:
    response=request.execute()
    
    for item in response["items"]:
    data=dict(playlist_Id=item["id"],
    channel_Id=item['snippet']['channelId'],
    Title=item['snippet'][ 'title'],
    channel_Name=item[ 'snippet']['channelTitle'],
    PublishedAt=item['snippet']['publishedAt'],
    video_count=item[ 'contentDetails']['itemCount'])
    playlist_data.append(data)
    next_page_Token=response.get("nextPageToken")
    
    if next_page_Token is None:
    break
    return playlist_data
    
# Technologies Used
•	Python: Programming language used for scripting.
•	Google API Client Library: Enables interaction with the YouTube Data API.
•	MySQL Connector: Facilitates communication between Python and MySQL database.
•	Pandas: Used for data manipulation and analysis.
•	Streamlit: Framework used to build the interactive dashboard.
•	Matplotlib: Library for creating visualizations in Python.



