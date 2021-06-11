import streamlit as st
import etl
import _thread
import frontend
import os

st.beta_set_page_config(layout="wide")

def already_started_etl():
    try:
        pids = set(int(line.strip()) for line in open('.ik'))
    except FileNotFoundError:
        pids = set()
    current_pid = os.getpid()
    if current_pid not in pids:
        with open('.ik', 'w') as f:
            f.write(f"{current_pid}\n")
        return False
    return True

# need to 'cache' to only startup etl job once
# (altho, streamlit is pretty buggy and runs this multiple times)
@st.cache(hash_funcs={_thread.LockType: lambda _: None}, show_spinner=False, suppress_st_warning=True)
def start_data_pipeline():
    if not already_started_etl():
        with st.spinner('Hold on, fetching/backfilling data (can take about a minute)...'):
            etl.start()
        st.balloons()

start_data_pipeline()


# Frontend
symbols = st.multiselect('Market', ['BTC-PERP', 'ETH-PERP', 'SOL-PERP'], default=['BTC-PERP'])
time_frame = st.selectbox('Time Frame', ['3m', '5m', '15m', '1h', '3h', '12h'], index=2)
num_symbols = len(symbols)
width = 900 / num_symbols

cols = st.beta_columns(num_symbols)
for idx, col in enumerate(cols):
    with col:
        chart, df = frontend.prep_chart(symbols[idx], time_frame, width=width)
        chart

st.button("Refresh")
st.markdown(frontend.get_table_download_link_csv(df), unsafe_allow_html=True)
