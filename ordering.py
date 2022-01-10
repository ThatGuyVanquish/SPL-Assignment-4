from persistence import repo

def order(file_name):
    current_id = 1
    current_order = repo._Orders.find(current_id)
    f = open(file_name, "w")
    while (current_order != None):
        current_hat = repo._Hats.order(current_order.hat)
        if current_hat != None:
            f.write()
        # need to write this to a file