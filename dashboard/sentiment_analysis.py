import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import io
import base64
from .comment_cleaning import remove_stopwords
from .models import CommentRecord


nltk.download('vader_lexicon')

def get_sentiment(comment):
    comment_nostop = remove_stopwords(comment)
    sentiment_score = compoundSentimentScore(comment_nostop)
    return sentiment_score

def compoundSentimentScore(text):
    sentimentAnalyzer = SentimentIntensityAnalyzer()
    return sentimentAnalyzer.polarity_scores(text)['compound']

def getSentimentLabel(sentimentValue):
    if(sentimentValue > 0.05):
        return "Positive"
    elif(sentimentValue < 0.05):
        return "Negative"
    else:
        return "Neutral"

    
def getCommentRecordsByVideoId(videoId):
    return CommentRecord.objects.filter(videoid=videoId)

def commentRecordsToDF(CommentRecords):
    return pd.DataFrame.from_records(CommentRecords.values())

def dictToDF(dict):
    return pd.DataFrame.from_records([dict])


def get_positive_negative_count(videoId,negative_threshold = -.05 ,positive_threshold = .05):
    comments_for_videoid = getCommentRecordsByVideoId(videoId)
    print(videoId)
    print(CommentRecord.objects.filter(videoid=videoId).count())
    positive_count = CommentRecord.objects.filter(videoid=videoId, sentimentscore__gt=positive_threshold).count()
    negative_count = CommentRecord.objects.filter(videoid=videoId,sentimentscore__lt=negative_threshold).count()
    print(positive_count,negative_count)
    result = {
        'Positive' : positive_count,
        'Negative' : negative_count
    }

    return result

def get_sentiment_barchart(videoId):
    pos_neg_df_labels = dictToDF(get_positive_negative_count(videoId))
    print(pos_neg_df_labels)
    chartTitle = 'Positive VS. Negative Comments for ' + videoId
    result_barchart = pos_neg_df_labels.plot.bar(
        title=chartTitle,
        color=['green','red'],
        rot=0,
        ylabel="Comment Count"
    )
    return result_barchart

def get_sentiment_barchart_bytes(videoId):
    chart = get_sentiment_barchart(videoId)
    chartBytes = io.BytesIO()
    plt.savefig(chartBytes,format='png')
    chartBytes.seek(0)
    my_base64_jpgData = base64.b64encode(chartBytes.read())
    return my_base64_jpgData
        