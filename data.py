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
    # print(response.json())
    df = pd.DataFrame(response.json()['response']['body']['items']['item'])
    df = df.loc[:, ['isinCd', 'itmsNm', 'trqu', 'clprPrc', 'clprBnfRt']]
    df.trqu = df.trqu.astype('int')
    df.clprBnfRt = df.clprBnfRt.astype('float')
    df.set_index('isinCd', inplace=True)
    return df

@st.cache_data
def get_bond_base_info(base_date: str):
    URL =  f'{BASE_URL}/GetBondIssuInfoService/getBondBasiInfo'
    params = dict(
        serviceKey=os.getenv('ACCESS_KEY'),
        resultType='json',
        basDt=base_date,
        numOfRows=30000,
    )
    response = requests.get(URL, params=params)
    # print(response.json())
    df = pd.DataFrame(response.json()['response']['body']['items']['item'])
    df = df.loc[:, [
        'isinCd', 'scrsItmsKcdNm', 'bondIsurNm', 'bondExprDt', 'bondSrfcInrt', 'intPayCyclCtt', 
        'kisScrsItmsKcdNm', 'kbpScrsItmsKcdNm', 'niceScrsItmsKcdNm'
    ]]
    df.bondSrfcInrt = df.bondSrfcInrt.astype('float')
    df.set_index('isinCd', inplace=True)
    return df

@st.cache_data
def get_bond_info(base_date: str):
    try:
        price_info = get_bond_price_info(base_date)
        base_info = get_bond_base_info(base_date)
        df = price_info.join(base_info, how='inner')
    except:
        raise NoDataError()
    df.kisScrsItmsKcdNm = df.kisScrsItmsKcdNm.str.replace('0', '') 
    df.niceScrsItmsKcdNm = df.niceScrsItmsKcdNm.str.replace('0', '') 
    df.bondExprDt = pd.to_datetime(df.bondExprDt, format='%Y%m%d', errors='coerce').dt.date
    df['rating'] = df.apply(lambda x: '/'.join(set([str(y).replace('0', '')
                for y in (x.kisScrsItmsKcdNm, x.kbpScrsItmsKcdNm, x.niceScrsItmsKcdNm)
                if str(y) != 'nan'])), axis=1)
    df['afterTax'] = df.clprBnfRt * (1 - 0.154)
    # 'itmsNm', 'trqu', 'clprPrc', 'clprBnfRt'
    # 0, 1, 2
    return df.iloc[:, [0,4,5,1,2,3,7,13,6,8,12]].sort_values('trqu', ascending=False)

class NoDataError(Exception):
    pass