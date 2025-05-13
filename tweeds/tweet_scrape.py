import snscrape.modules.twitter as api
import pandas as pd
import json
from datetime import date, timedelta

def make_json(data, jsonFilePath):
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

def printRes(tweet: api.Tweet):
    print(f"{tweet.id} {tweet.date} <{tweet.user.username}> {tweet.rawContent} \n")

def toOBJ(tweet: api.Tweet) -> object:
    return {
        "id": tweet.id,
        "date": tweet.date.strftime('%Y/%m/%d'),
        "username": tweet.user.username,
        "content": tweet.rawContent,
        "likes": tweet.likeCount,
        "retweet": tweet.retweetCount,
        "reply": tweet.replyCount,
        "user": {
            "username": tweet.user.username,
            "followers": tweet.user.followersCount,
            "displayName": tweet.user.displayname,
            "id": tweet.user.id
        },
        "url": tweet.url
    }

def search_user_last_4_years(username: str, limit: int = None, json_output: str = None, csv_output: str = None, silent: bool = False) -> None:
    """
    Search for tweets from a specific user for the last four years.

    Args:
        username (str): The username to search for (e.g., "MOE_BHH_01_0047").
        limit (int, optional): The maximum number of tweets to retrieve. Defaults to None (no limit).
        json_output (str, optional): Path to save the output in JSON format. Defaults to None.
        csv_output (str, optional): Path to save the output in CSV format. Defaults to None.
        silent (bool, optional): If True, don't print the tweets to the console. Defaults to False.
    """
    today = date.today()
    four_years_ago = today - timedelta(days=4 * 365)  # تقريبي لـ 4 سنوات

    query = f"(from:{username}) since:{four_years_ago.strftime('%Y-%m-%d')} until:{today.strftime('%Y-%m-%d')}"
    jsonObj = {}
    csvObj = []

    for i, tweet in enumerate(api.TwitterSearchScraper(query).get_items()):
        if limit and i == limit:
            break
        jsonObj[tweet.id] = toOBJ(tweet)
        csvObj.append(
            [tweet.id, tweet.date, tweet.rawContent, tweet.url,
             tweet.likeCount, tweet.retweetCount, tweet.replyCount, tweet.sourceLabel[12:]]
        )
        if not silent:
            printRes(tweet)

    if json_output:
        if json_output.endswith(".json"):
            make_json(jsonObj, json_output)
            print("Output saved in JSON!")
        else:
            print("Error: JSON output file must end with '.json'")

    if csv_output:
        if csv_output.endswith(".csv"):
            df = pd.DataFrame(
                csvObj, columns=["ID", "Date", "Tweet", "URL", "Likes", "Retweet", "Replies", "Source"])
            df.to_csv(csv_output, encoding='utf-8')
            print("Output saved in CSV!")
        else:
            print("Error: CSV output file must end with '.csv'")

if __name__ == '__main__':
    username_to_scrape = "@MOE_BHH_01_0047"
    # يمكنك تعديل هذه الخيارات حسب حاجتك
    number_of_tweets = 100  # يمكنك تغيير هذا الرقم لعدد التغريدات التي تريدها
    output_json_file = "moe_bhh_tweets_last_4_years.json"
    output_csv_file = "moe_bhh_tweets_last_4_years.csv"
    print_tweets_to_console = True

    search_user_last_4_years(
        username=username_to_scrape.replace("@", ""), # قم بإزالة علامة @ عند تمرير اسم المستخدم إلى الدالة
        limit=number_of_tweets,
        json_output=output_json_file,
        csv_output=output_csv_file,
        silent=not print_tweets_to_console
    )