from persistence import repo
from persistence import Order
from persistence import Hat
from persistence import Supplier

def parse(file1, file2, output_file):
    repo.create_tables()
    # Parsing input file
    with open(file1) as f:
        lines = f.readlines()
        first_line = lines[0].split(',')
        num_of_hats = int(first_line[0])
        num_of_suppliers = int(first_line[1][:-1])
        for i in range(1, 1+ num_of_hats):
            current_line = lines[i].split(',')
            id = int(current_line[0])
            topping = current_line[1]
            supplier = int(current_line[2])
            quantity = int(current_line[3][:-1])
            repo.hats.insert(Hat(id, topping, supplier, quantity))
        for i in range(1 + num_of_hats, 1 + num_of_hats + num_of_suppliers):
            current_line = lines[i].split(',')
            id = int(current_line[0])
            name = current_line[1][:-1]
            if i == num_of_hats + num_of_suppliers:
                name = current_line[1]
            repo.suppliers.insert(Supplier(id, name))
    # Parsing orders
    with open(file2) as g:
        lines = g.readlines()
        output = open(output_file, "w")
        for i in range(len(lines)):
            current_line = lines[i].split(',')
            order_location = current_line[0]
            order_topping = current_line[1][:-1]
            if i == len(lines) - 1:
                order_topping = current_line[1]
            ordered_hat = repo.hats.order(order_topping)
            if ordered_hat != None:
                repo.orders.insert(Order(i + 1, order_location, ordered_hat.id))
                current_supplier = repo.suppliers.find(ordered_hat.supplier)
                output.write(order_topping + "," + current_supplier.name + "," + order_location + "\n")
        output.close()
