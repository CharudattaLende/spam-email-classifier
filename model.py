import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

# ---------------------------------------------------------------------------
# Module-level globals — trained once when this module is first imported
# ---------------------------------------------------------------------------
_vectorizer = None
_model = None


def _train():
    """Download dataset, train the model, and store in module globals."""
    global _vectorizer, _model

    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_csv(url, sep="\t", names=["label", "message"])

    # Encode labels: ham → 0, spam → 1
    df["label"] = df["label"].map({"ham": 0, "spam": 1})

    _vectorizer = CountVectorizer()
    X = _vectorizer.fit_transform(df["message"])
    y = df["label"]

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    _model = MultinomialNB()
    _model.fit(X_train, y_train)


def predict_email(text: str) -> str:
    """
    Predict whether an email/message is spam or not.

    Parameters
    ----------
    text : str
        The raw message text to classify.

    Returns
    -------
    str
        "Spam" if the message is classified as spam, "Not Spam" otherwise.
    """
    if _model is None or _vectorizer is None:
        _train()

    vec = _vectorizer.transform([text])
    prediction = _model.predict(vec)
    return "Spam" if prediction[0] == 1 else "Not Spam"


# Train immediately on import so the first prediction is fast
_train()