import tkinter as tk


# ------------------ Order Class ----------------
class Orders:
    """

    """
    def __init__(self, name, phone_number, address):
        self.name = name
        self.phone_number = phone_number
        self.address = address 

class GUI:
    def __init__(self,root):
        self.root = root
        self.orders = []

        root.title("Ordering System")
        root.geometry("600x600")

        self.label = tk.Label(root, text = "Burritos", font=("Arial",14))
        self.label.pack(pady=20)
    
        self.order_button = tk.Button(root, text="Enter Order", command=self.enter_order)
        self.order_button.pack(pady=10)
        self.management_button = tk.Button(root, text="Management Summary", command=self.management_summary)
        self.management_button.pack(pady=10)
        self.kitchen_button = tk.Button(root, text="Kitchen Screen", command=self.kitchen_summary)
        self.kitchen_button.pack(pady=10)

        # status label
        self.status_label = tk.Label(root,text="", fg="blue")
        self.status_label.pack(pady=20)

        self.track_widgets = [] # Tracks widgets for clearing

    def clear_widgets(self):
        for widget in self.track_widgets:
            widget.destroy()
        self.track_widgets.clear()

    def highlight_button(self, clicked, others):
        clicked.config(bg="lightgreen", activebackground="green")
        for button in others:
            button.config(bg="SystemButtonFace")

            
    def enter_order(self):
        self.clear_widgets()
        self.highlight_button(self.order_button, [self.kitchen_button, self.management_button])
        name_label=tk.Label(self.root, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack()

        phone_number_label=tk.Label(self.root, text="Phone Number:")
        phone_number_label.pack()
        phone_number_entry = tk.Entry(self.root)
        phone_number_entry.pack()

        address_label = tk.Label(self.root, text="Address:")
        address_label.pack()
        address_entry = tk.Entry(self.root)
        address_entry.pack()


        def place_order():
            name = name_entry.get()
            phone_number = phone_number_entry.get()
            address = address_entry.get()
            Orders(name,phone_number,address)
            self.status_label.config(text="Order Processed ✅")
            self.order_button.config(bg="SystemButtonFace")
            name_entry.delete(0,tk.END)
            phone_number_entry.delete(0,tk.END)
            address_entry.delete(0,tk.END)
            self.root.after(2000,lambda:self.status_label.config(text="")) # lambda calls a simple one line function
            
        
        submit_button = tk.Button(self.root, text="Submit", command=place_order)
        submit_button.pack(pady=10)

        self.track_widgets += [
            name_label, name_entry,
            phone_number_label,phone_number_entry,
            address_label,address_entry,
            submit_button,
        ]


    def management_summary(self):
        self.clear_widgets()
        self.highlight_button(self.management_button, [self.order_button, self.kitchen_button])
        tk.Label(self.root, text="Management Summary").pack()
        def clear():
            self.management_button.config(bg="SystemButtonFace")


    def kitchen_summary(self):
        self.clear_widgets()
        self.highlight_button(self.kitchen_button, [self.order_button, self.management_button])
        tk.Label(self.root, text="Kitchen summary").pack()
    
# -----------Main window-------------

if __name__ == "__main__":
    root= tk.Tk()
    run_gui = GUI(root)
    root.attributes('-topmost', True)
    root.mainloop()

