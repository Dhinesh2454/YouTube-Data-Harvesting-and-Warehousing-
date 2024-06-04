from googleapiclient.discovery import build
import mysql.connector
import pandas as pd
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


# Function of Youtube API Connection 
def api_connect():
    api_key ="AIzaSyBxOY7kF96VNs2Jdl_QcL1RCQvp4KS16ek"
    api_server_name="youtube"
    api_version="v3"
    youtube= build(api_server_name,api_version,developerKey= api_key)
    return youtube
youtube=api_connect()
youtube
#  Streamlit Application input code 
st.title(":rainbow[ YOUTUBE DATA HARVESTING AND WAREHOUSING]")
channel_id = st.text_input("ENTER YOUR CHANNEL ID")

# Function of Connect to MySQL Database
mydb = mysql.connector.connect(host="127.0.0.1",
                                user="root",
                                password="Dhinesh@2454",
                                database="YoutubeDataBase",
                                auth_plugin="mysql_native_password")

cursor = mydb.cursor()

# Select the 10 Diffrent channel id
Channel_Ids = st.selectbox("Select a Channel Name", (
     "Open the Select Menu",
    "1.Doctor Arunkumar",
    "2.Streamlit",
    "3.Tech Classes",
    "4.Auto Kaaran",
    "5.Explore India",
))

if Channel_Ids == "1.Doctor Arunkumar":
    channel_id = "UCjZC9-Ym0UNMxqgcDX4Q0dg"
elif Channel_Ids == "2.Streamlit":
    channel_id = "UC3LD42rjj-Owtxsa6PwGU5Q"
elif Channel_Ids == "3.Tech Classes":
    channel_id = "UCPvDKIsrjA_h3g5yZJwCIHA"
elif Channel_Ids == "4.Auto Kaaran":
    channel_id = "UCOKNHJ1y3iiHjvI-FZLiT5g"
elif Channel_Ids == "5.Explore India":
    channel_id = "UCiPpjfWaWpSibmc8Y_JgSPQ"


# function of get Channel data
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

if channel_id:
      channel_details=get_channel_details(channel_id)
      df=pd.DataFrame(channel_details)

      

#function of get video_id
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
if channel_id:
    video_Ids=get_video_id(channel_id)
       
  

#Funtion get_video_information
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

if  channel_id:
    video_details=get_video_info(video_Ids)
    df2=pd.DataFrame(video_details)
     
# Function of get comment Details
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
               
if channel_id:
        comment_Details=get_comment_info(video_Ids)
        df3=pd.DataFrame(comment_Details)
    

# Funtion of get_Playlist_details

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
if channel_id:
    Playlist_Details=get_Playlist_info(channel_id)
    df1=pd.DataFrame(Playlist_Details)


# function of input query
def channel_info(channel_id):
    cha_det=get_channel_details(channel_id)
    play_inf=get_Playlist_info(channel_id)
    vi_id=get_video_id(channel_id)
    comm_info=get_comment_info( vi_id)
    vid_inf=get_video_info(vi_id)

    return "uploaded succesfully"
if channel_id:
    insert=channel_info(channel_id)
    print(insert)


#Function of channel table creation
def channel_table(df):
#Connect to MYSQL
    mydb=mysql.connector.connect(host="127.0.0.1",
                                user="root",
                                password="Dhinesh@2454",
                                database="YoutubeDataBase",
                                auth_plugin="mysql_native_password")

    cursor=mydb.cursor()

    # function of table creation query
    create_table = """CREATE TABLE IF NOT EXISTS Channels (
        channel_name VARCHAR(255) PRIMARY KEY,
        channel_id VARCHAR(255),
        subscriber INT,
        views INT,
        playlist_id VARCHAR(255),
        channel_Description TEXT,
        Total_video INT);"""

    cursor.execute(create_table)
    mydb.commit()

    # function of MSQL insert query
    if channel_id:
        values=[]
        for index ,row in df.iterrows():
            insert_query= """INSERT INTO Channels (
                                                    channel_name,
                                                    channel_id,
                                                    subscriber,
                                                    views,
                                                    playlist_id,
                                                    channel_Description,
                                                    Total_video) 
                                                    VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s)
                                                    );"""
            row_values= (
                row["channel_name"],
                row["channel_id"],
                row["subscriber"],
                row["views"],
                row["playlist_id"],
                row["channel_Description"],
                row["Total_video"]
                )
            values.append(row_values)
            
        try:
            cursor.executemany(insert_query, values)
            mydb.commit()
        except:

            Exists_channel_id= f"your given channel name {channel_id} is already Exists"
              

            return Exists_channel_id


