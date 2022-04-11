import flask
import tweepy
from flask import Flask, render_template, request

app = Flask(__name__)
user_keyword = ""


@app.route("/", methods=["GET", "POST"])
def home():
    global user_keyword
    if request.method == "POST":
        user_keyword = request.form["name"]
        auth = tweepy.OAuth1UserHandler(
            "Jk6t5MKWGxBcQvcoXaiIupAvT", "vm3PAf0ATB8SuXfNl9YCa2PRPyrYxlZ5GqNfz1lRqbKzMlK7VL",
            "1280546155403735040-rDXai7OVXP9vjN2iOvxvFEXhgcdLWV", "c0itxNKnevXCpGGgCEZBGG5qEuni9uc4HX5llA5EZWogg"
        )

        api = tweepy.API(auth)
        test = api.search_tweets(q=user_keyword, lang="en", count=100, result_type="recent")
        tweets = []
        names = []
        for num in test:
            tweets.append(num._json["text"])
            try:
                names.append(num._json["entities"]["user_mentions"][0]['screen_name'])
            except:
                print("Name not Inserted")

        for tweet in tweets:
            print(tweet)

        for name in names:
            print(name)
        return render_template("index.html")

    return render_template("index.html")


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)
