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
            'itmsNm': '채권명',
            'trqu': '거래량',
            'clprPrc': '가격',
            'clprBnfRt': '수익률',
            'bondSrfcInrt': '표면이율'
            'scrsItmsKcdNm': '분류',
            'bondIsurNm': '발행',
            'bondExprDt': '만기일',
            'intPayCyclCtt': '이자주기',
            'kisScrsItmsKcdNm': '한국신용평가',
            'kbpScrsItmsKcdNm': '한국자산평가',
            'niceScrsItmsKcdNm': 'NICE평가정보',
        },
    )
except:
    st.info('🫠 데이터가 없습니다')
