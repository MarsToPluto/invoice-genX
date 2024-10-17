import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from num2words import num2words
import random
import string
from invoice_without_tax import generatePDF

# Dark mode colors
dark_bg = "#1e1e1e"
dark_fg = "#dcdcdc"
dark_highlight = "#2d2d2d"
dark_accent = "#4e9a06"
dark_button_bg = "#444444"
dark_button_fg = "#ffffff"
dark_entry_bg = "#333333"

# Configure root window for dark mode
root = tk.Tk()
root.title("Invoice Exporter")
# root.configure(bg=dark_bg)

# Styling for labels
label_style = {
    "bg": dark_bg,
    "fg": dark_fg,
    "font": ('Arial', 10, 'bold')
}

# Styling for entries
entry_style = {
    "bg": dark_entry_bg,
    "fg": dark_fg,
    "insertbackground": dark_fg,
    "highlightbackground": dark_highlight,
    "highlightcolor": dark_accent,
    "font": ('Arial', 10)
}

# Styling for buttons
button_style = {
    "bg": dark_button_bg,
    "fg": dark_button_fg,
    "activebackground": dark_highlight,
    "activeforeground": dark_fg,
    "font": ('Arial', 10, 'bold'),
    "relief": tk.FLAT,
    "bd": 0
}


def generate_invoice_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def calculate_totals():
    try:
        taxable_amount = float(taxable_amount_entry.get())
        
        # Check if invoice is taxable
        if taxable_var.get() == "Taxable":
            cgst_percentage = 9.0
            sgst_percentage = 9.0
            
            cgst_amount = (taxable_amount * cgst_percentage) / 100
            sgst_amount = (taxable_amount * sgst_percentage) / 100
            total_amount = taxable_amount + cgst_amount + sgst_amount
            
            cgst_amount_var.set(f'Rs. {cgst_amount:.2f}')
            sgst_amount_var.set(f'Rs. {sgst_amount:.2f}')
            total_amount_var.set(f'Rs. {total_amount:.2f}')
        else:
            # No tax calculations for non-taxable
            cgst_amount_var.set('Rs. 0.00')
            sgst_amount_var.set('Rs. 0.00')
            total_amount = taxable_amount
            total_amount_var.set(f'Rs. {total_amount:.2f}')
        
        amount_in_words = convert_to_words(total_amount)
        amount_in_words_var.set(amount_in_words)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

def convert_to_words(amount):
    if amount == 0:
        return "Zero Rupees Only"
    
    amount_in_words = num2words(amount, lang='en_IN').replace(' and', ' and').replace(', ', ' ').replace(' Rupees', ' Rupees and').replace(' Paise', ' Paise').replace('Only', 'Only')
    
    return amount_in_words.capitalize() + ' Only'

def update_item_calculations(event=None):
    try:
        rate = float(item_rate_entry.get())
        qty = float(item_qty_entry.get())
        taxable_value = rate * qty
        
        if taxable_var.get() == "Taxable":
            cgst_amount = (taxable_value * 9.0) / 100
            sgst_amount = (taxable_value * 9.0) / 100
            amount = taxable_value + cgst_amount + sgst_amount
        else:
            cgst_amount = 0
            sgst_amount = 0
            amount = taxable_value
        
        item_taxable_value_entry.delete(0, tk.END)
        item_taxable_value_entry.insert(0, f'Rs. {taxable_value:.2f}')
        item_tax_amount_entry.delete(0, tk.END)
        item_tax_amount_entry.insert(0, f'Rs. {cgst_amount + sgst_amount:.2f}')
        item_amount_entry.delete(0, tk.END)
        item_amount_entry.insert(0, f'Rs. {amount:.2f}')
    except ValueError:
        item_taxable_value_entry.delete(0, tk.END)
        item_tax_amount_entry.delete(0, tk.END)
        item_amount_entry.delete(0, tk.END)

