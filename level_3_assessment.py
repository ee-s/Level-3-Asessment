import tkinter as tk
from tkinter import ttk
import json

REGULAR_PRICE = 8.5
DELIVERY_PRICE = 2.5
HIGHER_PRICE = 13.5
# ------------------ Order Class ---------------
class Orders:
    def __init__(self, name, phone_number, address, burritos, delivery):
        self.name = name
        self.phone_number = phone_number
        self.address = address 
        self.burritos = burritos
        self.delivery = delivery

class GUI:
    def __init__(self, root):
        self.root = root
        self.orders = []

        root.title("Ordering System")
        root.geometry("600x600")

        self.label = tk.Label(root, text="Burritos", font=("Arial", 14))
        self.label.pack(pady=20)
    
        self.order_button = tk.Button(root, text="Enter Order", command=self.enter_order)
        self.order_button.pack(pady=10)
        self.management_button = tk.Button(root, text="Management Summary", command=self.management_summary)
        self.management_button.pack(pady=10)
        self.kitchen_button = tk.Button(root, text="Kitchen Screen", command=self.kitchen_summary)
        self.kitchen_button.pack(pady=10)

        # status label
        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.pack(pady=20)
        self.status_label.config(text="Welcome to the burrito ordering system", fg="blue")

        self.track_widgets = []  # Tracks widgets for clearing
        self.delivery_variable = tk.BooleanVar()
        self.burrito_boxes = []

    def select_burritos(self, burrito_count):
            select_burritos_label = tk.Label(self.root,text="Select burrito types" )
            select_burritos_label.pack()
            self.track_widgets.append(select_burritos_label)            
            regular_burrito = [["Cheese", REGULAR_PRICE], ["Plain", REGULAR_PRICE], ["Spicy", REGULAR_PRICE]]
            higher_burrito= [["Deluxe", HIGHER_PRICE],["Large", HIGHER_PRICE],["Gourmet", HIGHER_PRICE]]

            burrito_types= higher_burrito + regular_burrito
            burrito_types = [f"{name} - ${price:.2f}" for name,price in burrito_types]
            for burrito in range(burrito_count):
                var = tk.StringVar()
                burrito_menu = ttk.Combobox(self.root, textvariable=var, values=burrito_types)
                burrito_menu.pack(pady=10)
                self.track_widgets.append(burrito_menu)
                self.burrito_boxes.append(var)
            
            confirm_button = tk.Button(self.root, text="Confirm", command=lambda: self.process_burrito_selection)
            confirm_button.pack(pady=10)
            self.track_widgets.append(confirm_button)

    def process_burrito_selection(self):
        selected_burritos = [ver.get() for ver in self.burrito_boxes]
        if all(selected_burritos):
            self.store_order(selected_burritos)
            self.status_label.config(text="Order placed successfully ✅", fg="green")
            self.root.after(2000, lambda: self.status_label.config(text=""))
            self.clear_widgets()
        else:
            self.status_label.config(text="❌ Please select all burrito types ❌", fg="darkred")
            self.root.after(2000, lambda: self.status_label.config(text=""))


    def clear_widgets(self):
        for widget in self.track_widgets:
            widget.destroy()
        self.track_widgets.clear()

    def highlight_button(self, clicked, others):
        clicked.config(bg="lightgreen", activebackground="green")
        for button in others:
            button.config(bg="SystemButtonFace", activebackground="SystemButtonFace")

    def get_burrito_amount(self):
        self.clear_widgets()

        burrito_label = tk.Label(self.root, text="How many burritos?")
        burrito_label.pack()

        self.burrito_count_entry = tk.Entry(self.root)
        self.burrito_count_entry.pack()

        enter_button = tk.Button(self.root, text="Enter", command=self.process_burrito_count)
        enter_button.pack(pady=10)

        self.track_widgets += [burrito_label, self.burrito_count_entry, enter_button]

    def process_burrito_count(self):
        burrito_count = self.burrito_count_entry.get().strip()
        if burrito_count.isdigit():
            count = int(burrito_count)
            if 0 < count < 10:
                self.burrito_count = count
                self.status_label.config(text=f"Ordering {self.burrito_count} burritos", fg="green")
                self.burrito_count_entry.delete(0, tk.END)
                self.clear_widgets()

                self.select_burritos(self.burrito_count)

                self.status_label.config(text=" Order Processed ✅", fg="green")
                self.root.after(2000, lambda: self.status_label.config(text=""))
                self.order_button.config(bg="SystemButtonFace")
                return burrito_count

        self.status_label.config(text="❌ Enter a valid number of burritos ❌", fg="darkred")
        self.root.after(2000, lambda: self.status_label.config(text=""))

