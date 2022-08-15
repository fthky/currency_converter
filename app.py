import streamlit as st
from requests import get
import json


try:

    ######### Currency Convert ##########

    API_KEY = "Your_API_Key" 
    BASE_URL = "https://free.currconv.com/"


    def get_currencies():
            
        endpoint = f"api/v7/currencies?apiKey={API_KEY}"
        url = BASE_URL + endpoint
        data = get(url).json()['results']
        data = list(data.items())
        data.sort()

        return data
    

    def list_currencies(currencies):
        currList = []
        for name, currency in currencies:
            name = currency['currencyName']
            id = currency['id']
            symbol = currency.get("currencySymbol", "")
            currList.append(f"{id}-{name}-{symbol}")
        return currList


    def exchange_rate(fromCurrency, toCurrency):
        endpoint = f"api/v7/convert?q={fromCurrency}_{toCurrency}&compact=ultra&apiKey={API_KEY}"
        url = BASE_URL + endpoint
        response = get(url).json()
        return list(response.values())[0]


    def calculate(fromCurrency, toCurrency, amount):
        rate = exchange_rate(fromCurrency, toCurrency)
        if rate is None:
            return
        calculated_amount = rate * amount
        return calculated_amount
        

        ############ Streamlit App ############

    data = get_currencies()

    st.title("Currency Converter")
    fromCurr = st.selectbox(
        'From',
        (list_currencies(data)))

    fromCurrId = fromCurr.split("-")[0]



    toCurr = st.selectbox(
        'To',
        (list_currencies(data))
    )

    toCurrId = toCurr.split("-")[0]

    amount = st.number_input('Amount')

    if st.button('Convert'):
        st.write("Exchange Rate:",exchange_rate(fromCurrId,toCurrId))
        st.write(amount, fromCurrId, "is", calculate(fromCurrId,toCurrId,amount), toCurrId)
    else:
        st.write('Please click convert button!')

    st.caption("['Click'](https://github.com/fthky/currency_converter) for GitHub Repository")

except:
    st.write("Free API limit reached. (Number of Requests per Hour: 100).")
 

