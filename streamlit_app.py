import streamlit as st
import pandas as pd
import data

st.title('🏃 채권 모아보기')

dt = st.date_input('🗓️ 조회할 일자')
column_config = {
            'itmsNm': '채권명',
            'trqu': '거래량',
            'clprPrc': '가격',
            'clprBnfRt': '수익률',
            'bondSrfcInrt': '표면이율',
            'scrsItmsKcdNm': '분류',
            'bondIsurNm': '발행',
            'bondExprDt': '만기일',
            'intPayCyclCtt': '이자주기',
            # 'kisScrsItmsKcdNm': '한국신용평가',
            # 'kbpScrsItmsKcdNm': '한국자산평가',
            # 'niceScrsItmsKcdNm': 'NICE평가정보',
            'rating': '신용도',
        }

try:
    df = data.get_bond_info(dt.strftime('%Y%m%d'))
    df.trqu = df.trqu.astype('int')
    df.kisScrsItmsKcdNm = df.kisScrsItmsKcdNm.str.replace('0', '') 
    df.niceScrsItmsKcdNm = df.niceScrsItmsKcdNm.str.replace('0', '') 
    df.bondExprDt = pd.to_datetime(df.bondExprDt, format='%Y%m%d', errors='coerce').dt.date
    df['rating'] = df.apply(lambda x: '/'.join(set([str(y).replace('0', '')
                for y in (x.kisScrsItmsKcdNm, x.kbpScrsItmsKcdNm, x.niceScrsItmsKcdNm)
                if str(y) != 'nan'])), axis=1)
    st.dataframe(df.iloc[:,
        [0,4,5,1,3,7,6,8,12]],
        use_container_width=True,
        hide_index=True,
        column_config=column_config)
except:
    st.info('🫠 데이터가 없습니다')
