import plotly.express as px
import numpy as np
import pandas as pd

# functions to plot interactive plotly charts
def interactive_plot(df):
    fig = px.line()
    for i in df.columns[1:]:
        fig.add_scatter(x=df['Date'], y=df[i], name=i)
    fig.update_layout(
        width=450,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1))

    return fig


# function to normalize the closing prices based on initial price
def normalize(df2):
    df = df2.copy()
    for i in df.columns[1:]:
        df[i] = df[i] / df[i][0]
    return df
# function to calculate the daily return
def daily_return(df):
    df_daily_return = df.copy()
    for i in df_daily_return.columns[1:]:
        df_daily_return[i] = df_daily_return[i].pct_change()
        
    df_daily_return.dropna(inplace=True)
    return df_daily_return



# function to calculate the beta
def calculate_beta(stocks_daily_return_df,stocks):
    rm  =stocks_daily_return_df['sp500'].mean()*252
    b,a = np.polyfit(stocks_daily_return_df['sp500'], stocks_daily_return_df[stocks],1)
    return b,a