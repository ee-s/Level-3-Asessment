import tkinter as tk

# ------------------ Order Class ----------------
class Order:
    def __init__(self, name, phone_number, address):
        self.name = name
        self.phone_number = phone_number
        self.address = address

# ------------------ App Class ----------------
class OrderApp:
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

        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.pack(pady=20)

        self.dynamic_widgets = []  # Track widgets to be cleared

    def clear_screen(self):
        for widget in self.dynamic_widgets:
            widget.destroy()
        self.dynamic_widgets.clear()

    def highlight_button(self, clicked, others):
        clicked.config(bg="lightgreen", activebackground="green")
        for button in others:
            button.config(bg="SystemButtonFace")

    def enter_order(self):
        self.clear_screen()
        self.highlight_button(self.order_button, [self.kitchen_button, self.management_button])

        name_label = tk.Label(self.root, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack()

        phone_label = tk.Label(self.root, text="Phone Number:")
        phone_label.pack()
        phone_entry = tk.Entry(self.root)
        phone_entry.pack()

        address_label = tk.Label(self.root, text="Address:")
        address_label.pack()
        address_entry = tk.Entry(self.root)
        address_entry.pack()

        def place_order():
            name = name_entry.get()
            phone = phone_entry.get()
            address = address_entry.get()

            if name and phone and address:
                self.orders.append(Order(name, phone, address))
                self.status_label.config(text="Order Processed ✅")

                # Clear the input fields
                name_entry.delete(0, tk.END)
                phone_entry.delete(0, tk.END)
                address_entry.delete(0, tk.END)

            else:
                self.status_label.config(text="Please fill in all fields", fg="red")

        submit_button = tk.Button(self.root, text="Submit", command=place_order)
        submit_button.pack(pady=10)

        # Track widgets for cleanup
        self.dynamic_widgets += [
            name_label, name_entry,
            phone_label, phone_entry,
            address_label, address_entry,
            submit_button
        ]

    def management_summary(self):
        self.clear_screen()
        self.highlight_button(self.management_button, [self.order_button, self.kitchen_button])
        label = tk.Label(self.root, text="Management Summary")
        label.pack()
        self.dynamic_widgets.append(label)

    def kitchen_summary(self):
        self.clear_screen()
        self.highlight_button(self.kitchen_button, [self.order_button, self.management_button])
        label = tk.Label(self.root, text="Kitchen Summary")
        label.pack()
        self.dynamic_widgets.append(label)

# ------------------ Main ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = OrderApp(root)
    root.mainloop()
