import streamlit as st
import pandas as pd
import numpy as np
import capm_functions
import yfinance as yf
import datetime
import pandas_datareader.data  as web 


st.set_page_config(page_title="CAPM Return", 
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded")


st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: white;
    }
    h1, h2, h3, h4, h5, h6, p, div {
        color: white !important;
    }
    .css-1d391kg, .css-1n76uvr, .css-1cpxqw2 {
        background-color: #1c1c1c !important;
        color: white !important;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
    }
    .css-1wa3eu0-placeholder {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)



st.title("CAPM Return Calculator / Captial Asset Pricing Model")
col1,col2 = st.columns([1,1])
with col1:
    stocks_list = st.multiselect("Choose 4 stocks:", ["TSLA", "AAPL", "MSFT", "GOOGL", "NFLX", "AMZN", "NVDA"], default=["TSLA", "AAPL", "AMZN", "GOOGL"])
with col2:
    year = st.number_input("Number of years:", 1, 10)
end = datetime.datetime.today()
start = datetime.date(datetime.date.today().year - year, datetime.date.today().month, datetime.date.today().day)
# loading data for sp500
sp500 = web.DataReader(['sp500'], 'fred', start, end)

# loading data for stocks only Close price
stocks_df = pd.DataFrame()
for stock in stocks_list:
    data = yf.download(stock, period=f'{year}y')
    stocks_df[stock] = data['Close']
stocks_df.reset_index(inplace=True) 
sp500.reset_index(inplace=True)
sp500.rename(columns={'DATE': 'Date'}, inplace=True)

# merge dataframes
df = pd.merge(stocks_df, sp500, how='inner', on='Date')
# df.set_index('Date', inplace=True)
# df.dropna(inplace=True)
df['Date'] = pd.to_datetime(df['Date']).dt.date
col1,col2 = st.columns([1,1])
with col1:
    st.markdown("### Data Frame Head")
    st.dataframe(df.head(),use_container_width=True)
    
with col2:
    st.markdown("### Data Frame Tail")
    st.dataframe(df.tail(),use_container_width=True)

col1,col2 = st.columns([1,1])
with col1:
    st.markdown("### Closing Price of All Stocks")
    st.plotly_chart(capm_functions.interactive_plot(df),use_container_width=True)
    
with col2:
    st.markdown("### NormalizedClosing Price of All Stocks")
    normalized_df = capm_functions.normalize(df)
    st.plotly_chart(capm_functions.interactive_plot(normalized_df),use_container_width=True)

stocks_daily_return_df = capm_functions.daily_return(df)
normalized_stocks_daily_return_df = capm_functions.daily_return(normalized_df)

col1,col2 = st.columns([1,1])
with col1:
    st.markdown("### Daily Return of All Stocks")
    st.plotly_chart(capm_functions.interactive_plot(stocks_daily_return_df),use_container_width=True)
    
with col2:
    st.markdown("### Normalized Daily Return of All Stocks")
    st.plotly_chart(capm_functions.interactive_plot(normalized_stocks_daily_return_df),use_container_width=True)
beta = {}
alpha = {}
   
for i in stocks_daily_return_df.columns:
    if i != 'Date' and i != 'sp500':
        b,a = capm_functions.calculate_beta(stocks_daily_return_df,i)
        beta[i] = b
        alpha[i] = a    
print(beta,alpha)

beta_df = pd.DataFrame(columns=['Stocks', 'Beta_values'])
beta_df['Stocks'] = beta.keys()
beta_df['Beta_values'] =[ str(round(i,2)) for i in beta.values()]

alpha_df = pd.DataFrame(columns=['Stocks', 'Alpha_values'])
alpha_df['Stocks'] = alpha.keys()
alpha_df['Alpha_values'] = [ str(round(i,2)) for i in alpha.values()]

col1,col2 = st.columns([1,1])
with col1:
    st.markdown("### Calculated Beta Values")
    st.dataframe(beta_df,use_container_width=True)
    

# risk free rate = 0
rf = 0
rm  = stocks_daily_return_df['sp500'].mean()*252
return_df = pd.DataFrame(columns=['Stocks', 'Return_values'])
return_values = []
for stock,value in beta.items():
    return_values.append(str(round(rf+ (value * (rm - rf)),2)))
return_df['Stocks'] = stocks_list
return_df['Return_values'] = return_values

with col2:
    st.markdown("### Calculated Return Values Using CAPM")
    st.dataframe(return_df,use_container_width=True)