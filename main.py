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

subs_categories = [
    {
        'category': 'fitness',
        'subs': [
            {
                'name': 'fitness',
                'keywords': ['fitness']
            },
            {
                'name': 'bodybuilding',
                'keywords': ['bodybuilding']
            },
            {
                'name': 'powerlifting',
                'keywords': ['powerlifting']
            },
            {
                'name': 'bodyweightfitness',
                'keywords': ['bodyweightfitness']
            }
        ]
    },
    {
        'category': 'programming',
        'subs': [
            {
                'name': 'learnprogramming',
                'keywords': ['learnprogramming']
            },
            {
                'name': 'WebDev',
                'keywords': ['webdev', 'web development']
            },
            {
                'name': 'Frontend',
                'keywords': ['Frontend', 'frontend development']
            },
            {
                'name': 'AskProgramming',
                'keywords': ['AskProgramming', 'ask programming']
            },
            {
                'name': 'Coding',
                'keywords': ['coding']
            },
            {
                'name': 'JavaScript',
                'keywords': ['javascript', 'js', 'es6']
            },
            {
                'name': 'LearnJavaScript',
                'keywords': ['LearnJavaScript', 'javascript', 'js', 'es6']
            }
        ]
    }
]


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


def get_posts():
    praw_subs = []
    for subreddit in subs_categories:
        for sub in subreddit['subs']:
            praw_subs.append({'sub': sub,
                              'category': subreddit['category'],
                              'praw': reddit.subreddit(sub['name'])})

    with open('data.csv', 'w', encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f)
        results = []
        for sub in praw_subs:
            submissions = set()
            for submission in sub['praw'].new(limit=1500):
                submissions.add(submission.selftext)
            results.append({
                'sub': sub['sub'],
                'category': sub['category'],
                'submissions': submissions
            })

        for result in results:
            print(result['sub'], len(result['submissions']))

        # every keyword should have more than 100 items available or else
        # importing the dataset in automl fails
        results = [result for result in results if len(result['submissions']) >= 100]

        for result in results:
            for submission in result['submissions']:
                keywords = [*result['sub']['keywords'], result['category']]
                writer.writerow([submission, ','.join(keywords)])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #get_fitness_posts()
    get_posts()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
