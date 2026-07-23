# --- DATA STRUCTURES ---

customers = [] 
reservations = []
waiting_list = []
rooms = [
    {"no": "101", "type": "Single", "avail": True}, {"no": "102", "type": "Double", "avail": True},
    {"no": "103", "type": "Single", "avail": True}, {"no": "104", "type": "Double", "avail": True},
    {"no": "105", "type": "Suite", "avail": True}, {"no": "201", "type": "Single", "avail": True},
    {"no": "202", "type": "Double", "avail": True}, {"no": "203", "type": "Single", "avail": True},
    {"no": "204", "type": "Double", "avail": True}, {"no": "205", "type": "Suite", "avail": True}
]


# --- ALGORITHMS (LINEAR SEARCH & BUBBLE SORT) ---

def linear_search_cust_id(cid):
    for i in range(len(customers)):
        if customers[i]["id"] == cid:
            return i  
    return -1         

def linear_search_cust_name(name):
    results = []
    for i in range(len(customers)):
        if customers[i]["name"].lower() == name.lower():
            results.append(customers[i])
    return results

def linear_search_room(no):
    for i in range(len(rooms)):
        if rooms[i]["no"] == no: 
            return i
    return -1

def linear_search_res_id(rid):
    for i in range(len(reservations)):
        if reservations[i]["id"] == rid:
            return i
    return -1

def bubble_sort_customers():
    lst = customers.copy()
    n = len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j]["name"].lower() > lst[j+1]["name"].lower():
               
                lst[j], lst[j+1] = lst[j+1], lst[j]
    return lst


# --- MENUS ---

def c_menu():
    while True:
        c = input("\n1.Add 2.View 3.Search 4.Update 5.Delete 6.Sort 7.Back\nSelect: ")
        if c == '1':
            cid = input("ID: ").strip()
            if linear_search_cust_id(cid) != -1: 
                print("Error: Customer ID already exists.")
                continue
            n = input("Name: ").strip()
            p = input("Phone: ").strip()
            e = input("Email: ").strip()
            if not (cid and n and p and e): 
                print("Error: Empty field.")
                continue
            customers.append({"id": cid, "name": n, "phone": p, "email": e})
            print("Customer added.")
        elif c == '2':
            for d in customers: 
                print(f"{d['id']} | {d['name']} | {d['phone']} | {d['email']}")
        elif c == '3':
            sc = input("Search by: 1.ID or 2.Name\nSelect: ")
            if sc == '1':
                cid = input("ID: ").strip()
                idx = linear_search_cust_id(cid)
                if idx != -1:
                    d = customers[idx]
                    print(f"{d['id']} | {d['name']} | {d['phone']} | {d['email']}")
                else:
                    print("Error: Not found.")
            elif sc == '2':
                name = input("Name: ").strip()
                res = linear_search_cust_name(name)
                if res:
                    for d in res:
                        print(f"{d['id']} | {d['name']} | {d['phone']} | {d['email']}")
                else:
                    print("Error: Not found.")
            else:
                print("Invalid choice.")
        elif c == '4':
            cid = input("ID: ").strip()
            idx = linear_search_cust_id(cid)
            if idx != -1:
                n = input("New Name: ").strip()
                p = input("New Phone: ").strip()
                e = input("New Email: ").strip()
                if n: customers[idx]["name"] = n
                if p: customers[idx]["phone"] = p
                if e: customers[idx]["email"] = e
                print("Customer updated.")
            else: 
                print("Error: Not found.")
        elif c == '5':
            cid = input("ID: ").strip()
            idx = linear_search_cust_id(cid)
            if idx != -1: 
                customers.pop(idx)
                print("Customer deleted.")
            else: 
                print("Error: Not found.")
        elif c == '6':
            sorted_cust = bubble_sort_customers()
            print("--- Customers Sorted A-Z ---")
            if not sorted_cust:
                print("No customers to sort.")
            for d in sorted_cust: 
                print(f"{d['id']} | {d['name']} | {d['phone']} | {d['email']}")
        elif c == '7': 
            break
        else: 
            print("Invalid choice.")

