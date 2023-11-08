import pandas as pd
import streamlit as st
import base64

# Read the trade log data from the CSV file
trade_log = pd.read_csv("tradelog.csv")

# Calculate the parameters
initial_portfolio_value = 6500
risk_free_rate = 0.05

# Total Trades
total_trades = len(trade_log)

# Profitable Trades
profitable_trades = len(trade_log[trade_log['Exit Price'] > trade_log['Entry Price']])

# Loss-Making Trades
loss_making_trades = total_trades - profitable_trades

# Win Rate
win_rate = profitable_trades / total_trades

# Average Profit per trade
average_profit_per_trade = (trade_log['Exit Price'] - trade_log['Entry Price']).where(trade_log['Exit Price'] > trade_log['Entry Price']).mean()

# Average Loss per trade
average_loss_per_trade = (trade_log['Exit Price'] - trade_log['Entry Price']).where(trade_log['Exit Price'] < trade_log['Entry Price']).mean()

# Risk Reward ratio
risk_reward_ratio = average_profit_per_trade / average_loss_per_trade

# Expectancy
loss_rate = 1 - win_rate
expectancy = (win_rate * average_profit_per_trade) - (loss_rate * average_loss_per_trade)

# Average Rate of Return (ROR) per trade
rate_of_return = ((trade_log['Exit Price'] - trade_log['Entry Price']) / trade_log['Entry Price']).mean()

# Sharpe Ratio
trade_log['Returns'] = (trade_log['Exit Price'] - trade_log['Entry Price']) / trade_log['Entry Price']
sharpe_ratio = (rate_of_return - risk_free_rate) / trade_log['Returns'].std()

# Max Drawdown
cumulative_returns = (1 + trade_log['Returns']).cumprod()
peak = cumulative_returns.expanding().max()
drawdown = (cumulative_returns - peak) / peak
max_drawdown = drawdown.min()

# Max Drawdown Percentage
max_drawdown_percentage = max_drawdown * 100

# CAGR (Compound Annual Growth Rate)
ending_value = initial_portfolio_value + (initial_portfolio_value * rate_of_return)
beginning_value = initial_portfolio_value
number_of_periods = total_trades
cagr = (ending_value / beginning_value) ** (1 / number_of_periods) - 1

# Calmar Ratio
calmar_ratio = cagr / max_drawdown_percentage

# Create a Streamlit app
st.title("Stock Market Analysis")

# Display the results using Streamlit
st.write("Analysis Results:")
st.write("Total Trades:", total_trades)
st.write("Profitable Trades:", profitable_trades)
st.write("Loss-Making Trades:", loss_making_trades)
st.write("Win Rate:", win_rate)
st.write("Average Profit per Trade:", average_profit_per_trade)
st.write("Average Loss per Trade:", average_loss_per_trade)
st.write("Risk Reward Ratio:", risk_reward_ratio)
st.write("Expectancy:", expectancy)
st.write("Average ROR per Trade:", rate_of_return)
st.write("Sharpe Ratio:", sharpe_ratio)
st.write("Max Drawdown:", max_drawdown)
st.write("Max Drawdown Percentage:", max_drawdown_percentage)
st.write("CAGR:", cagr)
st.write("Calmar Ratio:", calmar_ratio)

results = pd.DataFrame({
    'Parameter': ['Total Trades', 'Profitable Trades', 'Loss-Making Trades', 'Win Rate',
                  'Average Profit per Trade', 'Average Loss per Trade', 'Risk Reward Ratio',
                  'Expectancy', 'Average ROR per Trade', 'Sharpe Ratio', 'Max Drawdown',
                  'Max Drawdown Percentage', 'CAGR', 'Calmar Ratio'],
    'Value': [total_trades, profitable_trades, loss_making_trades, win_rate,
              average_profit_per_trade, average_loss_per_trade, risk_reward_ratio,
              expectancy, rate_of_return, sharpe_ratio, max_drawdown, max_drawdown_percentage,
              cagr, calmar_ratio]
})
# Save to CSV
csv = results.to_csv(index=False)
st.download_button("Download CSV file",
                   csv,
                   file_name='output.csv',
                   mime='text/csv')