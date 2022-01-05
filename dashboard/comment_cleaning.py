from nltk.corpus import stopwords

stop = stopwords.words("english")


def remove_stopwords(comment):
    if type(comment) is not str:
        comment = str(comment)
    if len(comment) > 1:
        removestop = lambda x: " ".join(
            [word for word in x.split() if word not in (stop)]
        )
        return removestop(comment)
    else:
        return comment
