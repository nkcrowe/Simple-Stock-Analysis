import streamlit as st
import data
import analysis

st.title("Stock Analysis")
st.write("Analyze any stock's performance over the last 5 years.")

# ── Sidebar: stock list and interval ─────────────────────────────────────────

with st.sidebar:
    st.header("Portfolio Setup")

    use_sample = st.checkbox("Use sample portfolio")
    if use_sample:
        ticker_list = ["^GSPC", "AAPL", "NVDA", "TSLA", "NFLX", "PFE", "BAC", "MSFT", "GOOGL", "DIS"]
        st.caption("Note: ^GSPC is the ticker for the S&P 500")
    else:
        raw = st.text_input("Enter tickers (comma-separated)", "AAPL, MSFT, GOOGL")
        ticker_list = sorted([t.strip().upper() for t in raw.split(",") if t.strip()])

    st.write("Current stock list:", ticker_list)

    time_interval = st.selectbox("Time interval", ["1d", "1wk", "1mo", "3mo"])

# ── Menu ──────────────────────────────────────────────────────────────────────

action_label = st.radio("Select an action", [
    "1. View stock list",
    "2. Analyze a single stock",
    "3. Compare two stocks",
    "4. Time interval analysis",
    "5. View portfolio summary",
    "6. Save an analysis report",
])
action = int(action_label[0])   # pull the number off the front of the label

# ── Action 1: View stock list ─────────────────────────────────────────────────

if action == 1:
    st.subheader("Current Stock List")
    st.write(ticker_list)

# ── Action 2: Analyze a single stock ─────────────────────────────────────────

elif action == 2:
    st.subheader("Single Stock Analysis")

    chosen = st.selectbox("Choose a stock to analyze", ticker_list)
    analysis_list = [chosen]

    if st.button("Run Analysis"):
        with st.spinner("Stock Data Loading..."):
            stocks = data.create_csv(analysis_list, time_interval)
            prices = analysis.stock_data(stocks, analysis_list)

        analysis.price_plot(analysis_list, prices, time_interval, action=3, final_start_date="")

        total_return, return_list, volatility = analysis.return_and_volatility(prices, analysis_list)
        st.write(f"**{analysis_list[0]} data**")
        st.write("---")
        st.write("Returns:", total_return[0] + "%")
        st.write("Volatility:", volatility[0] + "%")

# ── Action 3: Compare two stocks ──────────────────────────────────────────────

elif action == 3:
    st.subheader("Compare Two Stocks")

    if len(ticker_list) < 2:
        st.warning("Add at least 2 stocks to your portfolio to use this option.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            stock_a = st.selectbox("First stock",  ticker_list, index=0)
        with col2:
            stock_b = st.selectbox("Second stock", ticker_list, index=1)
        analysis_list = sorted([stock_a, stock_b])

        if st.button("Run Comparison"):
            with st.spinner("Stock Data Loading..."):
                stocks = data.create_csv(analysis_list, time_interval)
                prices = analysis.stock_data(stocks, analysis_list)

            analysis.price_plot(analysis_list, prices, time_interval, action=4, final_start_date="")

            for i in range(2):
                total_return, return_list, volatility = analysis.return_and_volatility(prices, analysis_list)
                st.write(f"**{analysis_list[i]} data**")
                st.write("---")
                st.write("Returns:", total_return[i] + "%")
                st.write("Volatility:", volatility[i] + "%")

# ── Action 4: Time interval analysis ─────────────────────────────────────────

elif action == 4:
    st.subheader("Time Interval Analysis")

    if time_interval == "3mo":
        st.caption("Due to time interval, available months are: 01, 04, 07, 10")
    st.caption("Available years: 2020, 2021, 2022, 2023, 2024, 2025")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.text_input("Start date (year-mm)", "2022-01")
    with col2:
        end_date = st.text_input("End date (year-mm)", "2024-01")

    chosen = st.selectbox("Choose a stock to analyze", ticker_list)
    analysis_list = [chosen]

    if st.button("Run Analysis"):
        with st.spinner("Loading interval data..."):
            stocks_interval, final_start_date, final_end_date = data.date_range(
                time_interval, ticker_list, start_date, end_date
            )
            prices = analysis.stock_data(stocks_interval, ticker_list)

        st.write("Time interval updated")
        analysis.price_plot(analysis_list, prices, time_interval, action=5, final_start_date=final_start_date)

        total_return, return_list, volatility = analysis.return_and_volatility(prices, analysis_list)
        st.write(f"**{analysis_list[0]} data from {final_start_date} to {final_end_date}**")
        st.write("---")
        st.write("Returns:", total_return[0] + "%")
        st.write("Volatility:", volatility[0] + "%")

# ── Action 5: Portfolio summary ───────────────────────────────────────────────

elif action == 5:
    st.subheader("Portfolio Summary")

    if st.button("Load Summary"):
        with st.spinner("Stock Data Loading..."):
            stocks = data.create_csv(ticker_list, time_interval)
            prices = analysis.stock_data(stocks, ticker_list)
            report = analysis.stock_analysis(prices, ticker_list, time_interval)

        st.text(report)   # preserves your fixed-width formatting

# ── Action 6: Save report ─────────────────────────────────────────────────────

elif action == 6:
    st.subheader("Save Analysis Report")

    if st.button("Generate Report"):
        with st.spinner("Stock Data Loading..."):
            report_text = data.save(ticker_list, time_interval)

        st.download_button(
            label="Download report as .txt",
            data=report_text,
            file_name="stock_report.txt",
            mime="text/plain",
        )