def add_item():
    name = item_name_entry.get()
    hsn = item_hsn_entry.get()
    rate = item_rate_entry.get()
    qty = item_qty_entry.get()
    taxable_value = item_taxable_value_entry.get() or 0
    tax_amount = item_tax_amount_entry.get() or 0
    amount = rate

    # Perform calculations based on the taxable status
    if taxable_var.get() == "Taxable":
        # Validation for taxable invoices
        if not all([name, hsn, rate, qty, taxable_value, tax_amount, amount]):
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
    else:
        # For non-taxable invoices, only validate required fields and calculate amount
        if not all([name, hsn, rate, qty]):
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return
        
        try:
            rate = float(rate)
            qty = float(qty)
            amount = rate * qty
            amount = f'Rs. {amount:.2f}'
        except ValueError:
            messagebox.showerror("Input Error", "Invalid rate or quantity.")
            return

        item_taxable_value_entry.delete(0, tk.END)
        item_taxable_value_entry.insert(0, f'Rs. {amount}')
        item_tax_amount_entry.delete(0, tk.END)
        item_tax_amount_entry.insert(0, "Rs. 0.00")
        item_amount_entry.delete(0, tk.END)
        item_amount_entry.insert(0, amount)

    # Add item to the listbox
    item_listbox.insert(tk.END, f"{name} | {hsn} | {rate} | {qty} | {item_taxable_value_entry.get()} | {item_tax_amount_entry.get()} | {amount}")
    
    # Clear input fields
    item_name_entry.delete(0, tk.END)
    item_hsn_entry.delete(0, tk.END)
    item_rate_entry.delete(0, tk.END)
    item_qty_entry.delete(0, tk.END)
    item_taxable_value_entry.delete(0, tk.END)
    item_tax_amount_entry.delete(0, tk.END)
    item_amount_entry.delete(0, tk.END)



def remove_item():
    try:
        selected_index = item_listbox.curselection()[0]
        item_listbox.delete(selected_index)
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select an item to remove.")

def calculate_and_display_totals():
    # Calculate totals
    # calculate_totals() # Uncomment if needed for total calculations
    
    # Collect invoice details
    invoice_id = invoice_no_label.cget("text").split(": ")[1]
    customer_name = customer_name_entry.get()
    place_of_supply = place_of_supply_entry.get()
    due_date = due_date_entry.get_date().strftime("%d %b %Y")
    invoice_type = taxable_var.get()
    
    # Extract item details from Listbox
    items = []
    for item in item_listbox.get(0, tk.END):
        item_details = item.split(' | ')
        items.append({
            "item_name": item_details[0],
            "hsn_sac": item_details[1],
            "rate": float(item_details[2]),
            "quantity": int(float(item_details[3])),
            "taxable_value": item_details[4] or 0,
            "tax_amount": item_details[5] or 0,
            "amount": item_details[6]
        })
    
    # Create a dictionary to store invoice and item details
    invoice_data = {
        "invoice_details": {
            "invoice_id": invoice_id,
            "customer_name": customer_name,
            "place_of_supply": place_of_supply,
            "due_date": due_date,
            "invoice_type": invoice_type
        },
        "items": items
    }
    # print(invoice_data)
    generatePDF(invoice_data)
    clear_and_reset()

def clear_and_reset():
    # Clear all input fields
    invoice_no_label.config(text="Invoice #: INV-XXXX")  # Placeholder for new invoice ID
    customer_name_entry.delete(0, tk.END)
    place_of_supply_entry.delete(0, tk.END)
    
    # Clear date picker widget
    if isinstance(due_date_entry, DateEntry):
        due_date_entry.set_date(None)  # Set date to None or a default value if needed
    
    # taxable_var.set("")  # Clear invoice type selection

    # Clear item list
    item_listbox.delete(0, tk.END)
    
    # Regenerate Invoice ID
    new_invoice_id = f"INV-{generate_invoice_number()}"
    invoice_no_label.config(text=f"Invoice #: {new_invoice_id}")
    
    # Show success alert
    messagebox.showinfo("Success", "Invoice.pdf has been generated")
    
    # Optionally, you can return the new invoice ID if needed
    return new_invoice_id

