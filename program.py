# --- DATA STRUCTURES ---

# Queue Node for Waiting List
class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None

# Queue (FIFO) for Waiting List
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        new_node = QueueNode(data)
        if self.rear is None:
            self.front = self.rear = new_node
            return
        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        if self.front is None:
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp.data
        
    def to_list(self):
        lst = []
        temp = self.front
        while temp:
            lst.append(temp.data)
            temp = temp.next
        return lst

# Linked List Node for Reservations
class ResNode:
    def __init__(self, data):
        self.data = data
        self.next = None

# Linked List for active reservations
class ResLinkedList:
    def __init__(self):
        self.head = None

    def add_res(self, data):
        new_node = ResNode(data)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node

    # Linear Search for reservation
    def search_res(self, res_id):
        curr = self.head
        while curr:
            if curr.data["id"] == res_id:
                return curr.data
            curr = curr.next
        return None

    def delete_res(self, res_id):
        curr = self.head
        prev = None
        while curr:
            if curr.data["id"] == res_id:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                return curr.data
            prev = curr
            curr = curr.next
        return None

    def to_list(self):
        lst = []
        curr = self.head
        while curr:
            lst.append(curr.data)
            curr = curr.next
        return lst

# Hash Table (Python dict) for customers
customers = {}

# Linked List for reservations
reservations = ResLinkedList()

# Queue for waiting list
waiting_queue = Queue()

# Array (List) for fixed rooms
rooms = [
    {"no": "101", "type": "Single", "avail": True}, {"no": "102", "type": "Double", "avail": True},
    {"no": "103", "type": "Single", "avail": True}, {"no": "104", "type": "Double", "avail": True},
    {"no": "105", "type": "Suite", "avail": True}, {"no": "201", "type": "Single", "avail": True},
    {"no": "202", "type": "Double", "avail": True}, {"no": "203", "type": "Single", "avail": True},
    {"no": "204", "type": "Double", "avail": True}, {"no": "205", "type": "Suite", "avail": True}
]


# --- ALGORITHMS ---

# Linear Search: Search Customer by Name
def search_cust_by_name(name):
    results = []
    for cid, info in customers.items():
        if info["name"].lower() == name.lower():
            results.append((cid, info))
    return results

# Linear Search: Scan room array
def get_room(no):
    for i in range(len(rooms)):
        if rooms[i]["no"] == no: 
            return i
    return -1

# Bubble Sort: Sort customers alphabetically
def bubble_sort_customers():
    lst = list(customers.items())
    n = len(lst)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j][1]["name"].lower() > lst[j+1][1]["name"].lower():
                lst[j], lst[j+1] = lst[j+1], lst[j]
    return lst

# Insertion Sort: Sort reservations
def insertion_sort_reservations():
    lst = reservations.to_list()
    for i in range(1, len(lst)):
        key = lst[i]
        j = i - 1
        while j >= 0 and key["id"] < lst[j]["id"]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key
    return lst


# --- MENUS ---

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
            sc = input("Search by: 1.ID or 2.Name\nSelect: ")
            if sc == '1':
                cid = input("ID: ").strip()
                if cid in customers:
                    d = customers[cid]
                    print(f"{cid} | {d['name']} | {d['phone']} | {d['email']}")
                else:
                    print("Error: Not found.")
            elif sc == '2':
                name = input("Name: ").strip()
                res = search_cust_by_name(name)
                if res:
                    for cid, d in res:
                        print(f"{cid} | {d['name']} | {d['phone']} | {d['email']}")
                else:
                    print("Error: Not found.")
            else:
                print("Invalid choice.")
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
            for cid, d in bubble_sort_customers(): 
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
        c = input("\n1.Add 2.View 3.Search 4.Update 5.Delete 6.Sort 7.Back\nSelect: ")
        if c == '1':
            rid = input("Res ID: ").strip()
            if reservations.search_res(rid) is not None: 
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
            reservations.add_res({"id": rid, "cid": cid, "rno": rno, "in": cin, "out": cout})
            print("Reservation added.")
        elif c == '2':
            for r in reservations.to_list(): 
                print(f"{r['id']} | Cust: {r['cid']} | Room: {r['rno']} | In: {r['in']} | Out: {r['out']}")
        elif c == '3':
            rid = input("Res ID: ").strip()
            r = reservations.search_res(rid)
            if r:
                print(f"{r['id']} | Cust: {r['cid']} | Room: {r['rno']} | In: {r['in']} | Out: {r['out']}")
            else:
                print("Error: Not found.")
        elif c == '4':
            rid = input("Res ID: ").strip()
            r = reservations.search_res(rid)
            if r:
                cin, cout = input("New Check In: ").strip(), input("New Check Out: ").strip()
                if cin: r["in"] = cin
                if cout: r["out"] = cout
                print("Reservation updated.")
            else: 
                print("Error: Not found.")
        elif c == '5':
            rid = input("Res ID: ").strip()
            deleted = reservations.delete_res(rid)
            if deleted:
                r_idx = get_room(deleted["rno"])
                rooms[r_idx]["avail"] = True
                print("Reservation deleted.")
            else: 
                print("Error: Not found.")
        elif c == '6': 
            sorted_res = insertion_sort_reservations()
            if not sorted_res:
                print("No reservations to sort.")
            for r in sorted_res:
                print(f"{r['id']} | Cust: {r['cid']} | Room: {r['rno']} | In: {r['in']} | Out: {r['out']}")
        elif c == '7': 
            break
        else: 
            print("Invalid choice.")

def q_menu():
    while True:
        c = input("\n1.Add Waiting 2.Serve Next 3.View Queue 4.Back\nSelect: ")
        if c == '1':
            n = input("Name: ").strip()
            if n: 
                waiting_queue.enqueue(n)
                print("Added to queue.")
        elif c == '2':
            served = waiting_queue.dequeue()
            if served:
                print(f"Now serving: {served}")
            else:
                print("Queue is empty.")
        elif c == '3':
            lst = waiting_queue.to_list()
            if not lst: 
                print("Queue is empty.")
            for i, n in enumerate(lst, 1): 
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