import tweepy
import time
import pandas as pd
import csv
import os
from datetime import datetime

API_KEY = "8ilH0Z268J2vt2aldWg5PvJPm"
API_SECRET_KEY = "4wjoqOLIxeDo169jArioDw2fMFFAvRbWooPdQhnxwk3pax6X3C"

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY, 'oob')
redirect_url = auth.get_authorization_url()
print("Open this link and log in with your Twitter profile.")
print(redirect_url)

USER_PIN = input("What's the pin value? ")

auth.get_access_token(USER_PIN)

api = tweepy.API(auth,
                 wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True,
                 retry_count=5,  # retry 5 times
                 retry_delay=5,  # seconds to wait for retry
                 )

os.makedirs(os.path.join('data', 'fetch'), exist_ok=True)

# Variable containing the path of the csv to analyze
PATH_CSV = 'data/fetch/followers.csv'

def words_in_phrase(words, phrase):
  """
  words_in_phrase()
    This function verify that at least one word of a set is contained in a phrase.

  :param words: This is the set of a words
  :param phrase: This is the phrase to check

  :return: If at least one word of a set is contained in the phrase, then the function return True.
  """

  res = False

  for w in words:
    if w in phrase:
      res = True
      break

  return res

def extract_timeline_as_df(timeline_list):
  """
  extract_timeline_as_df()
    This function extract the timeline of a user as a DataFrame of Pandas.
    It also creates the DF by filtering the timeline with the tweets published only in November
    and that contains at least one word about the Covid-19.

  :param timeline_list: This is the timeline of a user.

  :return: The Pandas' DataFrame already filtered, with user, author, date and text of a tweet.
  """

  columns = set()
  allowed_types = [str, int]
  tweets_data = []

  selected_month = ['Oct','Nov','Dec']
  selected_words = ['covid', 'vaccin', 'lockdown', 'pandemi', 'congiunt', 'coronavirus', 'dpcm', 'contag', 'mascherin', 'surgical', 'mask']

  for status in timeline_list:
    status_dict = dict(vars(status))
    keys = status_dict.keys()

    # Save the tweet if it was published in November
    if status.created_at.strftime("%b") in selected_month:
      # Save the tweet if it was published a tweet with the selected words
      if words_in_phrase(selected_words, status.text.lower()):
        # Save the tweet's data in a Python's dictionary
        single_tweet_data = {"user": status.user.screen_name, "date": status.created_at, "text": status.text}
        for k in keys:
          try:
            v_type = type(status_dict[k])
          except:
            v_type = None
          if v_type != None:
            if v_type in allowed_types:
              single_tweet_data[k] = status_dict[k]
              columns.add(k)
        tweets_data.append(single_tweet_data)

  header_cols = list(columns)
  header_cols.append("user")
  header_cols.append("date")
  header_cols.append("text")

  df = pd.DataFrame(tweets_data, columns=header_cols)
  return df


def print_log(string):
    """
    print_log()
      With this function I created an indented print function.

    :param string: This is the string to be indented.

    :return: The function returns a indented print.
    """

    tab_string = ""
    for t in range(DEPTH_LEVEL, 3):
        tab_string += "\t"

    return print(tab_string, string)


