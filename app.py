from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from twitter import *
import os
import re
from bayesbest import Bayes_Classifier_Best_Length

app = Flask(__name__)
search_text = ""

@app.route('/')
def home():
    global search_text
    if not session.get('logged_in'):
        consumer_key = "5DRYXXXXXXXXXXXXXXXXXOYRjSAjB"
        consumer_secret = "1JD9yjXXXXXXXXXXXXXX6mayN15IjEFjC"
        access_key = "16347943XXXXXXXXXXXXXMK3thdkJoHmhHIR"
        access_secret = "1h3fSXXXXXXXXXXXXXXXXXXXXXX9nfkWOi0jZqgf"

        twitter = Twitter(
            auth=OAuth(access_key, access_secret, consumer_key,
                       consumer_secret))

        if search_text == "":
            search_text = "Software Design"
        query = twitter.search.tweets(q=search_text)
        bc = Bayes_Classifier_Best_Length("")
        positive = 0
        negative = 0
        twitter_feed = ""
        i = 0
        for result in query["statuses"]:
            tweet = re.sub(r'([^\s\w]|_)+', '', result["text"])
            sentiment = bc.classify(tweet)
            query["statuses"][i]["sentiment"] = sentiment
            print sentiment
            if sentiment == "positive":
                positive += 1
            elif sentiment == "negative":
                negative += 1
            twitter_feed += sentiment + ":  " + result["user"]["screen_name"] + ":" + result["text"] + "\n"
            i = i + 1
        positive = positive / float(positive + negative)
        negative = negative / float(positive + negative)
        print positive
        return render_template('login.html', feeds=query["statuses"], twitter_feed=twitter_feed, positive=positive, negative=negative, neutral=0.4)
    else:
        return "Hello Boss!"


@app.route('/analyse', methods=['POST'])
def analyse():
    global search_text
    search_text = request.form['text']
    return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=5000)