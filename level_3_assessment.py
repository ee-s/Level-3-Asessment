"""
Burrito ordering system

This program allows users to order burritos which are saved to a JSON file, 
select delivery options, and view management and kitchen summaries.
The program also allows for orders to be deleted from the kitchen screen.
"""

# Importing libraries
import json
import tkinter as tk
from tkinter import ttk, messagebox



# Constants for prices
REGULAR_PRICE = 8.5
DELIVERY_PRICE = 2.5
HIGHER_PRICE = 13.5
MAX_BURRITOS = 5   # Maximum number of burritos

# ------------------ Order Class ------------------


class Order:
    """
        Class represents a single burrito order

        This stores customer information, burrito selection and information regarding the delivery.
        
        Methods:
            __init__(self, name, phone_number, address, burritos, delivery):
                Initialises the order with the following parameters:
                - name (str): Customer's name
                - phone_number (str): Customer's phone number
                - address (str): Customer's address
                - burritos (list): List of selected burrito types
                - delivery (bool): Whether order is delivered
                - total_price (float): Total price of the order
        """
    

    def __init__(self, name, phone_number, address, burritos, delivery):
        """
        The method initialises the order with the following parameters:
        
        Args:
            name (str): Customer's name
            phone_number (str): Customer's phone number
            address (str): Customer's address
            burritos (list): List of the selected burrito types
            delivery (bool): Whether the order is delivered or not
        """
        self.name = name
        self.phone_number = phone_number
        self.address = address 
        self.burritos = burritos
        self.delivery = delivery

#------------------- GUI Class ------------------