def r_menu():
    while True:
        c = input("\n1.View Rooms 2.Back\nSelect: ")
        if c == '1':
            for r in rooms: 
                print(f"Room {r['no']} | {r['type']} | Available: {r['avail']}")
        elif c == '2': 
            break
        else: 
            print("Invalid choice.")

def res_menu():
    while True:
        c = input("\n1.Add 2.View 3.Search 4.Update 5.Delete 6.Back\nSelect: ")
        if c == '1':
            rid = input("Res ID: ").strip()
            if linear_search_res_id(rid) != -1: 
                print("Error: Reservation ID already exists.")
                continue
            cid = input("Cust ID: ").strip()
            if linear_search_cust_id(cid) == -1: 
                print("Error: Customer not found.")
                continue
            rno = input("Room No: ").strip()
            idx = linear_search_room(rno)
            if idx == -1 or not rooms[idx]["avail"]: 
                print("Error: Room invalid or unavailable.")
                continue
            cin = input("Check In: ").strip()
            cout = input("Check Out: ").strip()
            rooms[idx]["avail"] = False
            reservations.append({"id": rid, "cid": cid, "rno": rno, "in": cin, "out": cout})
            print("Reservation added.")
        elif c == '2':
            for r in reservations: 
                print(f"{r['id']} | Cust: {r['cid']} | Room: {r['rno']} | In: {r['in']} | Out: {r['out']}")
        elif c == '3':
            rid = input("Res ID: ").strip()
            idx = linear_search_res_id(rid)
            if idx != -1:
                r = reservations[idx]
                print(f"{r['id']} | Cust: {r['cid']} | Room: {r['rno']} | In: {r['in']} | Out: {r['out']}")
            else:
                print("Error: Not found.")
        elif c == '4':
            rid = input("Res ID: ").strip()
            idx = linear_search_res_id(rid)
            if idx != -1:
                r = reservations[idx]
                cin = input("New Check In: ").strip()
                cout = input("New Check Out: ").strip()
                if cin: r["in"] = cin
                if cout: r["out"] = cout
                print("Reservation updated.")
            else: 
                print("Error: Not found.")
        elif c == '5':
            rid = input("Res ID: ").strip()
            idx = linear_search_res_id(rid)
            if idx != -1:
                deleted_rno = reservations[idx]["rno"]
                r_idx = linear_search_room(deleted_rno)
                rooms[r_idx]["avail"] = True
                reservations.pop(idx)
                print("Reservation deleted.")
            else: 
                print("Error: Not found.")
        elif c == '6': 
            break
        else: 
            print("Invalid choice.")

def w_menu():
    while True:
        c = input("\n1.Add to Waiting List 2.Remove from Waiting List 3.View 4.Back\nSelect: ")
        if c == '1':
            n = input("Name: ").strip()
            if n: 
                waiting_list.append(n)
                print("Added to waiting list array.")
        elif c == '2':
            if len(waiting_list) > 0:
                served = waiting_list.pop(0) 
                print(f"Removed: {served}")
            else:
                print("Waiting list is empty.")
        elif c == '3':
            if not waiting_list: 
                print("Waiting list is empty.")
            else:
                for i in range(len(waiting_list)): 
                    print(f"{i + 1}. {waiting_list[i]}")
        elif c == '4': 
            break
        else: 
            print("Invalid choice.")

def main():
    while True:
        print("\n===== SMART HOTEL MANAGEMENT SYSTEM =====")
        c = input("1. Customer Management\n2. Reservation Management\n3. Room Management\n4. Waiting List\n5. Exit\nSelect: ")
        if c == '1': c_menu()
        elif c == '2': res_menu()
        elif c == '3': r_menu()
        elif c == '4': w_menu()
        elif c == '5': break
        else: print("Invalid choice.")

if __name__ == "__main__":
    main()