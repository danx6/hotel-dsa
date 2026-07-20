
import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

# ---------------- Data Structures ----------------
customers = {}

rooms = [
    {"room": "101", "type": "Single", "available": True},
    {"room": "102", "type": "Single", "available": True},
    {"room": "103", "type": "Double", "available": True},
    {"room": "104", "type": "Double", "available": True},
    {"room": "105", "type": "Deluxe", "available": True},
    {"room": "106", "type": "Deluxe", "available": True},
    {"room": "107", "type": "Suite", "available": True},
    {"room": "108", "type": "Suite", "available": True},
    {"room": "109", "type": "Single", "available": True},
    {"room": "110", "type": "Double", "available": True},
]

reservations = {}
waiting_list = deque()
reservation_counter = 1

# ---------------- Linear Search: Customer ----------------
def linear_search_customer(cust_id):
    for key in customers:
        if key == cust_id:
            return customers[key]
    return None

# ---------------- Linear Search: Reservation ----------------
def linear_search_reservation(res_id):
    for key in reservations:
        if key == res_id:
            return reservations[key]
    return None

# ---------------- Linear Search: Room ----------------
def find_room(room_no):
    for r in rooms:
        if r["room"] == room_no:
            return r
    return None

# ---------------- Bubble Sort Customers ----------------
def bubble_sort_customers():
    ids = list(customers.keys())
    n = len(ids)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            name1 = customers[ids[j]]["name"].lower()
            name2 = customers[ids[j + 1]]["name"].lower()
            if name1 > name2:
                ids[j], ids[j + 1] = ids[j + 1], ids[j]
    return ids

# ---------------- Add Customer ----------------
def add_customer():
    cust_id = entry_cust_id.get().strip()
    name = entry_cust_name.get().strip()
    phone = entry_cust_phone.get().strip()
    email = entry_cust_email.get().strip()

    if cust_id == "" or name == "" or phone == "" or email == "":
        messagebox.showerror("Error", "All customer fields must be filled.")
        return

    if linear_search_customer(cust_id) is not None:
        messagebox.showerror("Error", "Customer ID already exists.")
        return

    customers[cust_id] = {"name": name, "phone": phone, "email": email}
    messagebox.showinfo("Success", "Customer added successfully.")
    clear_customer_fields()
    refresh_customer_table()

# ---------------- Update Customer ----------------
def update_customer():
    cust_id = entry_cust_id.get().strip()
    name = entry_cust_name.get().strip()
    phone = entry_cust_phone.get().strip()
    email = entry_cust_email.get().strip()

    if cust_id == "":
        messagebox.showerror("Error", "Please enter Customer ID to update.")
        return

    cust = linear_search_customer(cust_id)
    if cust is None:
        messagebox.showerror("Error", "Customer ID not found.")
        return

    if name == "" or phone == "" or email == "":
        messagebox.showerror("Error", "All customer fields must be filled.")
        return

    customers[cust_id]["name"] = name
    customers[cust_id]["phone"] = phone
    customers[cust_id]["email"] = email
    messagebox.showinfo("Success", "Customer updated successfully.")
    clear_customer_fields()
    refresh_customer_table()

# ---------------- Delete Customer ----------------
def delete_customer():
    cust_id = entry_cust_id.get().strip()
    if cust_id == "":
        messagebox.showerror("Error", "Please enter Customer ID to delete.")
        return

    cust = linear_search_customer(cust_id)
    if cust is None:
        messagebox.showerror("Error", "Customer ID not found.")
        return

    del customers[cust_id]
    messagebox.showinfo("Success", "Customer deleted successfully.")
    clear_customer_fields()
    refresh_customer_table()

# ---------------- Search Customer ----------------
def search_customer():
    cust_id = entry_cust_id.get().strip()
    if cust_id == "":
        messagebox.showerror("Error", "Please enter Customer ID to search.")
        return

    cust = linear_search_customer(cust_id)
    if cust is None:
        messagebox.showerror("Error", "Customer ID not found.")
        return

    for row in customer_tree.get_children():
        customer_tree.delete(row)
    customer_tree.insert("", "end", values=(cust_id, cust["name"], cust["phone"], cust["email"]))