class GUI:
    """
    The GUI class for the Burrito Ordering System.

    The class allows for users to input data and alter data,
    via a graphical user interface using Tkinter.
    This allows for users to:

    - Input personal information such as name and delivery information
    - Select the number of burritos
    - Select the type of burritos
    - View the management summary ( total sales, total burritos, total deliveries)
    - View the kitchen summary (all orders, delivery or not, total price)
    - Delete orders
    - Save orders to a JSON file

    These attributes and methods are specifically organised to have a logical flow and 
    clear, intuitive structure. 
    """


    def __init__(self, root):
        """
        The method initialises the GUI 

        Args:
            root (tk.Tk): This is the main window of the GUI

        Sets up the main attributes of the GUI, including the title, size, and buttons.
        """
        self.root = root
        self.orders = []

        # Set up the main window layout
        root.title("Ordering System")
        root.geometry("600x600")
        self.label = tk.Label(root, text="Burritos", font=("Myriad pro", 23))
        self.label.pack(pady=(10,2))

        # Implements buttons for specific functions
        self.order_button = tk.Button(root, text="Enter Order", command=self.enter_order)
        self.order_button.pack(pady=(10,2))
        self.management_button = tk.Button(root, text="Management Summary", command=self.management_summary)
        self.management_button.pack(pady=(10,2))
        self.kitchen_button = tk.Button(root, text="Kitchen Screen", command=self.kitchen_summary)
        self.kitchen_button.pack(pady=(10,2))

        # Implements a status label to respond to user input
        self.status_label = tk.Label(root, text="", fg="darkblue")
        self.status_label.pack(pady=(20,4))
        self.status_label.config(text="Burrito ordering system", fg="darkblue")

        self.track_widgets = []  # Tracks widgets for clearing
        self.delivery_variable = tk.BooleanVar() # Checkbox for delivery
        self.burrito_boxes = []

    def clear_widgets(self):
        """
        This method clears all widgets from the GUI.
        This is done via a loop that removes each widget in the track_widgets list.

        """
        for widget in self.track_widgets:
            widget.destroy()
        self.track_widgets.clear()

    def info_pop_up(self, message, color= "darkorange", duration=2000):
        """
        Displays a pop-up message for a short period of time to inform users about order status.

        Args:
            message (str): The text to display in the pop-up.
            color (str): The color of the text in the pop-up.
            duration (int): The time for the user to read the pop-up.
        """
        self.status_label.config(text=message, fg=color)
        self.root.after(duration, lambda: self.status_label.config(text="")) 
        # Clears the status label after the duration

    def enter_order(self):
        """
        This method displays the order entry screen, allowing users to input their name and delivery information.
        It also includes a checkbox for delivery which if clicked, will show the phone number and address fields.
        This allows for personal customer information to be entered.
        """
        self.clear_widgets()
        self.highlight_button(self.order_button, [self.kitchen_button, self.management_button])
        name_label = tk.Label(self.root, text="Name:")
        name_label.pack(pady=(10,2))
        name_entry = tk.Entry(self.root)
        name_entry.pack(pady=2)

        def hide_delivery_variables():
            """
            This method hides/shows the delivery variables depending on the state of the delivery checkbox.
            If the delivery checkbox is ticked the phone number and address fields will be shown.          
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

        delivery_checkbox = tk.Checkbutton(self.root, text="Delivery? (+2.50$)", variable=self.delivery_variable,
                                           command=hide_delivery_variables)
        delivery_checkbox.pack()

        phone_number_label = tk.Label(self.root, text="Phone Number: ")
        phone_number_entry = tk.Entry(self.root)
        address_label = tk.Label(self.root, text="Address: ")
        address_entry = tk.Entry(self.root)

        hide_delivery_variables()

        def place_order():
            """
            Method to place the order.
            This is done via checking the name, phone number and address fields.
            If feilds are valid, order is placed and pop-up is displayed.
            """
            name = name_entry.get().strip()
            if not name or name.isdigit():
                self.info_pop_up("Invalid name ❌", "darkred")
                return
            
            if self.delivery_variable.get():
                phone_number = phone_number_entry.get().strip()
                address = address_entry.get().strip()
                if not phone_number or not (7 <= len(phone_number) <= 18):
                    self.info_pop_up(" Invalid phone number ❌", "darkred")
                    return
                
                if not address or address.isdigit():
                    self.info_pop_up("Invalid address ❌", "darkred")
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
        Method displays the kitchen summary.
        This includes all orders, delivery, and total price.
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
        
        back_button = tk.Button(self.root, text="Back", command=self.back_to_main)
        back_button.pack(pady=5, padx=10)
        self.track_widgets.append(back_button)
        

    def management_summary(self):
        """
        Method displays the management summary.
        This includes total sales, total burritos, total deliveries and total dine-in orders.
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

        back_button = tk.Button(self.root, text="Back", command=self.back_to_main)
        back_button.pack(pady=5, padx=10)
        self.track_widgets.append(back_button)



    def select_burritos(self, burrito_count):
            """
            Displays a selection of burritos for the user to select from.
            This is specific to the pre selected number of burritos,
            using combo boxes and shows a real time total cost.

            Args:
                burrito_count (int): The number of burritos to be selected.
            """
            select_burritos_label = tk.Label(self.root,text="Select burrito types" )
            select_burritos_label.pack()
            self.track_widgets.append(select_burritos_label)            
            burrito_types = [
    ["Cheese", REGULAR_PRICE], ["Plain", REGULAR_PRICE], ["Spicy", REGULAR_PRICE],
    ["Deluxe", HIGHER_PRICE], ["Large", HIGHER_PRICE], ["Gourmet", HIGHER_PRICE]
]
            burrito_types = [f"{name} - ${price:.2f}" for name,price in burrito_types]
            for burrito in range(burrito_count):
                var = tk.StringVar()
                burrito_menu = ttk.Combobox(self.root, textvariable=var, values=burrito_types)
                burrito_menu.set("Select a burrito")
                burrito_menu.pack(pady=10)
                burrito_menu.bind("<<ComboboxSelected>>", lambda event: self.updateprice_total()) 
                self.burrito_boxes.append(var)
                self.track_widgets.append(burrito_menu)
            
            self.price_label = tk.Label(self.root, text="Total Price: $0.00")
            self.price_label.pack(pady=10)
            self.track_widgets.append(self.price_label)

                              
            confirm_button = tk.Button(self.root, text="Confirm", command=self.process_burrito_selection) 
            confirm_button.pack(pady=10)
            self.track_widgets.append(confirm_button)

    def process_burrito_selection(self):
        """
        Method processes the burrito selection.
        A pop-up message confirms that users want the order to be placed
        and checks whether all fields have been entered.
        """
        selected_burritos = [ver.get() for ver in self.burrito_boxes]
        if all(burrito and burrito != "Select a burrito" for burrito in selected_burritos):

            if messagebox.askyesno("Confirm Order", "Do you want to place this order?"):
                self.store_order(selected_burritos)
                self.info_pop_up("Order placed ✅", "darkgreen")
                self.burrito_boxes.clear()
                self.clear_widgets()

            else: 
                self.info_pop_up("Order cancelled ❌", "darkred")
                self.clear_widgets()
                self.burrito_boxes.clear()

        else:
            self.info_pop_up("Select all burrito types ❌", "darkred")
        

    def updateprice_total(self):
        """
        This method updates the total price based on real time selected burritos.
        It does this via checking the type of burrito ordered and adding its price to the total price.

        Returns:
            total_price (float): The total price of the order.
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

    def highlight_button(self, clicked, others):
        """
        This method highlights the clicked button and resets the others to their default state.
        This is done via a loop which changes the button background colours.

        Args:
            clicked (tk.Button): The clicked button.
            others (list): A list of the others to reset.

        """
        clicked.config(bg="lightgreen", activebackground="green")
        for button in others:
            button.config(bg="SystemButtonFace", activebackground="SystemButtonFace")

    def get_burrito_amount(self):
        """
        This method gets the number of burritos the user wants to order.
        """
        self.clear_widgets()

        burrito_label = tk.Label(self.root, text="How many burritos?")
        burrito_label.pack()

        self.burrito_count_entry = tk.Entry(self.root)
        self.burrito_count_entry.pack()
        # Calls the process burrito count function
        enter_button = tk.Button(self.root, text="Enter", command=self.process_burrito_count) 
        enter_button.pack(pady=10)

        self.track_widgets += [burrito_label, self.burrito_count_entry, enter_button]

    def process_burrito_count(self):
        """
        This method get the amount of burritos the user wants to order 
        The amount is checked to be valid and pop-ups are used to inform the user if the amount is valid.

        Returns:
            burrito_count (int): The number of burritos user wants to order.
        """
        burrito_count = self.burrito_count_entry.get().strip()
        if burrito_count.isdigit():
            count = int(burrito_count)
            if 0 < count <= MAX_BURRITOS:
                self.burrito_count = count
                self.status_label.config(text=f"""Ordering {self.burrito_count} burritos""", fg="darkgreen")
                self.burrito_count_entry.delete(0, tk.END)
                self.clear_widgets()

                self.select_burritos(self.burrito_count)
                self.info_pop_up("Processed ✅", "darkgreen")
                self.order_button.config(bg="SystemButtonFace")
                return self.burrito_count
            
        self.info_pop_up(f"Invalid number of burritos 1-{MAX_BURRITOS} ❌", "darkred")
       
    def delete_order(self, order_index):
        """
        This method deletes an order from the orders list.
        This does this via checking the orders position and confims the deletion with the user.

        Args:
            order_index (int): This is the index of the order to be deleted.

        """
        if 0 <= order_index < len(self.orders): # Checks the orders index is valid
            if messagebox.askyesno("Confirm deletion", "Do you want to delete this order?"):
                del self.orders[order_index]
                self.info_pop_up("Order deleted", "darkorange")
                self.clear_widgets()
            else: 
                self.info_pop_up("Not deleted", "darkorange")
                
    def back_to_main(self):
        """
        Method returns user to main menu.
        Widgets are cleared and a pop-up message is displayed.

        """
        self.clear_widgets()
        self.info_pop_up("Going to main menu", "darkorange")

    def store_order(self, burritos_types):
        """
        Method stores the order.
        Orders object is made and appended to a list.
        Information is saved to a JSON file.

        Args:
            burritos_types (list): The list of the selected burrito types.

        """
        total_price = self.updateprice_total()
        order = Order(
            name=self.store_name,
            phone_number = self.store_phone_number,
            address = self.store_address,
            burritos = burritos_types,
            delivery = self.delivery_variable.get())
        
        order.total_price = total_price
        self.orders.append(order)
        self.save_orders_file()  # Calls the function to save orders to a JSON file

    def save_orders_file(self):
        """
        Method saves the orders to a JSON file.
        Via loop that iterates through the orders list, 
        and saves orders to JSON file.
        """
        with open("orders.json", "w") as f:
            json.dump([order.__dict__ for order in self.orders], f, indent=4)
            print("Orders saved!")

# ----------- Main -------------
if __name__ == "__main__":
    root = tk.Tk()
    run_gui = GUI(root)
    root.attributes('-topmost', True)  # Sets the GUI to be on top of other windows
    root.mainloop()  # Calls the main loop to run the GUI