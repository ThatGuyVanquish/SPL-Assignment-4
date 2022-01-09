import _Repository

def parse():
    # Parsing input file
    with open(args[1]) as f:
        lines = f.readLines()
        first_line = lines[0].split(',')
        num_of_hats = int(first_line[0])
        num_of_suppliers = int(first_line[1][:-1])
        for i in range(1, 1+ num_of_hats):
            current_line = lines[i].split(',')
            id = int(current_line[0])
            topping = current_line[1]
            supplier = int(current_line[2])
            quantity = int(current_line[3][:-1])
            repo.hats.insert_hat(id, topping, supplier, quantity)
        for i in range(1 + num_of_hats, 1 + num_of_hats + num_of_suppliers):
            current_line = lines[i].split(',')
            id = int(current_line[0])
            name = current_line[1][:-2]
            repo.suppliers.insert_supplier(id, name)
    # Parsing orders
    with open(args[2]) as f:
        lines = f.readLines()
        for i in range(len(lines)):
            current_line = lines[i].split(',')
            repo.orders.inert_order(i + 1, current_line[0], current_line[1][:-1])