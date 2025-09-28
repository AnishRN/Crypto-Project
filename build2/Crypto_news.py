import yfinance as yf
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
from googlesearch import search
import datetime

def get_historical_stock_data(stock_symbol, start_date, end_date):
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    return stock_data

def extract_news_links(search_query, num_links=5):
    news_links = []
    search_results = search(search_query, num_results=num_links, lang='en')

    for result in search_results:
        if "news" in result:
            news_links.append(result)
    return news_links

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

def main():
    stock_symbol = input("Enter the stock symbol: ")
    start_date = 2020-1-0
    end_date = datetime.datetime.now()
    
    try:
        stock_data = get_historical_stock_data(stock_symbol, start_date, end_date)
        if stock_data.empty:
            print("No stock data found for the given date range.")
            return
        
        print(f"Analyzing historical performance of {stock_symbol} stock:")
        print(stock_data)
        
        search_query = f"{stock_symbol} stock news"
        news_links = extract_news_links(search_query)
        
        if not news_links:
            print("No news articles found.")
            return
        
        print(f"Analyzing news articles related to {stock_symbol} stock:")
        
        for link in news_links:
            try:
                response = requests.get(link)
                soup = BeautifulSoup(response.text, 'html.parser')
                news_text = ""
                for paragraph in soup.find_all('p'):
                    news_text += paragraph.get_text()
                sentiment_score = analyze_sentiment(news_text)
                
                print(f"News Article Link: {link}")
                print(f"Sentiment Score: {sentiment_score:.2f}")
                print("-" * 50)
            except Exception as e:
                print(f"Error processing article: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