def find_followers(id_query, mode_file, isLast):
    """
    find_followers()
      This function will collect a set number of followers for the user's input id.
      In addition, the function will allow you to save the user-follower pair in a csv.
      Since it is a long process, within the function there is a way to print the time
      when it is actually executed so that I can keep it under control.

    :param id_query: This is the id of the user whose followers you want to know about.
    :param mode_file: This is a variable that will allow you to create the csv file, if you are analyzing the first user,
                        or to hang it, if you are analyzing a later user.
    :param isLast: This variable indicates if I interested to analyze the user's followers.

    :return: The function returns a vector ID of the followers of the user passed in input.
    """

    # Output variable
    friends = []

    with open(PATH_CSV, mode_file) as csv_file:
        # Number of followers of the user passed in input to be analyzed in the next rounds
        NUM_FOLLOWERS_ANALYZE = 3
        # Number of followers to be saved for the user passed in input
        NUM_FOLLOWERS_COLLECT = 20
        # Number of followers to be retrieved for the user passed in input
        NUM_FOLLOWERS = 10000

        writer = csv.writer(csv_file)
        print_log("---Round--- " + datetime.now().strftime("%H:%M:%S"))

        n = 0
        try:
            curs = tweepy.Cursor(api.followers, id=id_query).items(NUM_FOLLOWERS)
            for j, _id in enumerate(curs):
                j += 1
                if j % 100 == 0:
                    print_log("#Operation: " + str(j))
                    if isLast == True:
                        time.sleep(120)

                _id = _id.screen_name
                # The condition is true if I interested to analyze the user's followers
                if isLast == False:
                    try:
                        # The condition is true if the number of followers to analyze wasn't completed
                        # and if the number of tweets of the user are at least one
                        # and if the number of followers of the user is at least one

                        if n < NUM_FOLLOWERS_ANALYZE:
                            user = api.get_user(_id)
                            user_timeline = user.timeline(count=1000)
                            df = extract_timeline_as_df(user_timeline)

                            if len(df) > 0:
                                api_foll = api.followers(_id)

                                if len(api_foll) > 0:
                                    friends.append(_id)
                                    n += 1
                                    print_log("Follower to analyze n " + str(
                                        n) + " - User ID: " + _id + " - Total num: " + str(
                                        j) + " - " + datetime.now().strftime("%H:%M:%S"))
                                    time.sleep(60)

                            writer.writerow([id_query, _id])
                            print_log("Writing of follower to analyze... " + id_query + " " + _id)
                            continue
                    except tweepy.TweepError:
                        # It may happen that the user in question has a private profile.
                        # In this case, it will be impossible to access his data and therefore it will be necessary to skip it
                        print_log("The user has hidden his followers, skipping... " + _id + " - Total num: " + str(
                            j) + " - " + datetime.now().strftime("%H:%M:%S"))
                        continue

                if j < NUM_FOLLOWERS_COLLECT:
                    writer.writerow([id_query, _id])
                    print_log("Writing... " + id_query + " " + _id + " - Total num: " + str(j))
                else:
                    if isLast == False:
                        if n >= NUM_FOLLOWERS_ANALYZE:
                            time.sleep(60)
                            return friends
                    else:
                        time.sleep(60)
                        return friends

        except tweepy.RateLimitError:
            # If I exceed the Rate limit of the Twitter API
            print_log("Waiting... " + datetime.now().strftime("%H:%M:%S"))
            # Retry the function
            friends = find_followers(id_query, mode_file)
        except tweepy.TweepError:
            # It may happen that the user in question has a private profile.
            # In this case, it will be impossible to access his data and therefore it will be necessary to skip it
            print_log("The user has hidden his followers, skipping... " + id_query + " " + datetime.now().strftime(
                "%H:%M:%S"))

    # I wait a minute each time to try to avoid that Twitter makes me wait for the rate limit time
    time.sleep(60)
    return friends


def recursive_follower_analysis(followers, mode_file, isLast):
    """
    recursive_follower_analysis()
      This function is a recursive function, which allows you to carry out the
      process of creating the dataset according to the depth we choose through a
      global constant called DEPTH_LEVEL.

    :param followers: This is the variable that contains all the users to analyze.
    :param mode_file: This is a variable that will allow you to create the csv file, if you are analyzing the first user,
                        or to hang it, if you are analyzing a later user.
    :param isLast: This variable indicates if I interested to analyze the user's followers.
    """

    global DEPTH_LEVEL

    for num, f in enumerate(followers, start=1):
        print("")
        print_log("-> DEPTH LEVEL:" + str(DEPTH_LEVEL))
        print_log(str(num) + " - FOR - User ID: " + f)
        foll = find_followers(f, mode_file, isLast)
        print_log("LEN: " + str(len(foll)))

        DEPTH_LEVEL -= 1

        if DEPTH_LEVEL >= 1:
            if DEPTH_LEVEL == 1:
                recursive_follower_analysis(foll, "a", True)
            else:
                recursive_follower_analysis(foll, "a", False)

        DEPTH_LEVEL += 1


first_twiter = "SkyTG24"  # SkyTG24's Twitter

DEPTH_LEVEL = 2

print("START: User ID:",first_twiter,datetime.now().strftime("%H:%M:%S"))
recursive_follower_analysis([first_twiter], "w", False)
print("Done",datetime.now().strftime("%H:%M:%S"))

