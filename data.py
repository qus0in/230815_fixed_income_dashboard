import os
import requests
import pandas as pd
import streamlit as st

BASE_URL = 'http://apis.data.go.kr/1160100/service'

@st.cache_data
def get_bond_price_info(base_date: str):
    URL = f'{BASE_URL}/GetBondSecuritiesInfoService/getBondPriceInfo'
    params = dict(
        serviceKey=os.getenv('ACCESS_KEY'),
        resultType='json',
        basDt=base_date,
        numOfRows=1000,
    )
    response = requests.get(URL, params=params)
    df = pd.DataFrame(response.json()['response']['body']['items']['item'])
    df = df.loc[:, ['isinCd', 'itmsNm', 'trqu', 'clprPrc', 'clprBnfRt']]
    df.set_index('isinCd', inplace=True)
    return df

@st.cache_data
def get_bond_base_info(base_date: str):
    URL =  f'{BASE_URL}/GetBondIssuInfoService/getBondBasiInfo'
    접속키 = os.getenv('ACCESS_KEY')
    params = dict(
        serviceKey=os.getenv('ACCESS_KEY'),
        resultType='json',
        basDt=base_date,
        numOfRows=30000,
    )
    response = requests.get(URL, params=params)
    df = pd.DataFrame(response.json()['response']['body']['items']['item'])
    df = df.loc[:, [
        'isinCd', 'scrsItmsKcdNm', 'bondIsurNm', 'bondExprDt', 'bondSrfcInrt', 'intPayCyclCtt', 
        'kisScrsItmsKcdNm', 'kbpScrsItmsKcdNm', 'niceScrsItmsKcdNm'
    ]]
    df.set_index('isinCd', inplace=True)
    return df

@st.cache_data
def get_bond_info(base_date: str):
    price_info = get_bond_price_info(base_date)
    base_info = get_bond_base_info(base_date)
    df = price_info.join(base_info, how='inner')
    return df