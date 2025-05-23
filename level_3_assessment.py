""""
Eliza Smith
21206
23/05/2025
Burrito ordering system expressed with a GUI
"""

# Importing libararies
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

# Constants for prices
REGULAR_PRICE = 8.5
DELIVERY_PRICE = 2.5
HIGHER_PRICE = 13.5


# ------------------ Order Class ------------------
class Orders:
    def __init__(self, name, phone_number, address, burritos, delivery):
        """
        

        """
        self.name = name
        self.phone_number = phone_number
        self.address = address 
        self.burritos = burritos
        self.delivery = delivery

#------------------- GUI Class ------------------
class GUI:
    """

    """
    def __init__(self, root):
        """
        
        """
        self.root = root
        self.orders = []

        root.title("Ordering System")
        root.geometry("600x600")

        self.label = tk.Label(root, text="Burritos")
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
        self.status_label.config(text="Burrito ordering system", fg="blue")

        self.track_widgets = []  # Tracks widgets for clearing
        self.delivery_variable = tk.BooleanVar()
        self.burrito_boxes = []

    def info_pop_up(self, message, color= "orange", duration=2000):
        self.status_label.config(text=message, fg=color)
        self.root.after(duration, lambda: self.status_label.config(text=""))


    def select_burritos(self, burrito_count):
            """

            """
            select_burritos_label = tk.Label(self.root,text="Select burrito types" )
            select_burritos_label.pack()
            self.track_widgets.append(select_burritos_label)            
            burrito_types= [["Cheese", REGULAR_PRICE], ["Plain", REGULAR_PRICE], ["Spicy", REGULAR_PRICE],
                            ["Deluxe", HIGHER_PRICE],["Large", HIGHER_PRICE],["Gourmet", HIGHER_PRICE]]
            burrito_types = [f"{name} - ${price:.2f}" for name,price in burrito_types]
            for burrito in range(burrito_count):
                var = tk.StringVar()
                burrito_menu = ttk.Combobox(self.root, textvariable=var, values=burrito_types)
                burrito_menu.set("Select a burrito")
                burrito_menu.pack(pady=10)
                burrito_menu.bind("<<ComboboxSelected>>", lambda event: self.updateprice_total())
                self.track_widgets.append(burrito_menu)
                self.burrito_boxes.append(var)
            
            self.price_label = tk.Label(self.root, text="Total Price: $0.00")
            self.price_label.pack(pady=10)
            self.track_widgets.append(self.price_label)
                   
            confirm_button = tk.Button(self.root, text="Confirm", command=self.process_burrito_selection)
            confirm_button.pack(pady=10)
            self.track_widgets.append(confirm_button)

    def process_burrito_selection(self):
        """
        
        """
        selected_burritos = [ver.get() for ver in self.burrito_boxes]
        if all(selected_burritos):

            if messagebox.askyesno("Confirm Order", "Do you want to place this order?"):
                self.store_order(selected_burritos)
                self.info_pop_up("Order placed ✅", "darkgreen")
                self.clear_widgets()
                self.burrito_boxes.clear()

            else: 
                self.info_pop_up("Order cancelled ❌", "darkred")
                self.clear_widgets()
                self.burrito_boxes.clear()

        else:
            self.info_pop_up("❌ Please select all burrito types ❌", "darkred")
           
        back_btn = tk.Button(self.root, text="Back", command=self.back_to_main)
        back_btn.pack()
        self.track_widgets.append(back_btn)

    def updateprice_total(self):
        """
        
        """
        total_price = 0
        for var in self.burrito_boxes:
            cost = var.get()
            if "Deluxe" in cost or "Large" in cost or "Gourmet" in cost:
                total_price += HIGHER_PRICE
            elif "Cheese" in cost or "Plain" in cost or "Spicy" in cost:
                total_price += REGULAR_PRICE
        if self.delivery_variable.get():
            total_price += DELIVERY_PRICE
        self.price_label.config(text=f"Total Price: ${total_price:.2f}")
        self.price_label.pack(pady=10)

        return total_price
            
    def clear_widgets(self):
        """
        
        """
        for widget in self.track_widgets:
            widget.destroy()
        self.track_widgets.clear()

    def highlight_button(self, clicked, others):
        """

        """
        clicked.config(bg="lightgreen", activebackground="green")
        for button in others:
            button.config(bg="SystemButtonFace", activebackground="SystemButtonFace")

    def get_burrito_amount(self):
        """

        """
        self.clear_widgets()

        burrito_label = tk.Label(self.root, text="How many burritos?")
        burrito_label.pack()

        self.burrito_count_entry = tk.Entry(self.root)
        self.burrito_count_entry.pack()

        enter_button = tk.Button(self.root, text="Enter", command=self.process_burrito_count)
        enter_button.pack(pady=10)

        self.track_widgets += [burrito_label, self.burrito_count_entry, enter_button]

    def process_burrito_count(self):
        """
        
        """
        burrito_count = self.burrito_count_entry.get().strip()
        if burrito_count.isdigit():
            count = int(burrito_count)
            if 0 < count < 10:
                self.burrito_count = count
                self.status_label.config(text=f"Ordering {self.burrito_count} burritos", fg="green")
                self.burrito_count_entry.delete(0, tk.END)
                self.clear_widgets()

                self.select_burritos(self.burrito_count)
                self.info_pop_up("Processed ✅", "darkgreen")
                self.order_button.config(bg="SystemButtonFace")
                return burrito_count
        self.info_pop_up("❌ Invalid number of burritos 1-9 ❌", "darkred")
       
    def delete_order(self, order_index):
        """
        
        """
        if 0 <= order_index < len(self.orders):
            if messagebox.askyesno("Confirm deletion", "Do you want to delete this order?"):
                del self.orders[order_index]
                self.info_pop_up("Order deleted ✅", "darkgreen")
                self.clear_widgets()
            else: 
                self.info_pop_up("Order not deleted ❌", "darkred")
                
    def back_to_main(self):
        """
        
        """
        self.clear_widgets()
        self.info_pop_up("Going to main menu", "darkorange")
    def enter_order(self):
        """
        
        """
        self.clear_widgets()
        self.highlight_button(self.order_button, [self.kitchen_button, self.management_button])

        name_label = tk.Label(self.root, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack()

        def hide_delivery_variables():
            """
            
            """
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

        delivery_checkbox = tk.Checkbutton(self.root, text="""Delivery? (+2.50$)""", variable=self.delivery_variable,
                                           command=hide_delivery_variables)
        delivery_checkbox.pack()

        phone_number_label = tk.Label(self.root, text="Phone Number: ")
        phone_number_entry = tk.Entry(self.root)
        address_label = tk.Label(self.root, text="Address: ")
        address_entry = tk.Entry(self.root)

        hide_delivery_variables()

        def place_order():
            """
            
            """
            back_btn = tk.Button(self.root, text="Back", command=self.back_to_main)
            back_btn.pack()
            self.track_widgets.append(back_btn)
            name = name_entry.get().strip()
            if not name or name.isdigit():
                self.info_pop_up("❌ Enter valid name ❌", "darkred")
                return
            
            if self.delivery_variable.get():
                phone_number = phone_number_entry.get().strip()
                address = address_entry.get().strip()
                if not phone_number or not (7 <= len(phone_number) <= 18):
                    self.info_pop_up("❌ Enter valid phone number ❌", "darkred")
                    return
                
                if not address or address.isdigit():
                    self.info_pop_up("❌ Enter valid address ❌", "darkred")
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

    def kitchen_summary(self):
        """
        
        """
        self.clear_widgets()
        self.highlight_button(self.kitchen_button, [self.order_button, self.management_button])
        kitchen_label = tk.Label(self.root, text="Kitchen summary")
        kitchen_label.pack()
        self.track_widgets += [kitchen_label]

        for idx,order in enumerate(self.orders, start=1):
            burritos_text= "\n".join(order.burritos)
            management_info_label = tk.Label(self.root, text=f"""
             Order #{idx} 
             Name: {order.name}
             Phone: {order.phone_number}
             Address: {order.address} 
             Burritos: {burritos_text}
             Delivery: {'Yes (+2.50$)' if order.delivery else 'No'}
             Total Price: ${order.total_price:.2f}""")
            
            management_info_label.pack()
            delete_button = tk.Button(self.root, text="Delete", command=lambda i=idx-1: self.delete_order(i))
            delete_button.pack()
            self.track_widgets += [management_info_label, delete_button]
        
        back_btn = tk.Button(self.root, text="Back", command=self.back_to_main)
        back_btn.pack()
        self.track_widgets.append(back_btn)
        

    def management_summary(self):
        """
        
        """
        self.clear_widgets()
        self.highlight_button(self.management_button, [self.order_button, self.kitchen_button])
        management_label = tk.Label(self.root, text="Management Summary")
        management_label.pack()
        self.track_widgets += [management_label]

        total_deliveries = 0
        total_burritos = 0
        total_dinein = 0
        total_sales_revenue = 0.0


        for order in self.orders:
            if order.delivery:
                total_deliveries += 1
            else:
                total_dinein += 1
            total_burritos += len(order.burritos)
            total_sales_revenue += order.total_price

        summary_label = tk.Label(self.root, text=f"""
                                 Total Deliveries: {total_deliveries}
                                 Total Dine-in Orders: {total_dinein}
                                 Total Burritos Ordered: {total_burritos}
                                 Total Sales Revenue: ${total_sales_revenue:.2f}""")
        summary_label.pack()
        self.track_widgets.append(summary_label)

        back_btn = tk.Button(self.root, text="Back", command=self.back_to_main)
        back_btn.pack()
        self.track_widgets.append(back_btn)

    def store_order(self, burritos_types):
        """
        
        """
        total_price = self.updateprice_total()
        order = Orders(
            name=self.store_name,
            phone_number = self.store_phone_number,
            address = self.store_address,
            burritos = burritos_types,
            delivery = self.delivery_variable.get())
        
        order.total_price = total_price
        self.orders.append(order)
        self.save_orders_file()

    def save_orders_file(self):
        """
        
        """
        with open("orders.json", "w") as f:
            json.dump([order.__dict__ for order in self.orders], f, indent=4)
            print("Orders saved!")

# ----------- Main -------------
if __name__ == "__main__":
    root = tk.Tk()
    run_gui = GUI(root)
    root.attributes('-topmost', True)
    root.mainloop()