# ---------------- Sort Customers ----------------
def sort_customers():
    sorted_ids = bubble_sort_customers()
    for row in customer_tree.get_children():
        customer_tree.delete(row)
    for cid in sorted_ids:
        cust = customers[cid]
        customer_tree.insert("", "end", values=(cid, cust["name"], cust["phone"], cust["email"]))

# ---------------- Clear Customer Fields ----------------
def clear_customer_fields():
    entry_cust_id.delete(0, tk.END)
    entry_cust_name.delete(0, tk.END)
    entry_cust_phone.delete(0, tk.END)
    entry_cust_email.delete(0, tk.END)

# ---------------- Refresh Customer Table ----------------
def refresh_customer_table():
    for row in customer_tree.get_children():
        customer_tree.delete(row)
    for cid in customers:
        cust = customers[cid]
        customer_tree.insert("", "end", values=(cid, cust["name"], cust["phone"], cust["email"]))

# ---------------- Refresh Room Table ----------------
def refresh_room_table():
    for row in room_tree.get_children():
        room_tree.delete(row)
    for r in rooms:
        status = "Available" if r["available"] else "Occupied"
        room_tree.insert("", "end", values=(r["room"], r["type"], status))

# ---------------- Add Reservation ----------------
def add_reservation():
    global reservation_counter
    cust_id = entry_res_custid.get().strip()
    room_no = entry_res_room.get().strip()
    check_in = entry_res_checkin.get().strip()
    check_out = entry_res_checkout.get().strip()

    if cust_id == "" or room_no == "" or check_in == "" or check_out == "":
        messagebox.showerror("Error", "All reservation fields must be filled.")
        return

    cust = linear_search_customer(cust_id)
    if cust is None:
        messagebox.showerror("Error", "Customer ID does not exist.")
        return

    room = find_room(room_no)
    if room is None:
        messagebox.showerror("Error", "Room number does not exist.")
        return

    if not room["available"]:
        messagebox.showerror("Error", "Room is not available.")
        return

    res_id = "R" + str(reservation_counter).zfill(3)
    reservation_counter += 1

    reservations[res_id] = {
        "cust_id": cust_id,
        "room": room_no,
        "checkin": check_in,
        "checkout": check_out
    }
    room["available"] = False

    messagebox.showinfo("Success", "Reservation added as " + res_id)
    clear_reservation_fields()
    refresh_reservation_table()
    refresh_room_table()

# ---------------- Update Reservation ----------------
def update_reservation():
    res_id = entry_res_id.get().strip()
    if res_id == "":
        messagebox.showerror("Error", "Please enter Reservation ID to update.")
        return

    res = linear_search_reservation(res_id)
    if res is None:
        messagebox.showerror("Error", "Reservation ID not found.")
        return

    check_in = entry_res_checkin.get().strip()
    check_out = entry_res_checkout.get().strip()

    if check_in == "" or check_out == "":
        messagebox.showerror("Error", "Check In and Check Out fields must be filled.")
        return

    res["checkin"] = check_in
    res["checkout"] = check_out
    messagebox.showinfo("Success", "Reservation updated successfully.")
    clear_reservation_fields()
    refresh_reservation_table()

# ---------------- Delete Reservation ----------------
def delete_reservation():
    res_id = entry_res_id.get().strip()
    if res_id == "":
        messagebox.showerror("Error", "Please enter Reservation ID to delete.")
        return

    res = linear_search_reservation(res_id)
    if res is None:
        messagebox.showerror("Error", "Reservation ID not found.")
        return

    room = find_room(res["room"])
    if room is not None:
        room["available"] = True

    del reservations[res_id]
    messagebox.showinfo("Success", "Reservation deleted successfully.")
    clear_reservation_fields()
    refresh_reservation_table()
    refresh_room_table()

# ---------------- Search Reservation ----------------
def search_reservation():
    res_id = entry_res_id.get().strip()
    if res_id == "":
        messagebox.showerror("Error", "Please enter Reservation ID to search.")
        return

    res = linear_search_reservation(res_id)
    if res is None:
        messagebox.showerror("Error", "Reservation ID not found.")
        return

    for row in reservation_tree.get_children():
        reservation_tree.delete(row)
    reservation_tree.insert("", "end", values=(res_id, res["cust_id"], res["room"], res["checkin"], res["checkout"]))

