import yfinance as yf
import analysis
import datetime

def dates(time_interval, start_date, end_date):
    #create list of dates based on time interval selected, used to verify user input in time interval analysis
    if time_interval == "1d":
        time_list = day_dates(start_date, end_date)
    elif time_interval == "1wk":
        start_time_list = day_dates(start_date, end_date)
        time_list = [start_time_list[entry] for entry in range(0, len(start_time_list), 7)]
    elif time_interval == "1mo":
        start_time_list = day_dates(start_date, end_date)
        time_list = [start_time_list[entry] for entry in range(0, len(start_time_list)) if start_time_list[entry][8:] == "01"]
    # elif time_interval == "3mo":
    #     time_list = quarter_dates()

    return time_list

def day_dates(start_date, end_date):
    #create list of all dates in range of stock data
    start_year = start_date[:4]
    end_year = end_date[:4]
    end_month = end_date[5:7]
    end_day = end_date[8:10]

    time_list = []
    for y in range(int(start_year), int(end_year)):
        for m in range(1, 13):
            if m == 1 or m == 3 or m ==5 or m == 7 or m == 8:
                for d in range(1, 32):
                    time_list.append(str(y) + "-0" + str(m) + "-" + str(d))
            elif m == 10 or m == 12:
                for d in range(1, 32):
                    time_list.append(str(y) + "-" + str(m) + "-" + str(d))

            elif m == 4 or m == 6 or m == 9:
                for d in range(1, 31):
                    time_list.append(str(y) + "-0" + str(m) + "-" + str(d))
            elif m == 11:
                for d in range(1, 31):
                    time_list.append(str(y) + "-" + str(m) + "-" + str(d))

            else:
                if y % 4:
                    for d in range(1, 30):  #leap years
                        time_list.append(str(y) + "-02-" + str(d))
                else:
                    for d in range(1, 29):
                        time_list.append(str(y) + "-02-" + str(d))

        #end year
        for m in range(1, 13):
            if m < int(end_month):
                if m == 1 or m == 3 or m == 5 or m == 7 or m == 8:
                    for d in range(1, 32):
                        time_list.append(str(end_year) + "-0" + str(m) + "-" + str(d))
                elif m == 10 or m == 12:
                    for d in range(1, 32):
                        time_list.append(str(end_year) + "-" + str(m) + "-" + str(d))

                elif m == 4 or m == 6 or m == 9:
                    for d in range(1, 31):
                        time_list.append(str(end_year) + "-0" + str(m) + "-" + str(d))
                elif m == 11:
                    for d in range(1, 31):
                        time_list.append(str(end_year) + "-" + str(m) + "-" + str(d))

                else:
                    for d in range(1, 29):  # feb (skip leap days)
                        time_list.append(str(end_year) + "-02-" + str(d))


            if m == int(end_month):
                if m == 1 or m == 3 or m == 5 or m == 7 or m == 8:
                    for d in range(1, 32):
                        if d <= int(end_day):
                            time_list.append(str(end_year) + "-0" + str(m) + "-" + str(d))
                elif m == 10 or m == 12:
                    for d in range(1, 32):
                        if d <= int(end_day):
                            time_list.append(str(end_year) + "-" + str(m) + "-" + str(d))

                elif m == 4 or m == 6 or m == 9:
                    for d in range(1, 31):
                        if d <= int(end_day):
                            time_list.append(str(end_year) + "-0" + str(m) + "-" + str(d))
                elif m == 11:
                    for d in range(1, 31):
                        if d <= int(end_day):
                            time_list.append(str(end_year) + "-" + str(m) + "-" + str(d))

                else:
                    if y % 4 == 0:
                        for d in range(1, 30):  # leap years
                            if d <= int(end_day):
                                time_list.append(str(y) + "-02-" + str(d))
                    else:
                        for d in range(1, 29):
                            if d <= int(end_day):
                                time_list.append(str(y) + "-02-" + str(d))


    return time_list

# def quarter_dates():
#     # create list of all dates by quarter in 5 year range of stock data
#     time_list = []
#     for y in range(0, 6):
#         for m in range(1, 8, 3):
#             time_list.append("202" + str(y) + "-0" + str(m) + "-01")
#         time_list.append("202" + str(y) + "-10-01")
#
#     return time_list

def create_csv(analysis_list, time_interval, start_date):
    #create stock data csv
    stocks = yf.download(analysis_list, start=start_date, end=datetime.date.today(), interval=time_interval, auto_adjust=True, progress=False)
    return stocks

def date_range(time_interval, analysis_list, start_date, end_date):
    time_list = dates(time_interval, start_date, end_date)

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


def save(ticker_list, time_interval, start_date):
    # returns report text as a string for Streamlit's download button
    # instead of writing to a file directly
    stocks = create_csv(ticker_list, time_interval, start_date)
    prices = analysis.stock_data(stocks, ticker_list)
    report_text = analysis.stock_analysis(prices, ticker_list, time_interval)
    return report_text