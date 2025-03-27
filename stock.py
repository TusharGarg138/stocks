import requests
from twilio.rest import Client


#required api keys and endpoints
Stock_api_key = "CAHLEF866LPVR8I1"
News_api_key = "9f939e33eb7642e99819a7b168115ce0"

Account_sid = "AC4c9844d365d2c8ea7c4f3b8c9b6a8377"
Auth_token = "435208cb1e4975ed5017f642999d3650"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

#stock api parameters
stock_param = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": Stock_api_key,
}

#getting response from stocks
response = requests.get(STOCK_ENDPOINT, params=stock_param)
#pprint(response.json())

#making list of that response
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

#fetching yesterday closing price
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)
#pprint(data_list)

#fetching day before yesterday price
day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday["4. close"]
print(day_before_yesterday_closing_price)

#calculating the how much percentage it changes
difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
print(difference)

up_down = None
if difference > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"

percentage = (difference/float(yesterday_closing_price)) *100
print(percentage)


if percentage > 5:
    news_params = {
        "apiKey": News_api_key,
        "qIntitle": COMPANY_NAME,

    }
    #fetching the news about the stock
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = (news_response.json()["articles"])
    #pprint(articles)

# taking only 3 of them
three_artices = articles[:3]
#pprint(three_artices)

formatted_articles = [f"{STOCK_NAME}: {up_down}, {percentage:.2f}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_artices]

#sending the sms to user about all the information of stock price
client = Client(Account_sid, Auth_token)
from_number = "+19786339926"
to_number = "+917717425541"
for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_=from_number,
        to=to_number
    )

