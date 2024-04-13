from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key="c75a43f75e03424594fb07524e1b90ee")
top_headlines = newsapi.get_top_headlines(q="Singapore", language="en", country="sg")

print(top_headlines)    