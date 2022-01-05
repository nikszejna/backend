from .models import CommentRecord
from django.db.utils import IntegrityError
from .sentiment_analysis import get_sentiment
import json
from apiclient.discovery import build


def get_comments(videoId):
    youtube_connection = connect_to_youtube()
    comment_list = commentsearch(youtube_connection, videoId)
    for comment in comment_list:
        comment_data = CommentRecord(
            user=comment["user"],
            usercomment=comment["usercomment"],
            likecount=comment["likecount"],
            commentid=comment["commentid"],
            publishingdate=comment["publishingdate"],
            sentimentscore=get_sentiment(comment["usercomment"]),
            videoid=videoId,
        )
        try:
            comment_data.save()
        except IntegrityError as err:
            print("Skipped duplicate comment save")
        except Exception as err:
            raise (err)

    return comment_list


def connect_to_youtube():
    with open("youtube_credentials.json") as cred_data:
        info = json.load(cred_data)
        api_key = info["youtube_apikeyjson"]
    youtube = build("youtube", "v3", developerKey=api_key)
    return youtube


# This is the function used to retrieve comments for a particular video id.  We separate it so the get comments for a keyword code
# is not so long, and it can be easily modified afterwards.
def commentsearch(
    youtube, videoIdentification, partofcomment="snippet", numbrofresult=100
):
    callobject = youtube.commentThreads().list(
        part=partofcomment,
        videoId=videoIdentification,
        maxResults=numbrofresult,
        textFormat="plainText",
    )

    totallist = []

    results = callobject.execute()

    result_set_to_dict()  # this is a first call, without it, the first page will get skipped.

    if ("nextPageToken" in results) == True:
        while ("nextPageToken" in results) == True:
            callobject = youtube.commentThreads().list(
                part=partofcomment,
                videoId=videoIdentification,
                maxResults=numbrofresult,
                textFormat="plainText",
                pageToken=results["nextPageToken"],
            )
            results = callobject.execute()

            result_set_to_dict()  # this will cll result_set_to_dict()

        # print(len(totallist))

    elif ("nextPageToken" in results) == False:
        print(len(totallist))

    return totallist


def result_set_to_dict():
    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
        resultdic = {
            "user": author,
            "usercomment": comment["snippet"]["textDisplay"],
            "likecount": comment["snippet"]["likeCount"],
            "commentid": item["id"],
            "publishingdate": comment["snippet"]["publishedAt"],
        }
        totallist.append(resultdic)
