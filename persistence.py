import sqlite3
import sys
import atexit

# DTO
class Hat(object):
    def __init__(self, id, topping, supplier, quantity):
        self.id = id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity

class Supplier(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Order(object):
    def __init__(self, id, location, hat):
        self.id = id
        self.location = location
        self.hat = hat

# DAO
class _Hats:
    def __init__(self, conn):
        self._conn = conn
    
    def insert(self, hat):
        self._conn.execute("INSERT INTO hats(id, topping, supplier, quantity) VALUES (?, ?, ?, ?)", [hat.id, hat.topping, hat.supplier, hat.quantity])
    
    def find(self, hat_topping):
        c = self._conn.cursor()
        c.execute("SELECT id, topping, supplier, quantity FROM hats WHERE topping = ?", [hat_topping])
        ret = c.fetchone()
        if ret != None:
            return Hat(*ret)
        return None

    def order(self, topping):
        c = self._conn.cursor()
        c.execute("SELECT id, topping, supplier, quantity FROM Hats WHERE topping = ? ORDER BY supplier ASC", [topping])
        current_hat = c.fetchone()
        if current_hat == None:
            return None
        current_hat = Hat(*current_hat)
        if current_hat.quantity - 1 == 0:
            c.execute("DELETE FROM hats WHERE id = ?", [current_hat.id])
        else:
            c.execute("UPDATE Hats SET quantity = ? WHERE id = ?", [current_hat.quantity - 1, current_hat.id])
        return current_hat

class _Suppliers:
    def __init__(self, conn):
        self._conn = conn
    
    def insert(self, supplier):
        self._conn.execute("INSERT INTO suppliers(id, name) VALUES (?, ?)", [supplier.id, supplier.name])
    
    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("SELECT id, name FROM suppliers WHERE id = ?", [supplier_id])
        return Supplier(*c.fetchone())

class _Orders:
    def __init__(self, conn):
        self._conn = conn
    
    def insert(self, order):
        self._conn.execute("INSERT INTO orders(id, location, hat) VALUES (?, ?, ?)", [order.id, order.location, order.hat])
    
    def find(self, order_id):
        c = self._conn.cursor()
        c.execute("SELECT id, location, hat FROM orders WHERE id = ?", [order_id])
        return Order(*c.fetchone())

# Repository
class _Repository(object):
    def __init__(self, db_file):
        self._conn = sqlite3.connect(db_file)
        self.hats = _Hats(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.orders = _Orders(self._conn)
    
    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        cur = self._conn.cursor()
        cur.executescript("""
        CREATE TABLE suppliers(
            id INTEGER PRIMARY KEY,
            name STRING NOT NULL
        );
        CREATE TABLE hats(
            id INTEGER PRIMARY KEY,
            topping STRING NOT NULL,
            supplier INTEGER REFERENCES suppliers(id),
            quantity INTEGER NOT NULL
            );
        CREATE TABLE orders(
            id INTEGER PRIMARY KEY,
            location STRING NOT NULL,
            hat INTEGER REFERENCES hats(id)
        );
        """)

repo = _Repository(sys.argv[4])
atexit.register(repo._close)