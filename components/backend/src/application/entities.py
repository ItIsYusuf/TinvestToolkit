from datetime import datetime

from attr import dataclass

@dataclass
class Client:
    id: int | None = None
    name: str = None
    surname: str = None
    patronymic: str = None
    password: str = None
    email: str = None
    token: str = None
    role: str = None

@dataclass
class ClientStocks:
    client_id: int | None = None
    stock_id: int | None = None
    sell_price: float = None
    buy_price: float = None

@dataclass
class Stocks:
    id: int | None = None
    ticker: str = None
    company_name: str = None