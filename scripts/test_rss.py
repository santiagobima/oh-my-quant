import feedparser

feed_url = "https://finance.yahoo.com/news/rss"
feed = feedparser.parse(feed_url)

print('Feed Title:', feed.feed.title)
for entry in feed.entries[:5]:
    print('-', entry.title)
    print('  Link:', entry.link)
    print('  Published:', entry.published)
    print()
# End of file