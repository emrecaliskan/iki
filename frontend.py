import altair as alt
from db import Db
import pandas as pd
import base64


def prep_chart(symbol: str, time_frame: str, width: int = 700, height: int = 400):
    interval_input = str(time_frame[:-1]) + (" minutes" if time_frame[-1] == 'm' else ' hours')
    query = f"""SELECT * FROM ticks WHERE symbol='{symbol}' AND timestamp>=NOW()-interval '{interval_input}' ORDER BY timestamp"""
    df = Db.query(query, 'ticks', output_df=True)
    line = alt.Chart(df, title=symbol).mark_line().encode(
        x='timestamp',
        y=alt.Y('price', scale=alt.Scale(domain=(df.price.min(), df.price.max()))),
    ).properties(width=width, height=height)
    return line, df


def get_table_download_link_csv(df: pd.DataFrame):
    csv = df.to_csv(index=False).encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv" target="_blank">Download csv file</a>'
    return href