def toggle_tax_fields(*args):
    if taxable_var.get() == "Taxable":
        item_taxable_value_entry.config(state='normal')
        item_tax_amount_entry.config(state='normal')
        item_amount_entry.config(state='normal')
    else:
        item_taxable_value_entry.config(state='disabled')
        item_tax_amount_entry.config(state='disabled')
        item_amount_entry.config(state='disabled')
        # Clear tax fields if non-taxable
        item_taxable_value_entry.delete(0, tk.END)
        item_tax_amount_entry.delete(0, tk.END)
        item_amount_entry.delete(0, tk.END)
        # Reset the calculations
        update_item_calculations()


# Configure grid to be responsive
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_rowconfigure(4, weight=0)
root.grid_rowconfigure(5, weight=0)
root.grid_rowconfigure(6, weight=0)
root.grid_rowconfigure(7, weight=0)
root.grid_rowconfigure(8, weight=0)
root.grid_rowconfigure(9, weight=0)
root.grid_rowconfigure(10, weight=0)
root.grid_rowconfigure(11, weight=0)
root.grid_rowconfigure(12, weight=1)
root.grid_rowconfigure(13, weight=0)
root.grid_rowconfigure(14, weight=0)
root.grid_rowconfigure(15, weight=0)
root.grid_rowconfigure(16, weight=0)
root.grid_rowconfigure(17, weight=0)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Seller Details Frame
seller_frame = tk.Frame(root, padx=5, pady=5, bg='#f5f5f5')
seller_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

tk.Label(seller_frame, text="Seller Details", font=('Arial', 12, 'bold'), bg='#f5f5f5').grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky='w')
tk.Label(seller_frame, text="Seller Name: JOHN DOE", bg='#f5f5f5').grid(row=1, column=0, columnspan=2, padx=5, pady=1, sticky='w')
tk.Label(seller_frame, text="Address: 1234 RANDOM STREET, ANYTOWN, USA, 123456", bg='#f5f5f5').grid(row=2, column=0, columnspan=2, padx=5, pady=1, sticky='w')
tk.Label(seller_frame, text="Phone: +1 800-123-4567", bg='#f5f5f5').grid(row=3, column=0, columnspan=2, padx=5, pady=1, sticky='w')
tk.Label(seller_frame, text="GSTIN: 22XYZ1234P9Z5", bg='#f5f5f5').grid(row=4, column=0, columnspan=2, padx=5, pady=1, sticky='w')


# Invoice Number
invoice_no_label = tk.Label(root, text=f"Invoice #: {generate_invoice_number()}", font=('Arial', 10, 'bold'), bg='#ffffff')
invoice_no_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

# Invoice Date
tk.Label(root, text="Invoice Date", font=('Arial', 8, 'bold')).grid(row=2, column=0, padx=5, pady=2, sticky='w')
invoice_date_entry = DateEntry(root, date_pattern='dd/MM/yyyy', background='darkblue', foreground='white', borderwidth=1, width=10)
invoice_date_entry.grid(row=2, column=1, padx=5, pady=2)

# Customer Name
tk.Label(root, text="Customer Name", font=('Arial', 8, 'bold')).grid(row=3, column=0, padx=5, pady=2, sticky='w')
customer_name_entry = tk.Entry(root, font=('Arial', 8))
customer_name_entry.grid(row=3, column=1, padx=5, pady=2)

# Place of Supply
tk.Label(root, text="Place of Supply", font=('Arial', 8, 'bold')).grid(row=4, column=0, padx=5, pady=2, sticky='w')
place_of_supply_entry = tk.Entry(root, font=('Arial', 8))
place_of_supply_entry.grid(row=4, column=1, padx=5, pady=2)

# Due Date
tk.Label(root, text="Due Date", font=('Arial', 8, 'bold')).grid(row=5, column=0, padx=5, pady=2, sticky='w')
due_date_entry = DateEntry(root, date_pattern='dd/MM/yyyy', background='darkblue', foreground='white', borderwidth=1, width=10)
due_date_entry.grid(row=5, column=1, padx=5, pady=2)

