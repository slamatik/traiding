import sqlite3
import pandas as pd
import os
import datetime
from populate_prices_db import get_prices

f = os.path.getmtime('stocks.db')
print(datetime.datetime.fromtimestamp(f))


def update():
    get_prices('1d')
