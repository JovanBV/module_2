from sqlalchemy import MetaData, Table, Column, Integer, String, Date, ForeignKey


metadata = MetaData()

user_table = Table("users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("password", String)
)

fruit_table = Table("fruits", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("price", Integer),
    Column("entry_date", Date),
    Column("amount", Integer)
)

invoice_table = Table("invoices", metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer),
    Column("fruit_id", Integer),
    Column("quantity", Integer),
    Column("total", Integer)
)