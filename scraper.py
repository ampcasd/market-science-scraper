import pandas as pd
import requests
import csv
import asyncio
import datetime
import re

# ---- Global Variables
day = datetime.datetime.now()
query_date = ""
# ----


def build_market_science_url():
    global query_date

    url = "https://marketsscience.com/daily_report_%Date%.html"
    query_date = day.strftime("%d%b%Y")
    print("Date", query_date)
    return url.replace("%Date%", query_date)


# ---- Editable Parameters
url = build_market_science_url()
# ----


# ---- Global Variables
filename = url[8:18] + ".csv"
df = ""
# ----


async def loop():
    global day, df

    while int(day.strftime("%Y")) > 2019:
        try:

            url = build_market_science_url()
            df = pd.read_csv(filename, index_col=0)

            await scrape(url)

            await asyncio.sleep(1)

        except Exception as err:
            print(err)


async def scrape(url):
    global day, query_date

    response = requests.get(url, headers={"User-Agent": "XY"}).text

    test = [m.start() for m in re.finditer("24h Fwd Return: ", response)]

    print(test)

    high_time_frame_index = response.find("High Time Frame")
    print("High Time Frame", high_time_frame_index)

    low_time_frame_index = response.find("Low Time Frame")
    print("Low Time Frame", low_time_frame_index)

    high_time_frame_predictions = []
    low_time_frame_predictions = []

    for index in test:
        value_start_index = index + len("24h Fwd Return: ")
        value_end_index = value_start_index + response[
            value_start_index : value_start_index + 8
        ].find("%")

        prediction = response[value_start_index:value_end_index]

        if value_start_index > low_time_frame_index:
            low_time_frame_predictions.append(prediction)
        else:
            high_time_frame_predictions.append(prediction)

        print("index", index, response[value_start_index:value_end_index])

    print(high_time_frame_predictions)
    print(low_time_frame_predictions)

    previous_day_close_price_start_index = (
        response.find('"Prev Close",') + len('"Prev Close",') + 1
    )
    previous_day_close_price_end_index = previous_day_close_price_start_index + 8

    last_day_close_price = response[
        previous_day_close_price_start_index:previous_day_close_price_end_index
    ]

    print(last_day_close_price)

    save_scraped_data(
        [
            query_date,
            high_time_frame_predictions,
            low_time_frame_predictions,
            last_day_close_price,
        ]
    )
    decrement_date()


def save_scraped_data(new_record):
    global df

    headers = [
        "date",
        "high_time_frame_predictions",
        "low_time_frame_predictions",
        "last_day_close",
    ]
    new_record_df = pd.DataFrame([new_record], columns=headers)
    new_df = df.append(new_record_df, ignore_index=True)

    print("df", new_df)

    new_df.to_csv(filename)


def decrement_date():
    global day

    one_day = datetime.timedelta(1)

    day = day - one_day


while True:
    asyncio.run(loop())
