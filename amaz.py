import time
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

email_id = "Enter your Email address over here"
email_pass = "Enter your password over here"
URL = "Enter the URL of the product here"


def check_price(prev):
    headers = {
        "User-Agent": "Instructions for this are given in the readme file"}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    price = soup.find(class_="a-size-medium a-color-price priceBlockBuyingPriceString").get_text()[2:]
    converted_price = int(price.split(".")[0].replace(",", ""))

    if converted_price < prev:
        notify_mail()
        return 2, converted_price
    return 1, converted_price


def notify_mail():
    msg = EmailMessage()
    msg['Subject'] = "Hurry Up! The price has fallen"
    msg['From'] = email_id
    msg['To'] = email_id
    msg.set_content(
        "Dear customer, \n The price of the product that you had wanted to buy for so long has fallen. \nGo to %s to buy it right now." % (
            URL))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_id, email_pass)
        smtp.send_message(msg)


x = 1
prev = 0
while x:
    x, prev = check_price(prev)
    if x == 1:
        time.sleep(1440)
    else:
        time.sleep(10080)
