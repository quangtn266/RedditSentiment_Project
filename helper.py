import time
import pandas as pd
import squarify
import matplotlib.pyplot as plt

def print_helper(tickers, picks, c_analyzed, posts, subs, titles, time, start_time):
    '''
    Print out top tickers, and most mentioning tickers

    :param tickers: dict - all the tickers found
    :param picks: int - top picks to analyze
    :param c_analyzed: int - the number of comments analyzed
    :param posts: int - the number of posts analyzed
    :param subs: int - the number of subreddits analyzed
    :param titles: list - list of the titles for post analysis
    :param time: time obj - top picks to analyze
    :param start_time: time obj - program start time
    :return:
        symbols: dict - dictionary of sorted tickers based on mentions
        times: list - include the number of time top tickers are mentioned
        top: list - list of top tickers
    '''

    # sorts the dictionary
    symbols = dict(sorted(tickers.items(), key=lambda item: item[1], reverse=True))
    top_picks = list(symbols.keys())[:picks]
    time = time.time - start_time

    # print top picks
    print("it took {t:2f) second to analyze {c} comments in {p} posts in {s} subreddit."
          "\n".format(t=time, c=c_analyzed, p=posts, s=len(subs)))
    print("Post analyzed saved in titles")
    print(f"\n{picks} most mentioned tickers: ")

    times = []
    top = []
    for i in top_picks:
        print(f"{i}: {symbols[i]}")
        times.append(symbols[i])
        top.append(f"{i}: {symbols[i]}")

    return symbols, times, top

def visualization(picks_ayz, scores, picks, times, top):
    """
    + Print sentiments analysis
    + Make a mentioned picks chart
    + make a chart of sentimart analysis of top picks

    :param picks_ayz:
    :param scores:
    :param picks:
    :param times:
    :param top:
    :return:
    """

    # print sentiment analysis
    print(f"\nSentiment analysis of top {picks_ayz} picks")
    df = pd.DataFrame(scores)
    df.index = ['Bearish', 'Neutral', 'Bullish', 'Total/ Compound']
    df = df.T

    print(df)

    # Date visualization
    # most mentioned picks
    squarify.plot(sizes=times, label=top, alpha=.7)
    plt.axis('off')
    plt.title(f"{picks} most mentioned picks")

    # sentiment analysis
    df = df.astype(float)
    colors = ['red', 'springgreen', 'forestgreen', 'coral']
    df.plot(kind='bar', color=colors, title=f'Sentiment analysis of top {picks_ayz} picks:')
    plt.show()