# ---------------- Clear Reservation Fields ----------------
def clear_reservation_fields():
    entry_res_id.delete(0, tk.END)
    entry_res_custid.delete(0, tk.END)
    entry_res_room.delete(0, tk.END)
    entry_res_checkin.delete(0, tk.END)
    entry_res_checkout.delete(0, tk.END)

# ---------------- Refresh Reservation Table ----------------
def refresh_reservation_table():
    for row in reservation_tree.get_children():
        reservation_tree.delete(row)
    for rid in reservations:
        res = reservations[rid]
        reservation_tree.insert("", "end", values=(rid, res["cust_id"], res["room"], res["checkin"], res["checkout"]))

# ---------------- Add Waiting Customer ----------------
def add_waiting_customer():
    name = entry_wait_name.get().strip()
    if name == "":
        messagebox.showerror("Error", "Please enter customer name for waiting list.")
        return
    waiting_list.append(name)
    entry_wait_name.delete(0, tk.END)
    refresh_waiting_table()
    messagebox.showinfo("Success", name + " added to waiting list.")

# ---------------- Serve Next Customer ----------------
def serve_next_customer():
    if len(waiting_list) == 0:
        messagebox.showerror("Error", "Waiting list is empty.")
        return
    served = waiting_list.popleft()
    refresh_waiting_table()
    messagebox.showinfo("Served", served + " has been served.")

# ---------------- Refresh Waiting Table ----------------
def refresh_waiting_table():
    for row in waiting_tree.get_children():
        waiting_tree.delete(row)
    position = 1
    for name in waiting_list:
        waiting_tree.insert("", "end", values=(position, name))
        position += 1

# ---------------- Main Window Setup ----------------
root = tk.Tk()
root.title("Smart Hotel Management System")
root.geometry("1000x650")
root.configure(bg="white")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ================= CUSTOMER TAB =================
customer_tab = tk.Frame(notebook, bg="white")
notebook.add(customer_tab, text="Customers")

cust_form = tk.Frame(customer_tab, bg="white")
cust_form.pack(pady=10)

