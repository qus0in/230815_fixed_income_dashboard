import streamlit as st
import data
import datetime
import pandas as pd

st.set_page_config(page_title="채권왕 변채권", page_icon="🦁")
st.title('🏃 채권 모아보기')

dt = st.date_input('🗓️ 조회할 일자')
st.toast('T+1 12:00 이후에 업데이트', icon='🗓️')
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
        col1, col2, col3, col4  = st.columns(4)
        with col1:
            r = st.radio('🌶️ 거래량', ['없음', '50% 이상', '75% 이상'])
            if r != '없음':
                df.query(f'trqu > {df.trqu.quantile(.5 if r == "50% 이상" else .75)}', inplace=True)
        with col2:
            invest = st.radio('🍺 투자등급 이상', ['미적용', '적용'])
            if invest == '적용':
                df.query(f'not rating.str.contains("B") or rating.str.contains("BBB")', inplace=True)
        with col3:
            duration = st.radio('🥃 최대 듀레이션', ['없음', '3년'])
            filter_date = (pd.Timestamp(datetime.datetime.today()) + pd.DateOffset(years=3)).date()
            if duration == '3년':
                df.query(f'bondExprDt < @filter_date',
                         inplace=True)
        with col4:
            earn = st.radio('🥃 최소 기대수익률', ['없음', '5%'])
            if earn == '5%':
                df.query(f'afterTax >= 5', inplace=True)
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

    st.write(f"**🥢 검색된 채권** : {len(df)}건")
    st.dataframe(df,
        use_container_width=True,
        hide_index=True,
        column_config=column_config)
except data.NoDataError:
    st.info('🫠 데이터가 없습니다')
except Exception as e:
    st.error(e)