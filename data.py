import yfinance as yf
import analysis

def dates(time_interval):
    #create list of dates based on time interval selected, used to verify user input in time interval analysis
    if time_interval == "1d":
        time_list = day_dates()
    elif time_interval == "1wk":
        time_list = week_dates()
    elif time_interval == "1mo":
        time_list = month_dates()
    elif time_interval == "3mo":
        time_list = quarter_dates()

    return time_list

def day_dates():
    #create list of all dates in 5 year range of stock data
    time_list = []
    for y in range(0, 5):  #first 4 years
        for m in range(1, 32):  # jan
            time_list.append("202" + str(y) + "-01-" + str(m))
        for m in range(1, 29):  # feb (skip leap days)
            time_list.append("202" + str(y) + "-02-" + str(m))
        for m in range(1, 32):  # mar
            time_list.append("202" + str(y) + "-03-" + str(m))
        for m in range(1, 31):  # apr
            time_list.append("202" + str(y) + "-04-" + str(m))
        for m in range(1, 32):  # may
            time_list.append("202" + str(y) + "-05-" + str(m))
        for m in range(1, 31):  # jun
            time_list.append("202" + str(y) + "-06-" + str(m))
        for m in range(1, 32):  # jul
            time_list.append("202" + str(y) + "-07-" + str(m))
        for m in range(1, 32):  # aug
            time_list.append("202" + str(y) + "-08-" + str(m))
        for m in range(1, 31):  # sep
            time_list.append("202" + str(y) + "-09-" + str(m))
        for m in range(1, 32):  # oct
            time_list.append("202" + str(y) + "-10-" + str(m))
        for m in range(1, 31):  # nov
            time_list.append("202" + str(y) + "-11-" + str(m))
        for m in range(1, 32):  # dec
            time_list.append("202" + str(y) + "-12-" + str(m))

    for y in range(5, 6):  #year 5 until 2025-11-28 (where stock data ends)
        for m in range(1, 32):  # jan
            time_list.append("202" + str(y) + "-01-" + str(m))
        for m in range(1, 29):  # feb (skip leap days)
            time_list.append("202" + str(y) + "-02-" + str(m))
        for m in range(1, 32):  # mar
            time_list.append("202" + str(y) + "-03-" + str(m))
        for m in range(1, 31):  # apr
            time_list.append("202" + str(y) + "-04-" + str(m))
        for m in range(1, 32):  # may
            time_list.append("202" + str(y) + "-05-" + str(m))
        for m in range(1, 31):  # jun
            time_list.append("202" + str(y) + "-06-" + str(m))
        for m in range(1, 32):  # jul
            time_list.append("202" + str(y) + "-07-" + str(m))
        for m in range(1, 32):  # aug
            time_list.append("202" + str(y) + "-08-" + str(m))
        for m in range(1, 31):  # sep
            time_list.append("202" + str(y) + "-09-" + str(m))
        for m in range(1, 32):  # oct
            time_list.append("202" + str(y) + "-10-" + str(m))
        for m in range(1, 29):  # nov
            time_list.append("202" + str(y) + "-11-" + str(m))
    return time_list

def week_dates():
    # create list of all dates by week in 5 year range of stock data
    time_list = []
    year = 2020
    month = 1
    mplace = 0
    day = 1
    dplace = 0

    while year != 2025 or mplace != 1 or month != 2:
        time_list.append(str(year) + "-" + str(mplace) + str(month) + "-" + str(dplace) + str(day))
        day += 7

        if day > 9:
            dplace += 1
            day -= 10

        if ((mplace == 0 and month == 1) or month == 3 or month == 5 or month == 7 or month == 8 or (
                mplace == 1 and month == 0)) and ((dplace == 3 and day > 1) or dplace >= 4):
            month += 1
            dplace = 0
            day -= 1

        elif (mplace == 1 and month == 2) and ((dplace == 3 and day > 1) or dplace >= 4):
            mplace = 0
            month = 1
            dplace = 0
            day -= 1
            year += 1

        elif (month == 4 or month == 6 or (mplace == 1 and month == 1)) and (
                (dplace == 3 and day > 0) or dplace >= 4):
            month += 1
            dplace = 0

        elif month == 9 and ((dplace == 3 and day > 0) or dplace >= 4):
            mplace = 1
            month = 0
            dplace = 0

        elif (mplace == 0 and month == 2) and (year == 2020 or year == 2024) and (
                (dplace == 2 and day > 9) or (dplace >= 3)):
            month += 1
            dplace = 0
            day += 1

        elif (mplace == 0 and month == 2) and (year == 2021 or year == 2022 or year == 2023) and (
                (dplace == 2 and day > 8) or (dplace >= 3)):
            month += 1
            dplace = 0
            day += 2

        elif (mplace == 0 and month == 2) and year == 2025 and ((dplace == 2 and day > 8) or (dplace >= 3)):
            month += 1
            dplace = 0
            day += 2

        if day > 9:
            day -= 10

    return time_list

def month_dates():
    # create list of all dates by month in 5 year range of stock data
    time_list = []
    for y in range(0, 6):
        for m in range(1, 10):
            time_list.append("202" + str(y) + "-0" + str(m) + "-01")
        for m in range(10, 13):
            time_list.append("202" + str(y) + "-" + str(m) + "-01")
    time_list.pop()

    return time_list

def quarter_dates():
    # create list of all dates by quarter in 5 year range of stock data
    time_list = []
    for y in range(0, 6):
        for m in range(1, 8, 3):
            time_list.append("202" + str(y) + "-0" + str(m) + "-01")
        time_list.append("202" + str(y) + "-10-01")

    return time_list

def create_csv(analysis_list, time_interval):
    #create stock data csv
    stocks = yf.download(analysis_list, start="2020-01-01", end="2025-12-01", interval=time_interval, auto_adjust=True, progress=False)
    return stocks

def date_range(time_interval, analysis_list, start_date, end_date):
    # updated signature: accepts start_date and end_date strings from Streamlit
    # instead of prompting the user via input()
    time_list = dates(time_interval)

    final_start_date = start_date
    final_end_date = end_date

    if time_interval == "1wk":
        day = ["-01", "-02", "-03", "-04", "-05", "-06", "-07"]
        for s in range(len(time_list)):
            for i in range(len(day)):
                if start_date + day[i] == time_list[s]:
                    final_start_date = start_date + day[i]
                if end_date + day[i] == time_list[s]:
                    final_end_date = end_date + day[i]
    else:
        final_start_date = start_date + "-01"
        final_end_date = end_date + "-01"

    stocks_interval = yf.download(analysis_list, start=final_start_date, end=final_end_date, interval=time_interval, auto_adjust=True, progress=False)

    return stocks_interval, final_start_date, final_end_date


def save(ticker_list, time_interval):
    # returns report text as a string for Streamlit's download button
    # instead of writing to a file directly
    stocks = create_csv(ticker_list, time_interval)
    prices = analysis.stock_data(stocks, ticker_list)
    report_text = analysis.stock_analysis(prices, ticker_list, time_interval)
    return report_text