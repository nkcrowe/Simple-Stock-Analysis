import matplotlib.pyplot as plt
import numpy as np

def stock_data(stocks, analysis_list):
    #create dictionary, key = ticker, value = list of open prices in date order
    prices = {}
    for i in analysis_list: #run through for each stock we are analyzing
        price = list(stocks["Open"][i])
        prices[i] = price
    return prices

def return_and_volatility(prices, analysis_list):
    #core data analysis, ran for each stock in analysis list
    return_list = []
    total_return = []

    #periodic return
    for ticker in analysis_list:
        series = prices[ticker]
        returns = []
        for p in range(len(series) - 1):
            r = ((series[p + 1] / series[p]) - 1) * 100
            returns.append(r)
        return_list.append(returns)

    #5yr-return
    for ticker in analysis_list:
        series = prices[ticker]
        calc = ((series[-1] / series[0]) - 1) * 100
        total_return.append(str(calc)[:7])

    #volatility per stock
    volatility = []
    for returns in return_list:
        r = np.array(returns)
        mean_r = r.mean()
        var = ((r - mean_r) ** 2).sum() / (len(r) - 1)
        std = var ** 0.5
        volatility.append(str(std)[:7])

    return total_return, return_list, volatility

def stock_analysis(prices, analysis_list, time_interval):
    total_return, return_list, volatility = return_and_volatility(prices, analysis_list)

    report = "" #reset report variable

    header = ("Stocks   |   Current Price   |   2020-01-01 Price   |   Return Over Last "
        + str(time_interval)
        + "   |   5 yr Return to Date   |   Volatility\n")

    separator = "-" * 120 + "\n"

    report = report + header
    report = report + separator

    for i in range(len(analysis_list)):
        ticker = analysis_list[i]

        #get all data for single stock
        current_price = "$" + str(prices[ticker][-1])[:7]
        start_price = "$" + str(prices[ticker][0])[:7]
        last_return = str(return_list[i][-1])[:7] + "%"
        five_year = total_return[i] + "%"
        vol = volatility[i] + "%"

        #write full line for single stock
        line = (
            ticker + " " * (16 - len(ticker)) +
            current_price + " " * (21 - len(current_price)) +
            start_price + " " * (25 - len(start_price)) +
            last_return + " " * (26 - len(last_return)) +
            five_year + " " * (22 - len(five_year)) +
            vol + "\n")

        report = report + line

    return report


def price_plot(analysis_list, prices, time_interval, action, start_date):
    import streamlit as st
    #create graph(s) of price data over time
    for i in range(len(analysis_list)):
        fig, ax = plt.subplots()
        ax.plot(prices[analysis_list[i]])
        ax.set_title(analysis_list[i] + " Stock Price")

        #single or double stock analysis
        if action == 3 or action == 4:
            if time_interval == "1d":
                ax.set_xlabel("Days since " + start_date)
            elif time_interval == "1wk":
                ax.set_xlabel("Weeks since " + start_date)
            elif time_interval == "1mo":
                ax.set_xlabel("Months since " + start_date)
            else:
                ax.set_xlabel("Quarters since " + start_date)

        #change x label if doing time interval analysis
        elif action == 5:
            if time_interval == "1d":
                ax.set_xlabel("Days since " + start_date)
            elif time_interval == "1wk":
                ax.set_xlabel("Weeks since " + start_date)
            elif time_interval == "1mo":
                ax.set_xlabel("Months since " + start_date)
            else:
                ax.set_xlabel("Quarters since " + start_date)

        ax.set_ylabel("Stock Price ($)")
        st.pyplot(fig)
        plt.close(fig)