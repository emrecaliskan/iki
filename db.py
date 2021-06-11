import datetime as dt
from pathlib import Path
import pytz
import constants

import duckdb
from tenacity import retry, stop_after_attempt, wait_fixed


class Db:
    DATA_DIR = Path(__file__).resolve().parent / "data"

    @classmethod
    def start(cls):
        cls._init_data_dir()
        cls._create_tables()

    @classmethod
    def _init_data_dir(cls):
        Path(cls.DATA_DIR).mkdir(parents=True, exist_ok=True)

    @classmethod
    @retry(stop=stop_after_attempt(5), wait=wait_fixed(0.05))
    def _get_cursor(cls, file_path, read_only=False):
        return duckdb.connect(database=file_path, read_only=read_only).cursor()

    @classmethod
    def _create_tables(cls):
        cur = cls._get_cursor(str(cls.DATA_DIR / "trades.db"), read_only=False)
        create_trades = """
            CREATE TABLE trades (
                symbol         VARCHAR,
                exchange      VARCHAR,
                tradetime      TIMESTAMP,
                amount         DOUBLE,
                price          DOUBLE,
                side_buy       BOOLEAN,
                forced         BOOLEAN
            );
        """
        try:
            cur.execute(create_trades)
        except Exception as e:
            if "already exists" not in str(e):
                raise e

        cur = cls._get_cursor(str(cls.DATA_DIR / "ticks.db"), read_only=False)
        create_trades = """
            CREATE TABLE ticks (
                symbol         VARCHAR,
                exchange       VARCHAR,
                timestamp      TIMESTAMP,
                price            DOUBLE
            );
        """
        try:
            cur.execute(create_trades)
        except Exception as e:
            if "already exists" not in str(e):
                raise e

    @classmethod
    def insert_trade(cls, symbol: str, exchange: str, timestamp: float, amount: float, price: float, side_buy: bool,
                     forced=False):
        try:
            cur = cls._get_cursor(str(cls.DATA_DIR / "trades.db"), read_only=False)
        except:
            return
        cur.execute(
            "INSERT INTO trades VALUES (?, ?, ?, ?, ?, ?, ?)",
            [symbol, exchange, dt.datetime.fromtimestamp(timestamp, tz=pytz.utc), amount, price, side_buy, forced],
        )

    @classmethod
    def insert_ticks(cls, symbol: str, exchange: str, timestamp: float, price: float):
        with constants.DB_LOCK:
            cur = cls._get_cursor(str(cls.DATA_DIR / "ticks.db"), read_only=False)
            cur.execute(
                "INSERT INTO ticks VALUES (?, ?, ?, ?)",
                [symbol, exchange, dt.datetime.fromtimestamp(timestamp, tz=pytz.utc), price]
            )

    @classmethod
    def query(cls, query: str, db: str, output_df: bool = False):
        db_name = 'ticks.db' if db == 'ticks' else 'trades.db'
        with constants.DB_LOCK:
            cur = cls._get_cursor(str(cls.DATA_DIR / db_name), read_only=True)
            if output_df:
                return cur.execute(query).fetchdf()
            return cur.execute(query).fetchall()
