import math
from datetime import date, timedelta

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Simple Stock Analysis", page_icon="📈", layout="wide")


def parse_tickers(raw: str) -> list[str]:
    tickers = []
    for item in raw.replace("\n", ",").split(","):
        ticker = item.strip().upper()
        if ticker and ticker not in tickers:
            tickers.append(ticker)
    return tickers


@st.cache_data(show_spinner=False, ttl=3600)
def load_prices(tickers: list[str], start_date: date, end_date: date, interval: str) -> pd.DataFrame:
    if not tickers:
        return pd.DataFrame()

    data = yf.download(
        tickers,
        start=start_date,
        end=end_date + timedelta(days=1),
        interval=interval,
        auto_adjust=True,
        progress=False,
        group_by="column",
    )

    if data.empty:
        return pd.DataFrame()

    close = data.get("Close")
    if close is None:
        return pd.DataFrame()

    if isinstance(close, pd.Series):
        close = close.to_frame(name=tickers[0])

    close = close.dropna(how="all").copy()
    close = close.sort_index()
    close.columns = [str(c).upper() for c in close.columns]
    return close


def compute_summary(prices: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for ticker in prices.columns:
        series = prices[ticker].dropna()
        if len(series) < 2:
            continue

        returns = series.pct_change().dropna()
        total_return = (series.iloc[-1] / series.iloc[0] - 1) * 100
        volatility = returns.std(ddof=1) * 100
        avg_return = returns.mean() * 100

        rows.append(
            {
                "Ticker": ticker,
                "Start Price": round(float(series.iloc[0]), 2),
                "Current Price": round(float(series.iloc[-1]), 2),
                "Total Return %": round(float(total_return), 2),
                "Avg Period Return %": round(float(avg_return), 2),
                "Volatility %": round(float(volatility), 2),
                "Data Points": int(series.shape[0]),
            }
        )

    if not rows:
        return pd.DataFrame()

    summary = pd.DataFrame(rows).sort_values("Total Return %", ascending=False).reset_index(drop=True)
    return summary


def normalized_prices(prices: pd.DataFrame) -> pd.DataFrame:
    normed = prices.copy()
    for col in normed.columns:
        series = normed[col].dropna()
        if not series.empty:
            normed[col] = normed[col] / series.iloc[0] * 100
    return normed


st.title("📈 Simple Stock Analysis")
st.caption("Interactive stock dashboard built with Streamlit and yfinance.")

with st.sidebar:
    st.header("Controls")
    ticker_input = st.text_area(
        "Tickers",
        value="AAPL, MSFT, NVDA",
        help="Enter one or more tickers separated by commas.",
        height=100,
    )
    interval = st.selectbox("Interval", ["1d", "1wk", "1mo", "3mo"], index=0)

    default_start = date.today() - timedelta(days=365 * 5)
    start_date = st.date_input("Start date", value=default_start)
    end_date = st.date_input("End date", value=date.today())

    analyze = st.button("Analyze", type="primary", use_container_width=True)

sample_portfolio = ["^GSPC", "AAPL", "NVDA", "TSLA", "NFLX", "PFE", "BAC", "MSFT", "GOOGL", "DIS"]
with st.expander("Quick start ideas"):
    st.write("Sample portfolio:", ", ".join(sample_portfolio))
    st.write("Try one ticker for a single-company view, or several to compare performance.")

if analyze:
    tickers = parse_tickers(ticker_input)

    if not tickers:
        st.error("Enter at least one valid ticker.")
        st.stop()

    if start_date >= end_date:
        st.error("Start date must be before end date.")
        st.stop()

    with st.spinner("Loading market data..."):
        prices = load_prices(tickers, start_date, end_date, interval)

    if prices.empty:
        st.error("No data returned. Check your ticker symbols, interval, or date range.")
        st.stop()

    summary = compute_summary(prices)

    st.subheader("Summary")
    if summary.empty:
        st.warning("Not enough data to compute summary metrics.")
    else:
        leader = summary.iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Best performer", leader["Ticker"])
        c2.metric("Top return", f"{leader['Total Return %']:.2f}%")
        c3.metric("Tickers analyzed", f"{len(summary)}")
        c4.metric("Interval", interval)

        display_summary = summary.copy()
        for col in ["Start Price", "Current Price"]:
            display_summary[col] = display_summary[col].map(lambda x: f"${x:,.2f}")
        for col in ["Total Return %", "Avg Period Return %", "Volatility %"]:
            display_summary[col] = display_summary[col].map(lambda x: f"{x:,.2f}%")

        st.dataframe(display_summary, use_container_width=True, hide_index=True)

    st.subheader("Price history")
    st.line_chart(prices, use_container_width=True)

    st.subheader("Normalized performance (starts at 100)")
    st.line_chart(normalized_prices(prices), use_container_width=True)

    daily_returns = prices.pct_change().dropna() * 100
    if not daily_returns.empty:
        st.subheader("Period returns (%)")
        st.line_chart(daily_returns, use_container_width=True)

    st.subheader("Latest prices")
    latest = prices.ffill().tail(15)
    st.dataframe(latest.style.format("${:,.2f}"), use_container_width=True)

    csv = prices.to_csv().encode("utf-8")
    st.download_button(
        "Download price data as CSV",
        data=csv,
        file_name="stock_prices.csv",
        mime="text/csv",
    )
else:
    st.info("Choose your tickers and settings, then click Analyze.")
