from sqlalchemy.orm import registry

from src.adapters.database import tables
from src.application import entities

mapper = registry()

mapper.map_imperatively(entities.Client, tables.clients)
mapper.map_imperatively(entities.ClientStocks, tables.client_stocks)
mapper.map_imperatively(entities.Stocks, tables.stocks)