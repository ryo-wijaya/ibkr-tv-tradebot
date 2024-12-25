from pydantic import BaseModel


class TradeRequest(BaseModel()):
    key: str
    symbol: str
    quantity: int
