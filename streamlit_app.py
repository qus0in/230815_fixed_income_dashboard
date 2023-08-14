import streamlit as st
import data

st.title('🏃 채권 모아보기')

dt = st.date_input('🗓️ 조회할 일자')

df = data.get_bond_info(dt.strftime('%Y%m%d'))

try:
    st.dataframe(df)
except:
    st.info('🫠 데이터가 없습니다')