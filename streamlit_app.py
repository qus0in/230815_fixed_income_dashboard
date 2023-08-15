import streamlit as st
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
            'afterTax': '세후수익률',
        }

try:
    df = data.get_bond_info(dt.strftime('%Y%m%d'))
    with st.container():
        st.subheader('🌱 필터')
        col1, col2, col3  = st.columns(3)
        with col1:
            r = st.radio('🌶️ 거래량', ['없음', '50% 이상', '75% 이상'])
            if r != '없음':
                df.query(f'trqu > {df.trqu.quantile(.5 if r == "50% 이상" else .75)}', inplace=True)
        with col2:
            invest = st.radio('🍺 투자등급 이상', ['미적용', '적용'])
            if invest == '적용':
                df.query(f'not rating.str.contains("B") or rating.str.contains("BBB")', inplace=True)
        with col3:
            ms = st.multiselect(
                '🍅 종류', ['후순위', '신종자본', '조건부자본', '전환사채'],
                default=['후순위', '신종자본', '조건부자본', '전환사채'])
            if '후순위' not in ms:
                df.query('not itmsNm.str.contains("\(후\)") ', inplace=True)
            if '신종자본' not in ms:
                df.query('not itmsNm.str.contains("신종") ', inplace=True)
            if '조건부자본' not in ms:
                df.query('not itmsNm.str.contains("\(상\)") ', inplace=True)
            if '전환사채' not in ms:
                df.query('not itmsNm.str.contains("CB") ', inplace=True)

    st.dataframe(df,
        use_container_width=True,
        hide_index=True,
        column_config=column_config)
except data.NoDataError:
    st.info('🫠 데이터가 없습니다')
except Exception as e:
    st.error(e)