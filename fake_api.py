# fake_api.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, request, jsonify

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")
    score = analyzer.polarity_scores(text)
    compound = score["compound"]

    if compound >= 0.05:
        sentiment = "חיובי"
    elif compound <= -0.05:
        sentiment = "שלילי"
    else:
        sentiment = "ניטרלי"

    return jsonify({"sentiment": sentiment, "score": compound})

if __name__ == "__main__":
    app.run(port=5000)
