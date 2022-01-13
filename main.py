import os
from dotenv import load_dotenv
import csv
import praw

load_dotenv()

version = 0
user_agent = f"{os.environ['APP_ID']}:{version}:{os.environ['USERNAME']}"

reddit = praw.Reddit(
    client_id=os.environ['APP_ID'],
    client_secret=os.environ['APP_SECRET'],
    user_agent=user_agent,
)


def get_fitness_posts():
    fitness_subreddit = reddit.subreddit('fitness')
    bodybuilding_subreddit = reddit.subreddit('bodybuilding')
    powerlifting_subreddit = reddit.subreddit('powerlifting')
    bodyweightfitness_subreddit = reddit.subreddit('bodyweightfitness')

    with open('data.csv', 'w', encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f)
        fitness_submissions = set()
        bodybuilding_submissions = set()
        powerlifting_submissions = set()
        for submission in fitness_subreddit.new(limit=400):
            fitness_submissions.add(submission.selftext)

        for submission in bodybuilding_subreddit.new(limit=1500):
            bodybuilding_submissions.add(submission.selftext)

        for submission in bodyweightfitness_subreddit.new(limit=500):
            # fill bodybuilding submissions to reach 100 items
            bodybuilding_submissions.add(submission.selftext)

        for submission in powerlifting_subreddit.new(limit=1200):
            powerlifting_submissions.add(submission.selftext)

        print(len(fitness_submissions))
        print(len(bodybuilding_submissions))
        print(len(powerlifting_submissions))

        for submission in fitness_submissions:
            if "Daily Simple Questions Thread" not in submission:
                writer.writerow([submission, 'fitness'])

        for submission in bodybuilding_submissions:
            writer.writerow([submission, 'bodybuilding, fitness'])

        for submission in powerlifting_submissions:
            writer.writerow([submission, 'powerlifting, fitness'])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_fitness_posts()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
