import requests
from bs4 import BeautifulSoup

# Define the URL of the website you want to scrape
url = 'https://www.coindesk.com/'

# Define CSS selectors for data points
headline_selector1 = 'h6'  # h6 or h3 (featured)
headline_selector2 = 'h3'
summary_selector = 'p'
author_selector = 'div.gJMKuU a'  # check if this exist bcz only articles have this
time_selector = 'div.eeyqKG span'
link_selector = 'a.card-title-link'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the webpage
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the news article elements
articles = soup.select_one('div.kuxwiI')

# Initialize an empty list to store the extracted data
news_data = []

# Iterate over each article and extract data
for article in articles:

    author = article.select_one(author_selector)
    if author is None:
        continue  # article always have an author so use it to detect whether the item in list is a new article or something else
    else:
        author = author.text.strip()

    headline = article.select_one(headline_selector1)
    headline = article.select_one(headline_selector2) if headline is None else headline

    headline = headline.text.strip()

    summary = article.select_one(summary_selector).text.strip()

    time = article.select_one(time_selector).text.strip()

    link = article.select_one(link_selector)['href']
    link = url + link

    # Create a dictionary to store the extracted data
    article_data = {
        'headline': headline,
        'summary': summary,
        'author': author,
        'time': time,
        'link': link
    }

    # Append the dictionary to the list
    news_data.append(article_data)

# Print the array of objects containing the extracted data
for data in news_data:
    print("Article headline: ", data["headline"])
    print("Article summary: ", data["summary"])
    print("Article author: ", data["author"])
    print("Article link: ", data["link"])
    print("Article time: ", data["time"], "\n\n")
