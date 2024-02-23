import os
from dotenv import load_dotenv
import smtplib
import requests
import datetime

load_dotenv()



#Sends a mail with the message string parameter.
def send_mail(message):
    app_email = os.getenv("APP_MAIL")
    app_password = os.getenv("APP_PASS")
    destination_email = os.getenv("DESTINATION_MAIL")
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=app_email, password=app_password)
    connection.sendmail(from_addr=app_email, to_addrs=destination_email, msg=message)
    connection.close()
    return


#Checks for cnn fear and greed index signals. Two default int parameters determining min and max. Returns a string if any of those values are triggered.
def fear_n_greed_signal(min=25, max=75):

    #Makes an api request for the cnn fear and greed signal. 
    response = requests.get("https://fear-and-greed-index.p.rapidapi.com/v1/fgi", headers={
        'X-RapidAPI-Key': 'cef161ed84msh2d62e5d9b7e0592p110b00jsne69dc48671c6',
        'X-RapidAPI-Host': 'fear-and-greed-index.p.rapidapi.com'
    }).json()

    current_index_value = f"The current value is {response['fgi']['now']['value']} and the market condition is {response['fgi']['now']['valueText']}."
    value = int(response['fgi']['now']['value'])

    ##Checks for value between at both ends.
    if value < min:
        return "Fear and greed:\nRipe to buy, getting oversold!!!" + current_index_value
    elif value > max:
        return "Fear and greed:\nGetting too overbought!!!" + current_index_value
    else:
        return

##Checks for all signals and returns a string.
def screener():
    signals = ""
    ##Checks for fear_n_greed signal. Can adjust min and max value.
    signals += fear_n_greed_signal() + "\n\n"
    return signals
    
    
if __name__ == "__main__":
    date = str(datetime.datetime.now())
    title = "Subject: Daily market screener\n\n" + date +"\n\n"
    new_message = screener()

    ##Only sends a mail if screener finds a signal.
    if new_message:
        send_mail(title + new_message)
    



