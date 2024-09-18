from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(
    naming_convention=naming_convention
)

clients = Table(
    'clients',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True
    ),
    Column(
        'name',
        String,
        nullable=False
    ),
    Column(
        'surname',
        String(255),
        nullable=False
    ),
    Column(
        'patronymic',
        String(255),
        nullable=False
    ),
    Column(
        'password',
        String(512),
        nullable=False
    ),
    Column(
        'email',
        String(255),
        nullable=False
    ),
    Column(
        'token',
        String(1024),
        nullable=False
    ),
    Column(
        'role',
        String(255),
        nullable=False
    )
)

client_stocks = Table(
    'client_stocks',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True
    ),
    Column(
        'client_id',
        ForeignKey(
            'clients.id',
            ondelete='SET NULL'
        ),
        nullable=True,
    ),
    Column(
        'stock_id',
        ForeignKey(
            'stocks.id',
            ondelete='SET NULL'
        ),
        nullable=True,
    ),
    Column(
        'sell_price',
        Float,
        nullable=False,
    ),
    Column(
        'buy_price',
        Float,
        nullable=False,
    ),
    Column(
        'created_at',
        DateTime,
        nullable=False,
    ),
)

stocks = Table(
    'stocks',
    metadata,
    Column(
        'id',
        Integer,
        primary_key=True,
    ),
    Column(
        'ticker',
        String(12),
        nullable=False,
    ),
    Column(
        'company_name',
        String(255),
        nullable=False,
    )
)
