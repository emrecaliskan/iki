import datetime as dt
import time
import constants
from db import Db
from exchanges.ftx import FtxWebsocketClient, Ftx


def backfill_ticks():
    now = dt.datetime.now()
    half_day_ago = now - dt.timedelta(hours=12)
    latest_date_in_db = Db.query("Select timestamp from ticks order by timestamp desc limit 1", 'ticks')
    start_time = half_day_ago if not latest_date_in_db else max(latest_date_in_db[0][0], half_day_ago)
    for symbol in constants.DEMO_MARKETS:
        print('backfilling', symbol)
        time.sleep(0.1)  # a little buffer
        out = Ftx.get_hist_prices(symbol, resolution=60, start=start_time, end=now)
        for tick in out['result']:
            Db.insert_ticks(symbol, 'FTX', int(tick['time'] / 1000), (tick['low'] + tick['high']) / 2.0)


def handle_tick_msg(msg: str) -> None:
    Db.insert_ticks(msg['market'], "FTX", int(msg['data']['time']), msg['data']['last'])


def handle_trades_msg(msg: str) -> None:
    pass


def start_feeds():
    Db.start()
    ws_client = FtxWebsocketClient(handle_tick_msg, handle_trades_msg)
    for symbol in constants.DEMO_MARKETS:
        ws_client.get_ticker(symbol)


def start():
    Db.start()
    backfill_ticks()
    start_feeds()  # forever running thread
