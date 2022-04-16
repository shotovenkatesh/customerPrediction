import flask
import tweepy
from flask import Flask, render_template, request
from collections import Counter
from functools import reduce

app = Flask(__name__)
user_keyword = ""
users_tweet_count = {}
max_users_tweets = {}
u_name = ""


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    global user_keyword
    global u_name
    global max_users_tweets
    global users_tweet_count
    if request.method == "POST":
        user_keyword = request.form["name"]
        auth = tweepy.OAuth1UserHandler(
            "Jk6t5MKWGxBcQvcoXaiIupAvT", "vm3PAf0ATB8SuXfNl9YCa2PRPyrYxlZ5GqNfz1lRqbKzMlK7VL",
            "1280546155403735040-rDXai7OVXP9vjN2iOvxvFEXhgcdLWV", "c0itxNKnevXCpGGgCEZBGG5qEuni9uc4HX5llA5EZWogg"
        )

        api = tweepy.API(auth)
        try:
            test = api.search_tweets(q=user_keyword, lang="en", count=200, result_type="recent", tweet_mode="extended")
        except:
            return render_template("index.html")

        tweets = []
        names = []
        # print(test)
        for num in test:

            tweets.append(num._json["full_text"])
            try:
                names.append(num._json["entities"]["user_mentions"][0]['screen_name'])
            except:
                # print("Name not Inserted")
                pass

        # for tweet in tweets:
        #     print(tweet)

        # for name in names:
        #     first_user = name
        user_with_more_tweets = reduce(lambda names, b: names + [b[0]] * b[1],
                                       sorted(Counter(names).items(), key=lambda x: x[1], reverse=True),
                                       [])

        # get highest_tweet_users,loop and find their index

        highest_tweet_users = []

        for i in names:
            if names.count(i) > 1 and i not in highest_tweet_users:
                highest_tweet_users.append(i)

        print(highest_tweet_users)
        for dup in highest_tweet_users:
            max_users_tweets[dup] = []
            lettersIndexes = [i for i in range(len(names)) if names[i] == dup]
            for indx in lettersIndexes:
                max_users_tweets[dup].append(tweets[indx])

        print(max_users_tweets)

        for key in max_users_tweets:
            users_tweet_count[key] = len(max_users_tweets[key])

        print(users_tweet_count)

        # print(user_with_more_tweets)

        return render_template("submit.html", names=max_users_tweets, tweet_no=users_tweet_count)
    # return render_template("submit.html")


@app.route("/tweets", methods=["GET", "POST"])
def show_tweets():
    global max_users_tweets
    global users_tweet_count

    if request.method == "POST":
        user_name = request.form["u_name"]
        return render_template("tweets.html", tweets=max_users_tweets, tw_id=user_name)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)

# TODO
