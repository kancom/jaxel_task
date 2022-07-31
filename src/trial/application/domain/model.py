from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from ..foundation import Pair


class Quote(BaseModel):
    pair: Pair
    ts: datetime
    rate: Decimal
