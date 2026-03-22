def main():
    import data
    import analysis

    print("Welcome to Stock Analysis!")
    print("You can analyze any stock's performance over the last 5 years.\n")

    #create initial stock list and time interval
    ticker_list = data.choose_stocks()
    time_interval = data.choose_interval()

    #menu and user selection
    action = menu()
    while action != 8: #enter 8 to exit code
        if action == 1: #view stock list
            data.stock_list(ticker_list)

        elif action == 2: #edit stock list and time interval
            ticker_list = data.edit_stocks(ticker_list)
            time_interval = data.choose_interval()
            data.stock_list(ticker_list)

        elif action == 3: #analyze single stock
            data.stock_list(ticker_list) #show stock list
            analysis_list = analysis.choose_single_stock(ticker_list) #user chooses stock to analyze
            if len(analysis_list) < 1: #if stock list is empty, choose stock to add and analyze
                add = input("Enter stock to analyze: ").strip().upper()
                analysis_list.append(add)

            print("\nStock Data Loading...")
            stocks = data.create_csv(analysis_list, time_interval) #load stock data
            prices = analysis.stock_data(stocks, analysis_list) #place open prices into dictionary, key = stock ticker
            analysis.price_plot(analysis_list, prices, time_interval, action, final_start_date = "") #plot prices

            total_return, return_list, volatility = analysis.return_and_volatility(prices, analysis_list) #returns and volatility for stock
            print(analysis_list[0], "data")
            print("–" * 20)
            print("Returns:", total_return[0] + "%",  # need this for single and double function too
                  "\nVolatility:", volatility[0] + "%\n")
            go_back = ""
            while go_back != "back": #wait until user enters back to return to menu
                go_back = input("\nEnter \"back\" to return to menu: ").strip().lower()

        elif action == 4: #compare two stocks
            data.stock_list(ticker_list) #show stock list
            analysis_list = analysis.choose_two_stocks(ticker_list) #user chooses 2 stocks from stock list
            if len(analysis_list) < 2: #if only 1 stock in stock list, enter second to compare to
                add = input("Enter stock to compare to: ").strip().upper()
                analysis_list.append(add)

            print("\nStock Data Loading...")
            stocks = data.create_csv(analysis_list, time_interval) #download stock data
            prices = analysis.stock_data(stocks, analysis_list) #create dictionary of open prices, key = stock ticker
            analysis.price_plot(analysis_list, prices, time_interval, action, final_start_date = "") #price plot of each stock

            for i in range(0, 2): #return and volatility of each stock
                total_return, return_list, volatility = analysis.return_and_volatility(prices, analysis_list)
                print(analysis_list[i], "data")
                print("–"*20)
                print("Returns:", total_return[i] + "%",  # need this for single and double function too
                      "\nVolatility:", volatility[i] + "%\n")
            go_back = ""
            while go_back != "back": #wait until user enters back to return to menu
                go_back = input("\nEnter \"back\" to return to menu: ").strip().lower()

        elif action == 5: #look at stock in more specific time interval
            stocks_interval, final_start_date, final_end_date = data.date_range(time_interval, ticker_list) #user chooses new start and end dates
            print("\nTime interval updated")
            user_input = ""
            user_input = input("Enter stock to analyze (enter back to return to menu): ").strip().upper() #user chooses stock to look at
            while user_input != "BACK":

                while user_input not in ticker_list: #make sure user enters stock in their stock list
                    data.stock_list(ticker_list)
                    user_input = input("Enter valid stock to analyze (enter back to return to menu): ").strip().upper()

                analysis_list = [user_input]
                prices = analysis.stock_data(stocks_interval, ticker_list) #download open price data
                analysis.price_plot(analysis_list, prices, time_interval, action, final_start_date) #price plot

                #individual stock return and volatility analysis
                total_return, return_list, volatility = analysis.return_and_volatility(prices, analysis_list)

                print(analysis_list[0], "data from " + final_start_date + " to " + final_end_date)
                print("Returns:", total_return[0] + "%", #need this for single and double function too
                    "\nVolatility:", volatility[0] + "%\n")

                user_input = input("Enter stock to analyze (enter back to return to menu): ").strip().upper() #allow user to look at another stock or return to menu



        elif action == 6: #portfolio summary
            print("\nStock Data Loading...")
            stocks = data.create_csv(ticker_list, time_interval) #download data of entire stock list
            prices = analysis.stock_data(stocks, ticker_list) #create dictionary of open prices
            report = analysis.stock_analysis(prices, ticker_list, time_interval) #combine data into str to print
            print(report)

            go_back = ""
            while go_back != "back": #wait until user enters back to return to menu
                go_back = input("\nEnter \"back\" to return to menu: ").strip().lower()

        elif action == 7: #save file
            data.save(data, ticker_list, time_interval) #file only appears when code run finishes?

        action = menu() #back to menu until user enters 8



def menu():
    #menu for user action
    action = 0
    while action < 1 or action > 8:
        print("\nMake selection from options below: ",
                           "1.  View stock list",
                           "2.  Edit stock list/time interval",
                           "3.  Analyze a single stock",
                           "4.  Compare two stocks",
                           "5.  Time interval analysis",
                           "6.  View portfolio summary",
                           "7.  Save an analysis report to a file",
                           "8.  Exit\n", sep = "\n")

        action = input().strip() #make sure input is number
        while not action.isdigit():
            print("Invalid selection, please enter a number 1-8")
            action = input()

        action = int(action)

        if int(action) < 1 or int(action) > 8: #make sure input is between 1-8
            print("Invalid selection, please enter a number 1-8")

    return int(action)

if __name__ == "__main__":
    main()