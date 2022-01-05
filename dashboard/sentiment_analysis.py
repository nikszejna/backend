import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import io
import base64
from collections import Counter
from .comment_cleaning import remove_stopwords
from .models import CommentRecord


nltk.download("vader_lexicon")


def get_top_n_words(videoId, n):
    comments = getCommentRecordsByVideoId(videoId)
    commentdf = commentRecordsToDF(comments).apply(remove_stopwords)
    comments_value_counts = pd.DataFrame(
        Counter(" ".join(commentdf).split()).most_common(n)
    )
    return comments_value_counts


def chart_top_n_words(videoId, n):
    topWords = get_top_n_words(videoId, n)
    most_common_bar_plot = topWords.loc[0 : n - 1].plot(kind="bar")
    most_common_bar_plot.set_xticklabels(topWords[0].loc[0 : n - 1], rotation=90)
    return most_common_bar_plot


def get_top_n_words_chart_as_bytes(videoId, n):
    chart = chart_top_n_words(videoId, n)
    chartBytes2 = io.BytesIO()
    plt.savefig(chartBytes2, format="png")
    chartBytes2.seek(0)
    return base64.b64encode(chartBytes2.read())


def get_sentiment(comment):
    comment_nostop = remove_stopwords(comment)
    sentiment_score = compoundSentimentScore(comment_nostop)
    return sentiment_score


def compoundSentimentScore(text):
    sentimentAnalyzer = SentimentIntensityAnalyzer()
    return sentimentAnalyzer.polarity_scores(text)["compound"]


def getSentimentLabel(sentimentValue):
    if sentimentValue > 0.05:
        return "Positive"
    elif sentimentValue < 0.05:
        return "Negative"
    else:
        return "Neutral"


def getCommentRecordsByVideoId(videoId):
    return CommentRecord.objects.filter(videoid=videoId)


def commentRecordsToDF(CommentRecords):
    return pd.DataFrame.from_records(CommentRecords.values())


def dictToDF(dict, idx=None):
    return pd.DataFrame.from_records([dict])


def get_positive_negative_count(
    videoId, negative_threshold=-0.05, positive_threshold=0.05
):
    comments_for_videoid = getCommentRecordsByVideoId(videoId)
    positive_count = CommentRecord.objects.filter(
        videoid=videoId, sentimentscore__gt=positive_threshold
    ).count()
    negative_count = CommentRecord.objects.filter(
        videoid=videoId, sentimentscore__lt=negative_threshold
    ).count()
    result = {"Positive": positive_count, "Negative": negative_count}

    return result


def get_sentiment_barchart(videoId):
    pos_neg_df_labels = dictToDF(get_positive_negative_count(videoId))
    chartTitle = "Positive VS. Negative Comments for " + videoId
    result_barchart = pos_neg_df_labels.plot.bar(
        title=chartTitle,
        color=["green", "red"],
        rot=0,
        ylabel="Comment Count",
        xlabel="Sentiment",
    )
    return result_barchart


def get_sentiment_barchart_bytes(videoId):
    chart = get_sentiment_barchart(videoId)
    chartBytes = io.BytesIO()
    plt.savefig(chartBytes, format="png")
    chartBytes.seek(0)
    my_base64_jpgData = base64.b64encode(chartBytes.read())
    return my_base64_jpgData


def get_chart_as_bytes(chart):
    chartBytes = io.BytesIO()
    plt.savefig(chartBytes, format="png")
    chartBytes.seek(0)
    my_base64_jpgData = base64.b64encode(chartBytes.read())
    return my_base64_jpgData

