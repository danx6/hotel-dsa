from collections import deque

customers = {}
reservations = []
waiting_queue = deque()
rooms = [
    {"no": "101", "type": "Single", "avail": True}, {"no": "102", "type": "Double", "avail": True},
    {"no": "103", "type": "Single", "avail": True}, {"no": "104", "type": "Double", "avail": True},
    {"no": "105", "type": "Suite", "avail": True}, {"no": "201", "type": "Single", "avail": True},
    {"no": "202", "type": "Double", "avail": True}, {"no": "203", "type": "Single", "avail": True},
    {"no": "204", "type": "Double", "avail": True}, {"no": "205", "type": "Suite", "avail": True}
]

def search_res(res_id):
    for i in range(len(reservations)):
        if reservations[i]["id"] == res_id: 
            return i
    return -1

def sort_cust():
    lst = list(customers.items())
    for i in range(len(lst)):
        for j in range(len(lst) - i - 1):
            if lst[j][1]["name"].lower() > lst[j+1][1]["name"].lower():
                lst[j], lst[j+1] = lst[j+1], lst[j]
    return lst

def get_room(no):
    for i in range(len(rooms)):
        if rooms[i]["no"] == no: 
            return i
    return -1

def c_menu():
    while True:
        c = input("\n1.Add 2.View 3.Search 4.Update 5.Delete 6.Sort 7.Back\nSelect: ")
        if c == '1':
            cid = input("ID: ").strip()
            if cid in customers: 
                print("Error: Exists.")
                continue
            n, p, e = input("Name: ").strip(), input("Phone: ").strip(), input("Email: ").strip()
            if not (cid and n and p and e): 
                print("Error: Empty field.")
                continue
            customers[cid] = {"name": n, "phone": p, "email": e}
            print("Customer added.")
        elif c == '2':
            for cid, d in customers.items(): 
                print(f"{cid} | {d['name']} | {d['phone']} | {d['email']}")
        elif c == '3':
            cid = input("ID: ").strip()
            if cid in customers:
                d = customers[cid]
                print(f"{cid} | {d['name']} | {d['phone']} | {d['email']}")
            else:
                print("Error: Not found.")
        elif c == '4':
            cid = input("ID: ").strip()
            if cid in customers:
                n, p, e = input("New Name: ").strip(), input("New Phone: ").strip(), input("New Email: ").strip()
                if n: customers[cid]["name"] = n
                if p: customers[cid]["phone"] = p
                if e: customers[cid]["email"] = e
                print("Customer updated.")
            else: 
                print("Error: Not found.")
        elif c == '5':
            cid = input("ID: ").strip()
            if cid in customers: 
                del customers[cid]
                print("Customer deleted.")
            else: 
                print("Error: Not found.")
        elif c == '6':
            for cid, d in sort_cust(): 
                print(f"{cid} | {d['name']} | {d['phone']} | {d['email']}")
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
            if search_res(rid) != -1: 
                print("Error: Exists.")
                continue
            cid = input("Cust ID: ").strip()
            if cid not in customers: 
                print("Error: Customer not found.")
                continue
            rno = input("Room No: ").strip()
            idx = get_room(rno)
            if idx == -1 or not rooms[idx]["avail"]: 
                print("Error: Room invalid or unavailable.")
                continue
            cin, cout = input("Check In: ").strip(), input("Check Out: ").strip()
            rooms[idx]["avail"] = False
            reservations.append({"id": rid, "cid": cid, "rno": rno, "in": cin, "out": cout})
            print("Reservation added.")
        elif c == '2':
            for r in reservations: 
                print(f"{r['id']} | Cust: {r['cid']} | Room: {r['rno']} | In: {r['in']} | Out: {r['out']}")
        elif c == '3':
            rid = input("Res ID: ").strip()
            idx = search_res(rid)
            if idx != -1:
                r = reservations[idx]
                print(f"{r['id']} | Cust: {r['cid']} | Room: {r['rno']} | In: {r['in']} | Out: {r['out']}")
            else:
                print("Error: Not found.")
        elif c == '4':
            rid = input("Res ID: ").strip()
            idx = search_res(rid)
            if idx != -1:
                cin, cout = input("New Check In: ").strip(), input("New Check Out: ").strip()
                if cin: reservations[idx]["in"] = cin
                if cout: reservations[idx]["out"] = cout
                print("Reservation updated.")
            else: 
                print("Error: Not found.")
        elif c == '5':
            rid = input("Res ID: ").strip()
            idx = search_res(rid)
            if idx != -1:
                r_idx = get_room(reservations[idx]["rno"])
                rooms[r_idx]["avail"] = True
                reservations.pop(idx)
                print("Reservation deleted.")
            else: 
                print("Error: Not found.")
        elif c == '6': 
            break
        else: 
            print("Invalid choice.")

def q_menu():
    while True:
        c = input("\n1.Add Waiting 2.Serve Next 3.View Queue 4.Back\nSelect: ")
        if c == '1':
            n = input("Name: ").strip()
            if n: 
                waiting_queue.append(n)
                print("Added to queue.")
        elif c == '2':
            if waiting_queue:
                print(f"Now serving: {waiting_queue.popleft()}")
            else:
                print("Queue is empty.")
        elif c == '3':
            if not waiting_queue: 
                print("Queue is empty.")
            for i, n in enumerate(waiting_queue, 1): 
                print(f"{i}. {n}")
        elif c == '4': 
            break
        else: 
            print("Invalid choice.")

def main():
    while True:
        print("\n===== SMART HOTEL MANAGEMENT SYSTEM =====")
        c = input("1. Customer Management\n2. Reservation Management\n3. Room Management\n4. Waiting Queue\n5. Exit\nSelect: ")
        if c == '1': c_menu()
        elif c == '2': res_menu()
        elif c == '3': r_menu()
        elif c == '4': q_menu()
        elif c == '5': break
        else: print("Invalid choice.")

if __name__ == "__main__":
    main()