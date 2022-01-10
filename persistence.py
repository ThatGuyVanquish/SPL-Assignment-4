import sqlite3
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
        self._conn.execute("INSERT INTO Hats(id, topping, supplier, quantity) VALUES (?, ?, ?, ?)", [hat.id, hat.topping, hat.supplier, hat.quantity])
    
    def find(self, hat_topping):
        c = self._conn.cursor()
        c.execute("SELECT id FROM Hats WHERE topping = ?", [hat_topping])
        return Hat(*c.fetchone())

    def order(self, hat_id):
        c = self._conn.cursor()
        c.execute("SELECT id FROM Hats WHERE id = ?", [hat_id])
        current_hat = Hat(*c.fetchone())
        if current_hat = None:
            return None
        c.execute("SELECT id FROM Hats WHERE topping = ?", [current_hat.topping])
        returned_hat = Hat(*c.fetchone())
        if returned_hat.quantity - 1 == 0:
            c.execute("DELETE FROM Hats WHERE id = ?", [returned_hat.id])
        else:
            c.execute("UPDATE Hats SET quantity = ? WHERE id = ?", [returned_hat.quantity - 1, returned_hat.id])
        return returned_hat

class _Suppliers:
    def __init__(self, conn):
        self._conn = conn
    
    def insert(self, supplier):
        self._conn.execute("INSERT INTO Suppliers(id, name) VALUES (?, ?)", [supplier.id, supplier.name])
    
    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("SELECT id FROM Suppliers WHERE id = ?", [supplier_id])
        return Supplier(*c.fetchone())

class _Orders:
    def __init__(self, conn):
        self._conn = conn
    
    def insert(self, order):
        self._conn.execute("INSERT INTO Orders(id, location, hat) VALUES (?, ?, ?)", [order.id, order.location, order.hat])
    
    def find(self, order_id):
        c = self._conn.cursor()
        c.execute("SELECT id FROM Orders WHERE id = ?", [order_id])
        return Order(*c.fetchone())

# Repository
class _Repository(object):
    def __init__(self):
        #self._conn = sqlite.connect(args[3])
        self._conn = sqlite.connect('database.db')
        self.hats = _Hats(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.orders = _Orders(self._conn)
    
    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE Hats (
        id INTEGER PRIMARY KEY,
        topping STRING NOT NULL,
        supplier INTEGER REFERENCES Suppliers(id),
        quantity INTEGER NOT NULL
        );
        CREATE TABLE Suppliers (
        id INTEGER PRIMARY KEY,
        name STRING NOT NULL
        );
        CREATE TABLE Orders (
        id INTEGER PRIMARY KEY,
        location STRING NOT NULL,
        hat INTEGER REFERECES Hats(id)
        );
        """)

    repo = _Repository()
    atexit.register(repo._close)