from datetime import datetime

from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.sql.sqltypes import DECIMAL
from sqlalchemy.types import DateTime

metadata = MetaData()


QuoteModel = Table(
    "quote",
    metadata,
    Column("quote_id", Integer, primary_key=True),
    Column("pair", String(length=50)),
    Column("ts", DateTime, default=datetime.now),
    Column("rate", DECIMAL(6, 3)),
)
