import streamlit as st
import data

st.title('🏃 채권 모아보기')

dt = st.date_input('🗓️ 조회할 일자')

try:
    df = data.get_bond_info(dt.strftime('%Y%m%d'))
    df.trqu = df.trqu.astype('int')
    st.dataframe(df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'itmsNm': '채권명'
        }
    )
except:
    st.info('🫠 데이터가 없습니다')
