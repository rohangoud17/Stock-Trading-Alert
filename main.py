import requests
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Stock name = TSLA

STOCK_NAME = input("Please enter your stock name: ")
COMPANY_NAME = input("Please enter your Company name: ")
API_key = "CZMMMP02IBF93GW2"
news_api_key = "9dd4f0baa5714819aea38981f1328dea"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": API_key
}

news_parameters = {
    "apiKey" : news_api_key
}

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
connection = requests.get(url= STOCK_ENDPOINT, params= parameters)
connection.raise_for_status()
data = connection.json()
closing_price_28 = data["Time Series (Daily)"]['2024-06-28']["4. close"]
# 
#TODO 2. - Get the day before yesterday's closing stock price
closing_price_27 = data["Time Series (Daily)"]['2024-06-27']["4. close"]

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(float(closing_price_28)-float(closing_price_27))
difference = round(difference,2)

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage = difference/float(closing_price_27)*100

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if percentage < 5:
    

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news_connection = requests.get(url= "https://newsapi.org/v2/everything?q=TSLA&apiKey=9dd4f0baa5714819aea38981f1328dea")
    news_connection.raise_for_status()

    news_articles = news_connection.json()



    articles = news_articles["articles"][0:4]



    article_formatted= [f"brief:{art["title"]}\ndescription:{art["description"]}" for art in articles]
    message = random.choice(article_formatted)

    # Set up the email content using MIMEText to ensure proper encoding
    msg = MIMEMultipart()
    msg['From'] = "simbathelion987@gmail.com"
    msg['To'] = "rohangoud8417@gmail.com"
    msg['Subject'] = f"{percentage:.2f}"

    # Attach the plain text message
    msg.attach(MIMEText(message, 'plain', 'utf-8'))

    # Sending the email
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()  # Secure the connection
        connection.login(user="simbathelion987@gmail.com", password="jwybkqgnliqpdxbe")
        connection.sendmail(from_addr="simbathelion987@gmail.com", to_addrs="rohangoud8417@gmail.com", msg=msg.as_string())






#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

