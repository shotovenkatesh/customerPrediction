import flask
import tweepy
from flask import Flask, render_template, request
from collections import Counter
from functools import reduce
from monkeylearn import MonkeyLearn
import random

app = Flask(__name__)
user_keyword = ""
users_tweet_count = {}
max_users_tweets = {}
user_scores = {}
final_statements = {}
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
        #     data.append(tweet)
        # print(data)

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

        # print(highest_tweet_users)
        for dup in highest_tweet_users:
            max_users_tweets[dup] = []
            lettersIndexes = [i for i in range(len(names)) if names[i] == dup]
            for indx in lettersIndexes:
                max_users_tweets[dup].append(tweets[indx])

        ml = MonkeyLearn('ea64be9b30f12ba9ad817f8eb0a9e98d23b496bc')
        # def sentiment_classifer(*args):
        #     for result in args:
        #         sentiment = result["classifications"][0]["tag_name"]
        #         confidence = result["classifications"][0]["confidence"]
        #         store = [sentiment,confidence]
        #         sentiment_confidence[user_tweet].append(store)
        # print(max_users_tweets)

        sentiment_confidence = {}
        # in the above hash, user name is stored as key, values are sentiment and cofidence
        for user_tweet in max_users_tweets:
            # data is tweets of all the users
            # when the loop runs for the first time data will have tweets of the highest user(all of em)
            # each time the loop runs data will change tweets but will store of tweets of coresponding user
            data = max_users_tweets[user_tweet]
            model_id = 'cl_pi3C7JiL'
            result = ml.classifiers.classify(model_id, data)
            # in result.body , variable text becomes individual tweets
            sentiment_confidence[user_tweet] = []
            for result in result.body:
                sentiment = result["classifications"][0]["tag_name"]
                confidence = result["classifications"][0]["confidence"]
                store = [sentiment, confidence]
                sentiment_confidence[user_tweet].append(store)
        print(sentiment_confidence)



        def calculate_score(score_list):
            overall_score = 0
            for score in score_list:
                sentiment = score[0]
                if sentiment == "Neutral":
                    overall_score += 0.5
                elif sentiment == "Positive":
                    overall_score += 1
                else:
                    overall_score -= 1
            return overall_score

        for score in sentiment_confidence:
            d = ["5%", "10%", "12%", "7%"]
            final_score = 0
            showdown = ""
            user_name = score
            total_tweet = len(sentiment_confidence[score])
            thershold = (total_tweet / 2) - 0.5
            user_data = sentiment_confidence[user_name]
            overall_score = calculate_score(user_data)
            final_score = (overall_score * 100) / total_tweet
            # print(final_score)
            if final_score < 0:
                showdown = random.choice(d)
            elif final_score == 0:
                showdown = "50%"
            else:
                showdown = f"{final_score}%"
            # print(showdown)
            user_scores[user_name] = showdown



        for user in user_scores:
            actual_score = user_scores[user]
            score = int(float(actual_score.replace('%', '')))
            statement = ""
            if score >= 50:
                statement = f"{user} has a keen interest in this area of field "
            elif score >= 15 and score < 50:
                statement = f" It's possible that the {user} is intrigued"
            else:
                statement = f'{user} is less likely to be interested in this area of field'
            final_statements[user] = statement


        # for result in result.body:
        #     sentiment = result["classifications"][0]["tag_name"]
        #     confidence = result["classifications"][0]["confidence"]
        #     store = [sentiment,confidence]
        #     sentiment_confidence[user_tweet].append(store)

        for key in max_users_tweets:
            users_tweet_count[key] = len(max_users_tweets[key])

        # print(users_tweet_count)

        # print(user_with_more_tweets)
        user_with_sentiment_count = {}
        # for sentiment in sentiment_confidence:
        #     user_with_sentiment_count[sentiment] = [ ]
        # print(user_with_sentiment_count)
        for sen in sentiment_confidence:
            user = sentiment_confidence[sen]

            first_element = 0
            # print(user)

            neutral = 0
            positive = 0
            negative = 0
            for sentiment in user:
                element = sentiment[0]
                if element == "Neutral":
                    neutral+= 1
                elif element == "Negative":
                    negative += 1
                else:
                    positive += 1
            final_append = [positive,negative,neutral]
            # print(user_with_sentiment_count[sen])
            # print(final_append)
            user_with_sentiment_count[sen] = final_append
        # print(user_with_sentiment_count)




        return render_template("submit.html", names=max_users_tweets, tweet_no=users_tweet_count,sentiment = user_with_sentiment_count)
    # return render_template("submit.html")


@app.route("/tweets", methods=["GET", "POST"])
def show_tweets():
    global max_users_tweets
    global users_tweet_count
    global final_statements
    global user_scores

    print(user_scores)
    print(final_statements)


    if request.method == "POST":
        user_name = request.form["u_name"]
        return render_template("tweets.html", tweets=max_users_tweets, tw_id=user_name,scores = user_scores,statement = final_statements)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=80)

# TODO
