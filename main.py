# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.
##################### Extra Hard Starting Project ######################
import os
import random
import pandas as pd
import smtplib
import datetime as dt
import requests
from twilio.rest import Client

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

today = dt.datetime.now()
today_tuple = (today.month, today.day)

# 1. Update the birthdays.csv
friends = ["Colin", "Shayan", "Skylar", "Dean"]
years = [2003, 2003, 2003, 2008]
months = [3, 2, 4, 6]
days = [12, 10, 12, 2]
email = ["gsvitti03@gmail.com"]*4
birthdays = pd.DataFrame(
    {
        "name": friends,
        "email": email,
        "year": years,
        "month": months,
        "day": days
    }
)

birthdays.to_csv("birthdays.csv", index=False)

birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in birthdays.iterrows()}
print(birthdays_dict)


# 2. Check if today matches a birthday in the birthdays.csv
if today_tuple in birthdays_dict:
    file_path = f"letter_templates/letter_{random.randint(1,3)}.txt"

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
    with open(file_path) as text_file:
        letter = text_file.read()
        finalized_letter = letter.replace("[NAME]", birthdays_dict[today_tuple]["name"])

# 4. Send the letter generated in step 3 to that person's email address.
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=birthdays_dict[today_tuple]["email"],
                            msg=f"Subject:Happy Birthday\n\n{finalized_letter}")
        
# Weather API section - part 2

parameters = {
    'lat': 32.715736,
    'lon': -117.161087,
    'appid': os.environ.get("OWM_API_KEY"),
    'cnt': 4,
}

OWM_endpoint = 'http://api.openweathermap.org/data/2.5/forecast'
response = requests.get(OWM_endpoint, params=parameters)
account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_TOKEN")

# 200 for success, 400 for failure
print(response.status_code)
# print(response.json())

time_list = response.json()['list']

weather_ids = []
weather_descriptions = []

for i in range (len(time_list)):
    subsection = time_list[i]
    weather = subsection['weather']
    weather_id = weather[0]['id']
    weather_description = weather[0]['description']

    weather_ids.append(weather_id)
    weather_descriptions.append(weather_description)

if any(weather_code < 700 for weather_code in weather_ids):
    # Initiate the client to send SMS message
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        from_='whatsapp:+14155238886',
        body="It's going to rain today, remember to bring an umbrella",
        to='whatsapp:+18586954115'
    )

    print(message.status)

else:
    print('The sky looks clear today, no need for an umbrella!')