tk.Label(cust_form, text="Customer ID", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_cust_id = tk.Entry(cust_form, width=20)
entry_cust_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(cust_form, text="Name", bg="white").grid(row=0, column=2, padx=5, pady=5, sticky="e")
entry_cust_name = tk.Entry(cust_form, width=20)
entry_cust_name.grid(row=0, column=3, padx=5, pady=5)

tk.Label(cust_form, text="Phone", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_cust_phone = tk.Entry(cust_form, width=20)
entry_cust_phone.grid(row=1, column=1, padx=5, pady=5)

tk.Label(cust_form, text="Email", bg="white").grid(row=1, column=2, padx=5, pady=5, sticky="e")
entry_cust_email = tk.Entry(cust_form, width=20)
entry_cust_email.grid(row=1, column=3, padx=5, pady=5)

cust_btn_frame = tk.Frame(customer_tab, bg="white")
cust_btn_frame.pack(pady=5)

tk.Button(cust_btn_frame, text="Add Customer", width=15, command=add_customer).grid(row=0, column=0, padx=5)
tk.Button(cust_btn_frame, text="Update Customer", width=15, command=update_customer).grid(row=0, column=1, padx=5)
tk.Button(cust_btn_frame, text="Delete Customer", width=15, command=delete_customer).grid(row=0, column=2, padx=5)
tk.Button(cust_btn_frame, text="Search Customer", width=15, command=search_customer).grid(row=0, column=3, padx=5)
tk.Button(cust_btn_frame, text="Sort Customers", width=15, command=sort_customers).grid(row=0, column=4, padx=5)
tk.Button(cust_btn_frame, text="Clear", width=15, command=clear_customer_fields).grid(row=0, column=5, padx=5)

customer_tree = ttk.Treeview(customer_tab, columns=("id", "name", "phone", "email"), show="headings", height=15)
customer_tree.heading("id", text="Customer ID")
customer_tree.heading("name", text="Name")
customer_tree.heading("phone", text="Phone")
customer_tree.heading("email", text="Email")
customer_tree.pack(fill="both", expand=True, padx=10, pady=10)

# ================= ROOM TAB =================
room_tab = tk.Frame(notebook, bg="white")
notebook.add(room_tab, text="Rooms")

room_tree = ttk.Treeview(room_tab, columns=("room", "type", "status"), show="headings", height=20)
room_tree.heading("room", text="Room Number")
room_tree.heading("type", text="Room Type")
room_tree.heading("status", text="Availability")
room_tree.pack(fill="both", expand=True, padx=10, pady=10)

# ================= RESERVATION TAB =================
res_tab = tk.Frame(notebook, bg="white")
notebook.add(res_tab, text="Reservations")

res_form = tk.Frame(res_tab, bg="white")
res_form.pack(pady=10)

tk.Label(res_form, text="Reservation ID", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_res_id = tk.Entry(res_form, width=20)
entry_res_id.grid(row=0, column=1, padx=5, pady=5)

tk.Label(res_form, text="Customer ID", bg="white").grid(row=0, column=2, padx=5, pady=5, sticky="e")
entry_res_custid = tk.Entry(res_form, width=20)
entry_res_custid.grid(row=0, column=3, padx=5, pady=5)

tk.Label(res_form, text="Room Number", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_res_room = tk.Entry(res_form, width=20)
entry_res_room.grid(row=1, column=1, padx=5, pady=5)

tk.Label(res_form, text="Check In", bg="white").grid(row=1, column=2, padx=5, pady=5, sticky="e")
entry_res_checkin = tk.Entry(res_form, width=20)
entry_res_checkin.grid(row=1, column=3, padx=5, pady=5)

tk.Label(res_form, text="Check Out", bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_res_checkout = tk.Entry(res_form, width=20)
entry_res_checkout.grid(row=2, column=1, padx=5, pady=5)

res_btn_frame = tk.Frame(res_tab, bg="white")
res_btn_frame.pack(pady=5)

tk.Button(res_btn_frame, text="Add Reservation", width=15, command=add_reservation).grid(row=0, column=0, padx=5)
tk.Button(res_btn_frame, text="Update Reservation", width=15, command=update_reservation).grid(row=0, column=1, padx=5)
tk.Button(res_btn_frame, text="Delete Reservation", width=15, command=delete_reservation).grid(row=0, column=2, padx=5)
tk.Button(res_btn_frame, text="Search Reservation", width=15, command=search_reservation).grid(row=0, column=3, padx=5)
tk.Button(res_btn_frame, text="Clear", width=15, command=clear_reservation_fields).grid(row=0, column=4, padx=5)

reservation_tree = ttk.Treeview(res_tab, columns=("id", "custid", "room", "checkin", "checkout"), show="headings", height=13)
reservation_tree.heading("id", text="Reservation ID")
reservation_tree.heading("custid", text="Customer ID")
reservation_tree.heading("room", text="Room Number")
reservation_tree.heading("checkin", text="Check In")
reservation_tree.heading("checkout", text="Check Out")
reservation_tree.pack(fill="both", expand=True, padx=10, pady=10)

# ================= WAITING QUEUE TAB =================
wait_tab = tk.Frame(notebook, bg="white")
notebook.add(wait_tab, text="Waiting Queue")

wait_form = tk.Frame(wait_tab, bg="white")
wait_form.pack(pady=10)

tk.Label(wait_form, text="Customer Name", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_wait_name = tk.Entry(wait_form, width=25)
entry_wait_name.grid(row=0, column=1, padx=5, pady=5)

wait_btn_frame = tk.Frame(wait_tab, bg="white")
wait_btn_frame.pack(pady=5)

tk.Button(wait_btn_frame, text="Add Waiting Customer", width=20, command=add_waiting_customer).grid(row=0, column=0, padx=5)
tk.Button(wait_btn_frame, text="Serve Next Customer", width=20, command=serve_next_customer).grid(row=0, column=1, padx=5)

waiting_tree = ttk.Treeview(wait_tab, columns=("pos", "name"), show="headings", height=18)
waiting_tree.heading("pos", text="Position")
waiting_tree.heading("name", text="Customer Name")
waiting_tree.pack(fill="both", expand=True, padx=10, pady=10)

# ---------------- Initial Load ----------------
refresh_room_table()
refresh_customer_table()
refresh_reservation_table()
refresh_waiting_table()

root.mainloop()
