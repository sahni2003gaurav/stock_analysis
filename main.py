import streamlit as st
import pandas as pd
import numpy as np

# i need to add user input to show stocks *DONE
# i need to add revenue and profits dataset
# i need to add my personal analysis

st.header("**ANALYSIS OF LARGE CAP COMPANIES BY USING THEIR DATA FROM 02-03-2020 TO 28-02-2022**")

st.sidebar.header('USER INPUT')

def get_input():
    start_date = st.sidebar.text_input("Start Date","02-03-2020")
    end_date = st.sidebar.text_input("End Date","28-02-2022")
    stock_symbol = st.sidebar.text_input("Stock Symbol","WIPR")
    return start_date,end_date,stock_symbol

def get_company_name(symbol):
    if symbol== 'WIPR':
        return 'WIPRO'
    elif symbol=='SBI':
        return 'SBI'
    else:
        'None'

def get_data(symbol,start,end):
    if symbol.upper()=='WIPR':
        df = pd.read_csv("WIPRO.csv")
        df_prom = pd.read_csv('WIPRO_PROM.csv')
    elif symbol.upper()=='SBI':
        df = pd.read_csv("E:/SBIN.NS.csv")
        df_prom = pd.read_csv('SBI_PROM.csv')
    else:
        df = pd.DataFrame(columns = ['Date','Close','Open','Volume','Adj Close','High','Low'])
        df_prom = pd.DataFrame(columns = ["COMPANY","PROMOTERS","PUBLIC","EMPLOYEE TRUSTS","STATUS","AS ON DATE","SUBMISSION DATE","REVISION DATE",])

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    start_row = 0
    end_row = 0

    for i in range(0, len(df)):
        if start <= pd.to_datetime(df['Date'][i]):
            start_row = i
            break

    for j in range(0, len(df)):
        if end <= pd.to_datetime(df['Date'][len(df) - 1 - j]):
            end_row = len(df) - 1 - j
            break

    df = df.set_index(pd.DatetimeIndex(df['Date'].values))

    return df.iloc[start_row:end_row+1, :],df_prom

def get_technical_analysis(df,df_prom):
    rating = 0
    holding = np.array(df_prom['PROMOTERS'])

    if holding[8]>=70:
        rating+=20
    elif (holding[8]>=60) & (holding[8]<=70):
        rating+=18
    elif (holding[8]>=60) & (holding[8]<=70):
        rating+=18
    elif (holding[8]>=50) & (holding[8]<=60):
        rating+=16
    elif (holding[8]>=40) & (holding[8]<=50):
        rating+=12
    elif (holding[8]>=20) & (holding[8]<=40):
        rating+=9
    elif (holding[8]>=10) & (holding[8]<=20):
        rating+=5
    else:
        rating+=0
    return rating

#starting the program
start,end,symbol = get_input()

df,df_prom = get_data(symbol,start,end)

company_name = get_company_name(symbol.upper())

#display STOCK PRICE
st.write("**STOCK PRICE** OF ",company_name)
st.line_chart(df['Adj Close'])

#display VOLUME CHART
st.write("VOLUME CHART")
st.line_chart(df['Volume'])

#display statistics
st.write("STATISTICS OF ",company_name)
st.write(df)

#display shareholding pattern
st.header("SHAREHOLDING PATTERN")
st.write(df_prom)

#display technical analysis
st.header("TECHNICAL ANALYSIS")
rating = get_technical_analysis(df,df_prom)
st.write("RATING FOR THIS STOCK IS:",rating," OUT OF 100")
