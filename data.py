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
def choose_stocks():
    #initial stock selection
    ticker_list = []
    user_input = ""
    print("Enter stock tickers one at a time (input \"done\" when finished):")
    print("eg.) Apple = AAPL, Google = GOOGL, Microsoft = MSFT")
    print("Enter \"sample\" to use sample portfolio")

    while user_input != "DONE" and user_input != "SAMPLE": #user can add until they enter done
        user_input = input().strip().upper()
        ticker_list.append(user_input)
        if user_input == "DONE": #remove done input
            ticker_list.remove("DONE")

    if user_input == "SAMPLE": #preset sample stock list
        ticker_list = ["^GSPC", "AAPL", "NVDA", "TSLA", "NFLX", "PFE", "BAC", "MSFT", "GOOGL", "DIS"]
        note = "Note: [^GSPC] is the ticker for the S&P 500"
    else:
        note = ""
    ticker_list.sort()
    print("Your current stock list is:", ticker_list)
    print(note)

    return ticker_list

def choose_interval():
    #choose time interval for stock data
    time_interval = input("Enter time interval for data (1d, 1wk, 1mo, 3mo): ").strip()
    while time_interval != "1d" and time_interval != "1wk" and time_interval != "1mo" and time_interval != "3mo": #verify user input
        time_interval = input("Enter valid time interval (1d, 1wk, 1mo, 3mo): ")

    return time_interval

def create_csv(analysis_list, time_interval):
    #create stock data csv
    stocks = yf.download(analysis_list, start="2020-01-01", end="2025-12-01", interval = time_interval, auto_adjust = True)

    return stocks

def edit_stocks(ticker_list):
    #edit stock list
    user_input = ""

    print("Enter stock tickers one at a time to add/remove (input \"done\" when finished):")
    while user_input != "DONE":
        user_input = input().strip().upper()

        if user_input in ticker_list:
            ticker_list.remove(user_input)
        else:
            ticker_list.append(user_input)

        if user_input == "DONE":
            ticker_list.remove("DONE")

    ticker_list.sort()

    return ticker_list

def stock_list(ticker_list):
    #print current stock list
    print("Current stocks:")
    print(ticker_list)

def date_range(time_interval, analysis_list):
    #create new date range for time interval analysis
    time_list = dates(time_interval)

    print("Let's look at a more specific interval within the last 5 years")
    if time_interval == "3mo":
        print("Due to time interval available months are: 01, 04, 07, 10")
    print("available years are: 2020, 2021, 2022, 2023, 2024, 2025")

    #starting date – user enters year and month
    #not every day is in the date range especially if using weekly interval so don't have user choose day
    start_date = input("Enter start date (year-mm): ")
    if time_interval == "1wk": #if time interval is week, not every month date will start on the first
        day = ["-01", "-02", "-03", "-04", "-05", "-06", "-07"]
        for s in range(len(time_list)):
            for i in range(len(day)):
                if start_date + day[i] == time_list[s]:
                    final_start_date = start_date + day[i]
    else:
        final_start_date = start_date + "-01" #for daily, monthly, quarterly interval every available month starts on the first

    #ending date – same method as start day
    end_date = input("Enter end date (year-mm): ")
    if time_interval == "1wk":
        day = ["-01", "-02", "-03", "-04", "-05", "-06", "-07"]
        for s in range(len(time_list)):
            for i in range(len(day)):
                if start_date + day[i] == time_list[s]:
                    final_end_date = end_date + day[i]
    else:
        final_end_date = end_date + "-01"

    stocks_interval = yf.download(analysis_list, start=final_start_date, end=final_end_date, interval=time_interval, auto_adjust=True) #new stock data with new date interval

    return stocks_interval, final_start_date, final_end_date


def save(data, ticker_list, time_interval):
    print("\nStock Data Loading...")

    stocks = data.create_csv(ticker_list, time_interval)
    prices = analysis.stock_data(stocks, ticker_list)

    report_text = analysis.stock_analysis(prices, ticker_list, time_interval) #create full stock data report

    name = input("Enter name for file: ")

    file = open(name + ".txt", "w")
    file.write(report_text) #write report to data file
    file.close()

    print("Saved analysis report to", name + ".txt")