# Taxable Dropdown
tk.Label(root, text="Invoice Type", font=('Arial', 8, 'bold')).grid(row=6, column=0, padx=5, pady=2, sticky='w')
taxable_var = tk.StringVar(value="Taxable")
taxable_dropdown = ttk.Combobox(root, textvariable=taxable_var, values=["Taxable", "Non-Taxable"], state='readonly', width=10)
taxable_dropdown.grid(row=6, column=1, padx=5, pady=2)
taxable_dropdown.bind("<<ComboboxSelected>>", toggle_tax_fields)

# Item Details Frame
item_frame = tk.Frame(root, padx=5, pady=5)
item_frame.grid(row=7, column=0, columnspan=2, sticky='ew')

tk.Label(item_frame, text="Item Details", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=4, padx=5, pady=2, sticky='w')

# Item Name
tk.Label(item_frame, text="Item Name", font=('Arial', 8, 'bold')).grid(row=1, column=0, padx=5, pady=2, sticky='w')
item_name_entry = tk.Entry(item_frame, font=('Arial', 8))
item_name_entry.grid(row=1, column=1, padx=5, pady=2)

# HSN/SAC
tk.Label(item_frame, text="HSN/SAC", font=('Arial', 8, 'bold')).grid(row=2, column=0, padx=5, pady=2, sticky='w')
item_hsn_entry = tk.Entry(item_frame, font=('Arial', 8))
item_hsn_entry.grid(row=2, column=1, padx=5, pady=2)

# Rate
tk.Label(item_frame, text="Rate", font=('Arial', 8, 'bold')).grid(row=3, column=0, padx=5, pady=2, sticky='w')
item_rate_entry = tk.Entry(item_frame, font=('Arial', 8))
item_rate_entry.grid(row=3, column=1, padx=5, pady=2)

# Quantity
tk.Label(item_frame, text="Quantity", font=('Arial', 8, 'bold')).grid(row=4, column=0, padx=5, pady=2, sticky='w')
item_qty_entry = tk.Entry(item_frame, font=('Arial', 8))
item_qty_entry.grid(row=4, column=1, padx=5, pady=2)

# Taxable Value
tk.Label(item_frame, text="Taxable Value", font=('Arial', 8, 'bold')).grid(row=5, column=0, padx=5, pady=2, sticky='w')
item_taxable_value_entry = tk.Entry(item_frame, font=('Arial', 8), state='normal')
item_taxable_value_entry.grid(row=5, column=1, padx=5, pady=2)

# Tax Amount
tk.Label(item_frame, text="Tax Amount", font=('Arial', 8, 'bold')).grid(row=6, column=0, padx=5, pady=2, sticky='w')
item_tax_amount_entry = tk.Entry(item_frame, font=('Arial', 8), state='normal')
item_tax_amount_entry.grid(row=6, column=1, padx=5, pady=2)

# Amount
tk.Label(item_frame, text="Amount", font=('Arial', 8, 'bold')).grid(row=7, column=0, padx=5, pady=2, sticky='w')
item_amount_entry = tk.Entry(item_frame, font=('Arial', 8), state='normal')
item_amount_entry.grid(row=7, column=1, padx=5, pady=2)

# Add Item Button
add_item_button = tk.Button(item_frame, text="Add Item", command=add_item, font=('Arial', 8, 'bold'))
add_item_button.grid(row=8, column=0, columnspan=2, pady=5)

# Remove Item Button
remove_item_button = tk.Button(item_frame, text="Remove Item", command=remove_item, font=('Arial', 8, 'bold'))
remove_item_button.grid(row=8, column=2, columnspan=2, pady=5)

# Item Listbox
item_listbox = tk.Listbox(root, width=60, height=8, font=('Arial', 8))
item_listbox.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

# Calculate Totals
calculate_button = tk.Button(root, text="Generate PDF", command=calculate_and_display_totals, font=('Arial', 10, 'bold'), bg='#4CAF50', fg='white')
calculate_button.grid(row=9, column=0, columnspan=2, pady=10)


root.mainloop()