# ---------- Add -----------
    def enter_order(self):
        self.clear_widgets()
        self.highlight_button(self.order_button, [self.kitchen_button, self.management_button])

        name_label = tk.Label(self.root, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack()

        def hide_delivery_variables():
            if self.delivery_variable.get():
                phone_number_label.pack()
                phone_number_entry.pack()
                address_label.pack()
                address_entry.pack()
            else:
                phone_number_label.pack_forget()
                phone_number_entry.pack_forget()
                address_label.pack_forget()
                address_entry.pack_forget()

        delivery_checkbox = tk.Checkbutton(self.root, text="Delivery? \n(+2.50$)", variable=self.delivery_variable,
                                           command=hide_delivery_variables)
        delivery_checkbox.pack()

        phone_number_label = tk.Label(self.root, text="Phone Number:")
        phone_number_entry = tk.Entry(self.root)
        address_label = tk.Label(self.root, text="Address:")
        address_entry = tk.Entry(self.root)

        hide_delivery_variables()

        def place_order():
            name = name_entry.get().strip()
            if not name or name.isdigit():
                self.status_label.config(text="❌ Enter valid name ❌", fg="darkred")
                self.root.after(3000, lambda: self.status_label.config(text=""))
                return
            if self.delivery_variable.get():
                phone_number = phone_number_entry.get().strip()
                address = address_entry.get().strip()
                if not phone_number or not (7 <= len(phone_number) <= 18):
                    self.status_label.config(text="❌ Enter valid phone number ❌", fg="darkred")
                    self.root.after(3000, lambda: self.status_label.config(text=""))
                    return
                if not address or address.isdigit():
                    self.status_label.config(text="❌ Enter valid address ❌", fg="darkred")
                    self.root.after(3000, lambda: self.status_label.config(text=""))
                    return
            else:
                phone_number = "N/A"
                address = "N/A"

            self.store_name = name
            self.store_phone_number = phone_number
            self.store_address = address

            # Clear widgets after processing
            self.clear_widgets()

            # Ask for burrito count after details are entered
            self.get_burrito_amount()

        submit_button = tk.Button(self.root, text="Submit", command=place_order)
        submit_button.pack(pady=10)

        self.track_widgets += [
            name_label, name_entry,
            phone_number_label, phone_number_entry,
            address_label, address_entry,
            delivery_checkbox, submit_button]

    def management_summary(self):
        self.clear_widgets()
        self.highlight_button(self.management_button, [self.order_button, self.kitchen_button])
        management_label = tk.Label(self.root, text="Management Summary")
        management_label.pack()
        self.track_widgets += [management_label]

        for order in self.orders:
            management_info_label = tk.Label(self.root, text=f"Name: {order.name}\nPhone: {order.phone_number}\nAddress: {order.address}")
            management_info_label.pack()
            self.track_widgets.append(management_info_label)

    def kitchen_summary(self):
        self.clear_widgets()
        self.highlight_button(self.kitchen_button, [self.order_button, self.management_button])
        kitchen_label = tk.Label(self.root, text="Kitchen summary")
        kitchen_label.pack()
        self.track_widgets += [kitchen_label]

        for order in self.orders:
            kitchen_info_label = tk.Label(self.root,
                                           text=f"Name: {order.name}- Address: {order.address}")
            kitchen_info_label.pack()
            self.track_widgets.append(kitchen_info_label)

    def store_order(self, burritos):
        order = Orders(
            name=self.store_name,
            phone_number = self.store_phone_number,
            address = self.store_address,
            burritos = self.burrito_count,
            delivery = self.delivery_variable.get())
        self.orders.append(order)
        self.save_orders_file()

    def save_orders_file(self):
        with open("orders.json", "w") as f:
            json.dump([order.__dict__ for order in self.orders], f, indent=4)
            print("Orders saved!")

# ----------- Main -------------
if __name__ == "__main__":
    root = tk.Tk()
    run_gui = GUI(root)
    root.attributes('-topmost', True)
    root.mainloop()