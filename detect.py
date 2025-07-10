from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# יצירת אובייקט של מנתח הרגשות
analyzer = SentimentIntensityAnalyzer()

# קריאה מקובץ
with open("sentences.txt", "r", encoding="utf-8") as f:
    sentences = [line.strip() for line in f if line.strip()]

# ניתוח וכתיבה לתוצאה
with open("results.txt", "w", encoding="utf-8") as out:
    for idx, text in enumerate(sentences, 1):
        score = analyzer.polarity_scores(text)
        compound = score['compound']

        if compound >= 0.05:
            sentiment = "חיובי"
        elif compound <= -0.05:
            sentiment = "שלילי"
        else:
            sentiment = "ניטרלי"

        out.write(f"{idx}. '{text}' → {sentiment} (ציון: {compound})\n")

print("✓ ניתוח הרגשות הסתיים. התוצאות נשמרו בקובץ 'results.txt'")
