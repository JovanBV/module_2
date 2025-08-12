from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Text, Enum
from sqlalchemy import insert, select, update, delete, ForeignKey
from sqlalchemy.exc import IntegrityError
import bcrypt

metadata = MetaData()

user_table = Table("users", metadata,
    Column("id", Integer, nullable=False, primary_key=True),
    Column("username", String, nullable=False, unique=True),
    Column("password", Text, nullable=False),
    Column("role", String, nullable=False)
)

fruit_table = Table("fruits", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("price", Integer, nullable=False),
    Column("entry_date", Date, nullable=False),
    Column("stock", Integer, nullable=False)
)

order_items_table = Table("order_items", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", Integer, ForeignKey("orders.id"), nullable=False),
    Column("fruit_id", Integer, ForeignKey("fruits.id"), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("subtotal", Integer, nullable=False)
)

order_table = Table("orders", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("customer_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("status", Enum('pending', 'confirmed', 'preparing', 'delivered', 'cancelled', name='order_status'), default='pending')
)


class db_manager:
    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://postgres:jovan@localhost:5432/postgres')
        metadata.create_all(self.engine)

    def insert_user(self, username, password, role):
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            hashed_password_str = hashed_password.decode('utf-8')

            stmt = insert(user_table).values(username=username, password=hashed_password_str, role=role).returning(user_table)
            with self.engine.connect() as conn:
                result = conn.execute(stmt)
                user = result.fetchone()
                conn.commit()
            return user._asdict()
        except IntegrityError:
            return None

    def login_user(self, username, password):
        stmt = select(user_table).where(user_table.c.username == username)
        with self.engine.connect() as conn:
            result = conn.execute(stmt).fetchone()
            if result is None:
                return None
            
            user = result._asdict()
            stored_hash = user["password"]
            stored_hash_bytes = stored_hash.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash_bytes):
                del user["password"]
                return user
            else:
                return None

    def get_user_by_id(self, id):
        stmt = select(user_table).where(user_table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt).fetchone()
        if result is None:
            return None
        user = result._asdict()
        return user
    
    def get_fruit_by_id(self, id):
        stmt = select(fruit_table).where(fruit_table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt).fetchone()
        if result is None:
            return None
        fruit = result._asdict()
        return fruit

    def insert_fruit(self, name, price, entry_date, stock):
        try:
            stmt = insert(fruit_table).returning(fruit_table).values(name=name, price=price, entry_date=entry_date, stock=stock)
            with self.engine.connect() as conn:
                result = conn.execute(stmt)
                inserted_row = result.fetchone()
                conn.commit()
            return inserted_row._asdict()
        except IntegrityError:
            return None

    def get_fruits(self):
        stmt = select(fruit_table)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            all_fruits = [row._asdict() for row in result.fetchall()]
            return all_fruits

    def update_fruit(self, fruit_id, amount):
        try:
            stmt = update(fruit_table).where(fruit_table.c.id == fruit_id).values(amount=amount).returning(fruit_table)
            with self.engine.connect() as conn:
                result = conn.execute(stmt)
                updated_row = result.fetchone()
                conn.commit()
                return updated_row._asdict()
        except IntegrityError:
            return None

    def get_fruit(self, fruit_id):
        stmt = select(fruit_table).where(fruit_table.c.id == fruit_id)
        with self.engine.connect() as conn:
            return conn.execute(stmt).fetchone()

    def delete_fruit(self, fruit_id):
        try:
            stmt = delete(fruit_table).where(fruit_table.c.id == fruit_id).returning(fruit_table)
            with self.engine.connect() as conn:
                deleted_fruit = conn.execute(stmt)
                result = deleted_fruit.fetchone()
                conn.commit()
                return result._asdict()
        except IntegrityError:
            return None
        except AttributeError:
            return None

    def create_pending_order(self, user_id):
        try:
            stmt = insert(order_table).returning(order_table).values(customer_id=user_id, status='pending')
            with self.engine.connect() as conn:
                result = conn.execute(stmt)
                new_order = result.fetchone()
                conn.commit()
            return new_order._asdict()
        except IntegrityError:
            return None

    def get_pending_order(self, user_id):
        try:
            stmt = select(order_table).where(
                (order_table.c.customer_id == user_id) & 
                (order_table.c.status == 'pending')
            )
            with self.engine.connect() as conn:
                result = conn.execute(stmt).fetchone()
                if result is None:
                    return None
                return result._asdict()
        except Exception:
            return None

    def add_item_to_order(self, user_id, fruit_id, quantity):
        try:
            fruit = self.get_fruit_by_id(fruit_id)
            if not fruit:
                return None
            
            pending_order = self.get_pending_order(user_id)
            if not pending_order:
                pending_order = self.create_pending_order(user_id)
                if not pending_order:
                    return None
            
            order_id = pending_order["id"]
            subtotal = fruit["price"] * quantity
            
            stmt = insert(order_items_table).returning(order_items_table).values(
                order_id=order_id, 
                fruit_id=fruit_id, 
                quantity=quantity,
                subtotal=subtotal
            )
            with self.engine.connect() as conn:
                result = conn.execute(stmt)
                inserted_item = result.fetchone()
                conn.commit()
            return inserted_item._asdict()
        except IntegrityError:
            return None

    def get_pending_order_items(self, user_id):
        try:
            pending_order = self.get_pending_order(user_id)
            if not pending_order:
                return []
            
            order_id = pending_order["id"]
            stmt = select(order_items_table).where(order_items_table.c.order_id == order_id)
            with self.engine.connect() as conn:
                result = conn.execute(stmt)
                return [row._asdict() for row in result.fetchall()]
        except Exception:
            return []

    def validate_order_stock(self, order_items):
        try:
            for item in order_items:
                fruit = self.get_fruit_by_id(item["fruit_id"])
                if not fruit or item["quantity"] > fruit["stock"]:
                    return {"error": f"Not enough stock for fruit id: {item['fruit_id']}."}
            return None
        except Exception as error:
            return {"error": str(error)}

    def confirm_order(self, user_id):
        try:
            with self.engine.begin() as conn: 
                pending_order = self.get_pending_order(user_id)
                if not pending_order:
                    return {"error": "No pending order found"}
                
                order_id = pending_order["id"]
                
                stmt = select(order_items_table).where(order_items_table.c.order_id == order_id)
                result = conn.execute(stmt)
                order_items = [row._asdict() for row in result.fetchall()]
                
                if not order_items:
                    return {"error": "No items in order"}
                
                stock_validation = self.validate_order_stock(order_items)
                if stock_validation:
                    return stock_validation
                
                for item in order_items:
                    fruit = self.get_fruit_by_id(item["fruit_id"])
                    new_stock = fruit["stock"] - item["quantity"]
                    
                    update_stmt = update(fruit_table).where(
                        fruit_table.c.id == item["fruit_id"]
                    ).values(stock=new_stock)
                    conn.execute(update_stmt)
                
                confirm_stmt = update(order_table).where(
                    order_table.c.id == order_id
                ).values(status='confirmed').returning(order_table)
                
                result = conn.execute(confirm_stmt)
                confirmed_order = result.fetchone()
                
                return confirmed_order._asdict()
                
        except Exception as error:
            return {"error": str(error)}

    def get_user_orders(self, user_id):
        try:
            stmt = select(order_table).where(order_table.c.customer_id == user_id)
            with self.engine.connect() as conn:
                result = conn.execute(stmt)
                return [row._asdict() for row in result.fetchall()]
        except Exception:
            return []

db = db_manager()