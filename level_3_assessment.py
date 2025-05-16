import tkinter as tk

# ------------------ Order Class ----------------
class Orders:
    """

    """
    def __init__(self, name, phone_number, adress):
        self.name = name
        self.phone_number = phone_number
        self.adress = adress 

class GUI:
    def __init__(self,root):
        self.root = root
        self.orders = []

        root.title("Ordering System")
        root.geometry("600x600")

        self.label = tk.Label(root, text = "Burritos", font=("Arial",14))
        self.label.pack(pady=20)
    
        self.order_button = tk.Button(root, text="Enter Order", command=enter_order)
        self.order_button.pack(pady=10)
        self.management_button = tk.Button(root, text="Management Summary", command=management_summary)
        self.management_button.pack(pady=10)
        self.kitchen_button = tk.Button(root, text="Kitchen Screen", command=kitchen_summary)
        self.kitchen_button.pack(pady=10)

        # status label
        self.status_label = tk.Label(root,text="", fg="blue")
        self.status_label.pack(pady=20)

        self.track_widgets = [] # Tracks widgets for clearing

def highlight_button(clicked, others):
    clicked.config(bg="lightgreen", activebackground="green")
    for button in others:
        button.config(bg="SystemButtonFace")

        
def enter_order():
    highlight_button(order_button, [kitchen_button, management_button])
    tk.Label(root, text="Name:").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    tk.Label(root, text="Phone Number:").pack()
    phone_number_entry = tk.Entry(root)
    phone_number_entry.pack()

    tk.Label(root, text="Adress:").pack()
    adress_entry = tk.Entry(root)
    adress_entry.pack()


    def place_order():
        name = name_entry.get()
        phone_number = phone_number_entry.get()
        adress = adress_entry.get()
        Orders(name,phone_number,adress)
        status_label.config(text="Order Processed ✅")
        order_button.config(bg="SystemButtonFace")
        name_entry.delete(0,tk.END)
        phone_number_entry.delete(0,tk.END)
        adress_entry.delete(0,tk.END)
        
    
    submit_button = tk.Button(root, text="Submit", command=place_order)
    submit_button.pack(pady=10)


def management_summary():
    highlight_button(management_button, [order_button, kitchen_button])
    tk.Label(root, text="Management Summary").pack()
    close_button = tk.Button(root, text="X", command=clear)
    close_button.pack(pady=5)
    def clear():
        management_button.config(bg="SystemButtonFace")


def kitchen_summary():
    highlight_button(kitchen_button, [order_button, management_button])
    tk.Label(root, text="Kitchen summary").pack()

    
    
# -----------Main window-------------

if __name__ == "__main__":
    root.mainloop()

