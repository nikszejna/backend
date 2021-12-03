from nltk.corpus import stopwords
stop = stopwords.words('english')

def remove_stopwords(comment):
    removestop = lambda x: ' '.join([word for word in x.split() if word not in (stop)])
    return removestop(comment)
