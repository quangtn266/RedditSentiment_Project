import praw, time
from data import *
from helper import print_helper, visualization
from predict import sentiment_analysis

def data_extractor(reddit):
    '''
    Extract all the data from reddit.
    :param reddit (reddit object)
    :return: posts (int) - number of post analysis.
        c_analyzed (int) - number of comments analysis.
        tickers (dict) - dictionary of the tickers found
        titles (list) - list of the title of posts analysis
        a_comments (dict) - all the comments to analyze
        picks (int) - top picks to analyzer
        subs (int) - the number of subreddits alaysis
        pick_ayz (int) - top picks to analyze
    '''

    # set the program parameters

    # sub-reddit to research
    subs = ['wallstreetbets']

    # post flairs to search || None flair is automatically considered
    post_flairs = {'Daily Discussion', 'Weekend Discussion', 'Discussion'}

    # author whom comments are allowed more than once
    goodAuth = {'AutoModerator'}

    # allow one comment / 1 author/ 1 symbol
    uniqueCmt = True

    # authors ignores posts
    ignoreAuthP = {'example'}

    # authors ignores comment
    ignoreAuthC = {'example'}

    # up-vote ratio for post to be considered
    upvoteRatio = 0.70

    # define of up-vote, post is considered if up-vote exceeds "up"
    ups = 20

    # define the limit, comments "replace more limit"
    limit = 1

    # define up-vote, comment is considered if up-vote exceed "upvotes"
    upvotes = 2

    # define "picks" parameter
    picks = 10

    # define "pick_anyz" as the number of picks for sentiment analysis
    pics_ayz = 5

    posts, count, c_analyzed, tickers, titles, a_comments = 0, 0 ,0, {}, [], {}
    cmt_auth = {}

    for sub in subs:
        subreddit = reddit.subreddit(sub)

        # sorting posts by hot
        hot_python = subreddit.hot()

        # extracting comments, symbols from subreddit
        for submission in hot_python:
            flair = submission.link_flair_text
            author = submission.author.name

            # checking post upvote ratio for upvotes, post flair and author
            if submission.upvote_ratio >= upvoteRatio and submission.ups > ups \
                and (flair in post_flairs or flair is None) and author not in ignoreAuthP:
                submission.comment_sort = 'new'
                comments = submission.comments
                titles.append(submission.title)
                posts+=1

                try:
                    submission.comments.replace_more(limit=limit)
                    for comment in comments:
                        # try except for deleted account.
                        try: auth = comment.author.name
                        except:
                            pass
                        c_analyzed+=1

                        # checking: comment up-votes and author
                        if comment.score > upvotes and auth not in ignoreAuthC:
                            split = comment.body.split(" ")
                            for word in split:
                                word = word.replace("$", "")
                                # upper = ticket, length of ticker <= 5
                                # excluded words.
                                if word.isupper() and len(word) <=5 and \
                                    word not in blacklist and word in us:

                                    # unique comments, try/ except for key errors
                                    if uniqueCmt and auth not in goodAuth:
                                        try:
                                            if auth in cmt_auth[word]:
                                                break
                                        except:
                                            pass
                                    # counting tickers
                                    if word in tickers:
                                        tickers[word] +=1
                                        a_comments[word].append(comment.body)
                                        cmt_auth[word].append(auth)
                                        count+=1
                                    else:
                                        tickers[word]=1
                                        cmt_auth[word]=[auth]
                                        a_comments[word]=[comment.body]
                                        count+=1
                except Exception as e: print(e)
    return posts, c_analyzed, tickers, titles, a_comments, picks, subs, pics_ayz






def main():
    start_time = time.time()

    # reddit client

    reddit = praw.Reddit(user_agent="Comment Extraction", client_id="",
                         client_secret="", username="", password="")

    posts, c_analyzed, tickers, titles, a_comments, picks,\
    subs, picks_ayz = data_extractor(reddit)

    symbols, times, top = print_helper(tickers, picks, c_analyzed, posts, subs
                                       ,titles, time, start_time)

    scores = sentiment_analysis(picks_ayz, a_comments, symbols)
    visualization(picks_ayz, scores, picks, times, top)



if __name__ == '__main__':
    main()