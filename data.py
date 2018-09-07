class Data:

    Id = ""
    Desc = []

    def __init__(self, id, desc):
        self.Id = id
        self.Desc = desc

class TextDesc:

    Term = ""
    TF = ""
    DF = ""
    TFIDF = ""

    def __init__(self, term, tf, df, tfidf):
        self.Term = term
        self.TF = tf
        self.DF = df
        self.TFIDF = tfidf