def playlist_table():
    #Connect to MYSQL
    mydb=mysql.connector.connect(host="127.0.0.1",
                                user="root",
                                password="Dhinesh@2454",
                                database="YoutubeDataBase",
                                auth_plugin="mysql_native_password")

    cursor=mydb.cursor()
    
    # function of table create query
    create_query = """CREATE TABLE IF NOT EXISTS playlists (
        playlist_Id VARCHAR(255) PRIMARY KEY,
        channel_Id VARCHAR(255),
        Title VARCHAR(255),
        channel_Name VARCHAR(255),
        PublishedAt TIMESTAMP,
        video_count INT);"""

    cursor.execute(create_query)

    mydb.commit()

    #Function  convert to datetime string to mysql-comfortible formate 

    def convert_to_mysql_datetime(datetime_str):
        datetime_obj=datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
        mysql_datetime=datetime.strftime(datetime_obj,"%Y-%m-%d %H:%M:%S")

        return mysql_datetime

    #insert data into playlist table
    values=[]
    for index ,row in df1.iterrows():
        insert_query=("""INSERT INTO playlists( playlist_Id,
                                            channel_Id,
                                            Title ,
                                            channel_Name,
                                            PublishedAt,
                                            video_count) 
                                            VALUES (%s ,%s ,%s ,%s ,%s ,%s) 
                                            ON DUPLICATE KEY UPDATE
                                            playlist_Id=VALUES(playlist_Id) ;""")
        row_values=(
                row["playlist_Id"],
                row["channel_Id"],
                row["Title"],
                row["channel_Name"],
                convert_to_mysql_datetime(row["PublishedAt"]),
                row["video_count"]
                )
        values.append(row_values)
        
    try:
        cursor.executemany(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        print("Error:", err)

    return "channel table created succesfully"



# function to call all extracted videos data insert to my sql database
def videos_table():
    #Connect to MYSQL
    mydb=mysql.connector.connect(host="127.0.0.1",
                                user="root",
                                password="Dhinesh@2454",
                                database="YoutubeDataBase",
                                auth_plugin="mysql_native_password")

    cursor=mydb.cursor()

    #function of table create query
    create_query = """CREATE TABLE IF NOT EXISTS videos (
        channel_name VARCHAR(255),
        Video_Id VARCHAR(255) PRIMARY KEY,
        channel_id VARCHAR(255),
        Title VARCHAR(255),
        Description TEXT,
        Thumbnail VARCHAR(255),
        Tags TEXT,
        Published_date TIMESTAMP,
        Duration TIME,
        Views INT,
        Likes INT,
        Comments INT,
        Favorite_Count INT,
        Definition VARCHAR(250),
        Caption_status VARCHAR(250)
    );"""
    cursor.execute(create_query)
    mydb.commit()
    def convert_to_mysql_datetime(datetime_str):
            datetime_obj=datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
            mysql_datetime=datetime.strftime(datetime_obj,"%Y-%m-%d %H:%M:%S")

            return mysql_datetime
    def list_to_string(tags_str):
        if isinstance(tags_str, list):
            return ",".join(tags_str)
        else:
            return str(tags_str)

    def convert_duration_to_mysql(duration_str):
        duration_str=duration_str[2:]
        seconds=0
        if "H" in duration_str:
            hours,duration_str=duration_str.split("H")
            seconds+=int(hours)*3600
        if "M" in duration_str:
            minute,duration_str=duration_str.split("M")
            seconds+=int(minute)*60
        if "S" in duration_str:
            seconds+=int(duration_str[:-1])
        formatted_duration="{:02d}:{:02d}:{:02d}".format(seconds // 3600,seconds % 3600 // 60,seconds % 60)
        return formatted_duration
        

    values=[]
    for index,row in df2.iterrows():
        insert_query = """INSERT INTO videos (
                                            channel_name,
                                            Video_Id,
                                            channel_id,
                                            Title,
                                            Description,
                                            Thumbnail,
                                            Tags,
                                            Published_date,
                                            Duration,
                                            Views,
                                            Likes,
                                            Comments,
                                            Favorite_Count,
                                            Definition,
                                            Caption_status)

                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
                                            ON DUPLICATE KEY UPDATE
                                            Video_Id = VALUES(Video_Id);"""
        row_values=(row["channel_name"],row["Video_Id"],row["channel_id"],
                    row["Title"],row["Description"],
                    row["Thumbnail"],list_to_string(row["Tags"]),convert_to_mysql_datetime(row["Published_date"]),
                    convert_duration_to_mysql(row["Duration"]),row["Views"],row["Likes"],
                    row["Comments"],row["Favorite_Count"],
                    row["Definition"],row["Caption_status"]
                    )
        values.append(row_values)
    try:
        cursor.executemany(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        print("Error:", err)

    return "video table created succesfully"



def comments_table():
        #Connect to MYSQL
        mydb=mysql.connector.connect(host="127.0.0.1",
                                user="root",
                                password="Dhinesh@2454",
                                database="YoutubeDataBase",
                                auth_plugin="mysql_native_password")

        cursor=mydb.cursor()
       
        # function of table create query
        create_query = """CREATE TABLE IF NOT EXISTS comments (
        comment_id VARCHAR(255) ,
        Video_Id VARCHAR(255),
        comment_Text TEXT,
        comment_author VARCHAR(255),
        comment_PublishedAt TIMESTAMP

        );"""
        cursor.execute(create_query)
        mydb.commit()
        def convert_to_mysql_datetime(datetime_str):
                datetime_obj=datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
                mysql_datetime=datetime.strftime(datetime_obj,"%Y-%m-%d %H:%M:%S")

                return mysql_datetime

        values=[]
        for index,row in df3.iterrows():
                insert_query="""INSERT INTO comments ( 
                                                comment_id,
                                                Video_Id ,
                                                comment_Text,
                                                comment_author,
                                                comment_PublishedAt)
                                                
                                                VALUES (%s, %s, %s, %s, %s)
                                                ON DUPLICATE KEY UPDATE
                                                comment_Text = VALUES(comment_Text),
                                                comment_author = VALUES(comment_author),
                                                comment_PublishedAt = VALUES(comment_PublishedAt);"""
                row_values=(row["comment_id"],
                row["Video_Id"],
                row["comment_Text"],
                row["comment_author"],
                convert_to_mysql_datetime(row["comment_PublishedAt"]))

                values.append(row_values)

        try:
                cursor.executemany(insert_query, values)
                mydb.commit()
        except mysql.connector.Error as err:
                print("Error:", err)

        return "video table created succesfully"



def tables():
    Exists_channel_id=channel_table(df)
    if Exists_channel_id:
          return Exists_channel_id
    else:
        playlist_table()
        videos_table()
        comments_table()
    return print("Tables created successfully")
if channel_id:
    All_Tables=tables()

#Connect to MYSQL
mydb=mysql.connector.connect(host="127.0.0.1",
                        user="root",
                        password="Dhinesh@2454",
                        database="YoutubeDataBase",
                        auth_plugin="mysql_native_password")

cursor=mydb.cursor()

question=st.selectbox("Select a Query",(
                                        "Open the Select Menu",
                                        "1. Names of the all videos and corresponding Channels",
                                        "2.Which channels have the most number of videos, and how many videos do they have?",
                                        "3.What are the top 10 most viewed videos and their respective channels?",
                                        "4.How many comments were made on each video, and what are their corresponding video names?",
                                        "5.Which videos have the highest number of likes, and what are their corresponding channel names?",
                                        "6.What is the total number of likes for each video, and what are their corresponding video names",
                                        "7.What is the total number of views for each channel, and what are their corresponding channel names?",
                                        "8.What are the names of all the channels that have published videos in the year2022?",
                                        "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                                        "10.Which videos have the highest number of comments, and what are their corresponding channel names?",
                                        "11.Retrieve all stored channel information from the database"
                                        ))

# SQL Query Output - 1
if  question=="1. Names of the all videos and corresponding Channels":
    question1="""SELECT Title , channel_name  FROM videos"""
    cursor.execute(question1)
    q1=cursor.fetchall()
    mydb.commit()
    convert_df=pd.DataFrame(q1,columns=["video title","channel name"])
    st.write(convert_df)

# SQL Query Output-2
elif    question=="2.Which channels have the most number of videos, and how many videos do they have?":
        question2="""SELECT channel_name,Total_video FROM channels ORDER BY Total_video DESC """
        cursor.execute(question2)
        q2=cursor.fetchall()
        mydb.commit()
        convert_df2=pd.DataFrame(q2,columns=["Channel Name","Max Videos"])
        st.write(convert_df2)
        fig, ax = plt.subplots(figsize=(8, 6))  
        convert_df2.plot(kind='bar', x="Channel Name", y="Max Videos", color='skyblue', ax=ax,width=0.4)  
        ax.set_xlabel("channel name")  
        ax.set_ylabel("Max Videos")  
        ax.set_title("channels have the most number of videos")  
        st.pyplot(fig) 

# SQL Query Output-3
elif    question=="3.What are the top 10 most viewed videos and their respective channels?":
        question3="""SELECT channel_name as channelName,Title as videoTitle,Views as totalViews FROM videos ORDER BY Views DESC LIMIT 10"""
        cursor.execute(question3)
        q3=cursor.fetchall()
        mydb.commit()
        convert_df3 = pd.DataFrame(q3, columns=["channel name", "video title", "total views"])
        st.write(convert_df3) 
        fig, ax = plt.subplots(figsize=(8, 6))  # Explicitly create a figure and axis
        convert_df3.plot(kind='bar', x="channel name", y='total views', color='skyblue', ax=ax,width=0.4)  # Pass the axis to plot
        ax.set_xlabel("channel name")  # Set x-axis label
        ax.set_ylabel("Total Views")  # Set y-axis label
        ax.set_title("Top 10 Most Viewed Videos")  # Set plot title
        st.pyplot(fig)  

# SQL Query Output-4
elif    question=="4.How many comments were made on each video, and what are their corresponding video names?":
        question4="""SELECT Title as videotitle,Comments as totalcomment FROM videos ORDER BY Comments DESC"""
        cursor.execute(question4)
        q4=cursor.fetchall()
        mydb.commit()
        convert_df4=pd.DataFrame(q4,columns=["Videos Name","Total Comments"])
        st.write(convert_df4)
       
# SQL Query Output-5
elif    question=="5.Which videos have the highest number of likes, and what are their corresponding channel names?":
        question5="""SELECT channel_name as channelname,Title as videotitle, MAX(Likes) as likes 
                FROM videos 
                GROUP BY channel_name,Title 
                ORDER BY likes DESC LIMIT 10 """
        cursor.execute(question5)
        q5=cursor.fetchall()
        mydb.commit()
        convert_df5=pd.DataFrame(q5,columns=["channel name","Videos Title","Highest Likes"])
        st.write(convert_df5)
        fig, ax = plt.subplots(figsize=(8, 6))
        convert_df5.plot(kind='bar', x="channel name", y="Highest Likes", color='skyblue', ax=ax, width=0.4)  
        ax.set_xlabel("Videos Title")  
        ax.set_ylabel("Highest Likes")  
        ax.set_title("Top 10 Most Liked Videos")
        st.pyplot(fig)
# SQL Query Output-6
elif    question=="6.What is the total number of likes for each video, and what are their corresponding video names":
        question6="""SELECT Title as videotitle, SUM(Likes) as likes FROM videos GROUP BY Title ORDER BY likes DESC """
        cursor.execute(question6)
        q6=cursor.fetchall()
        mydb.commit()
        convert_df6=pd.DataFrame(q6,columns=["Videos Name","Total number of Likes"])
        st.write(convert_df6)

         
# SQL Query Output-7
elif    question=="7.What is the total number of views for each channel, and what are their corresponding channel names?":
        question7="""SELECT channel_name as channelname, Views as total_views FROM channels GROUP BY channel_name ORDER BY Views DESC """
        cursor.execute(question7)
        q7=cursor.fetchall()
        mydb.commit()
        convert_df7=pd.DataFrame(q7,columns=["channel name","Total number of views"])
        st.write(convert_df7)


# SQL Query Output-8     
elif    question=="8.What are the names of all the channels that have published videos in the year2022?":
        question7="""SELECT channel_name as channelname,Title as videotitle, Published_date as Published FROM videos WHERE YEAR(Published_date)=2022 """
        cursor.execute(question7)
        q7=cursor.fetchall()
        mydb.commit()
        convert_df7=pd.DataFrame(q7,columns=["channel name","videotitle","Published date"])
        st.write(convert_df7)

# SQL Query Output-9
elif    question=="9.What is the average duration of all videos in each channel, and what are their corresponding channel names?":
        question9="""SELECT channel_name as channelname,Title as videotitle,AVG(Duration) as average_duration
                FROM videos 
                GROUP BY channel_name,Title """
        cursor.execute(question9)
        q9=cursor.fetchall()
        mydb.commit()
        convert_df9=pd.DataFrame(q9,columns=["channel name","videotitle","Average Duration"])
        st.write(convert_df9)

# SQL Query Output-10
elif    question=="10.Which videos have the highest number of comments, and what are their corresponding channel names?":
        question10="""SELECT channel_name as channelname,Title as videotitle,MAX(Comments) as max_comments
                FROM videos 
                GROUP BY channel_name,Title
                ORDER BY max_comments DESC """
        cursor.execute(question10)
        q10=cursor.fetchall()
        mydb.commit()
        convert_df10=pd.DataFrame(q10,columns=["channel name","videotitle","Max comment"])
        st.write(convert_df10)

# SQL Query Output-10
elif question == "11.Retrieve all stored channel information from the database":
    question11 = """SELECT channel_name as channelname, subscriber as subscr, views as view, Total_video as totalvideo 
                    FROM channels
                    ORDER BY view DESC """   
    cursor.execute(question11)
    q11 = cursor.fetchall()
    mydb.commit()
    convert_df11 = pd.DataFrame(q11, columns=["channel name", "Subscriber", "Total_Views", "Total videos"])
    st.write(convert_df11) 
    fig, ax = plt.subplots(figsize=(8, 6))
    bar_width = 0.1   
    xpos = np.arange(len(convert_df11))  # Convert range object to a numpy array

    # Plotting each bar for different columns
    ax.bar(xpos + 0.2, convert_df11['Subscriber'], width=bar_width, label='Subscribers', align='center')
    ax.bar(xpos + 0.4, convert_df11['Total_Views'], width=bar_width, label='Total_Views', align='center')
    ax.bar(xpos + 0.6, convert_df11['Total videos'], width=bar_width, label='Total Videos', align='center')
    # Setting labels and title
    ax.set_xlabel('Channel Name')
    ax.set_ylabel('Counts')
    ax.set_title('Channels Information')
    ax.set_xticks([r + bar_width for r in range(len(convert_df11))])
    ax.set_xticklabels(convert_df11['channel name'], rotation=90)
    ax.legend()
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    st.pyplot(fig)  # Display the plot in Streamlit

  
       


      

