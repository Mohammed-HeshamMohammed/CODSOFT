from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

# Create main window
root = tk.Tk()
root.title("Contact List")
root.geometry("500x600")
root.config(bg="#f4f4f4")

contacts = {}  # Dictionary to store contacts

# Function to add a contact
def addcontact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if name and phone:  # Basic validation for name and phone
        contacts[name] = {"Phone": phone, "Email": email, "Address": address}
        refresh_contact_list()
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Name and Phone Number are required.")

# Function to update contacts
def update():
    selected_contact = get_selected()
    if selected_contact:
        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        address = address_entry.get()

        if name and phone:  # checking before updating
            contacts[selected_contact] = {"Phone": phone, "Email": email, "Address": address}
            refresh()
            clear_entries()
        else:
            messagebox.showwarning("Input Error", "Name and Phone Number are required.")
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to update.")

# Function to delete contacts
def delete():
    selected_contact = get_selected()
    if selected_contact:
        del contacts[selected_contact]
        refresh()
        clear_entries()
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to delete.")

# Function to contacts
def search_contact():
    search_term = simpledialog.askstring("Search", "Enter name or phone number:")
    if search_term:
        matching_contacts = [name for name, details in contacts.items() if search_term.lower() in name.lower() or search_term in details['Phone']]
        if matching_contacts:
            contact_listbox.delete(0, tk.END)
            for name in matching_contacts:
                contact_listbox.insert(tk.END, name)
        else:
            messagebox.showinfo("Search Result", "No matching contacts found.")

# Canceling Function (clear fields, show all contacts,etc.....)
def cancel():
    clear_entries()
    refresh()

# Function to refresh contact listbox
def refresh():
    contact_listbox.delete(0, tk.END)
    for name in contacts:
        contact_listbox.insert(tk.END, name)

# Function to clear input text fields
def clearingentries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# Function to handle listbox selection
def on_select(event):
    selected_contact = get_selected()
    if selected_contact:
        contact_info = contacts[selected_contact]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, selected_contact)

        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, contact_info["Phone"])

        email_entry.delete(0, tk.END)
        email_entry.insert(0, contact_info["Email"])

        address_entry.delete(0, tk.END)
        address_entry.insert(0, contact_info["Address"])

# Function to get selected contact name from the listbox
def get_selected():
    try:
        selected_index = contact_listbox.curselection()[0]
        return contact_listbox.get(selected_index)
    except IndexError:
        return None


#-----------------------------------------GUI-------------------------------------------


tk.Label(root, text="Contact Manager", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333").pack(pady=15)

# Frame for input fields
form_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.RIDGE)
form_frame.pack(pady=10, padx=20, fill=tk.X)

# Detailed fields for user friendly desgin
tk.Label(form_frame, text="Name", font=("Arial", 10, "bold"), bg="#ffffff", anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(form_frame, font=("Arial", 10), bg="#f0f0f0", width=40)
name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

tk.Label(form_frame, text="Phone", font=("Arial", 10, "bold"), bg="#ffffff", anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
phone_entry = tk.Entry(form_frame, font=("Arial", 10), bg="#f0f0f0", width=40)
phone_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

tk.Label(form_frame, text="Email", font=("Arial", 10, "bold"), bg="#ffffff", anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
email_entry = tk.Entry(form_frame, font=("Arial", 10), bg="#f0f0f0", width=40)
email_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

tk.Label(form_frame, text="Address", font=("Arial", 10, "bold"), bg="#ffffff", anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="w")
address_entry = tk.Entry(form_frame, font=("Arial", 10), bg="#f0f0f0", width=40)
address_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

btn_frame = tk.Frame(root, bg="#f4f4f4")
btn_frame.pack(pady=10)

cancel_btn = tk.Button(btn_frame, text="❌", font=("Arial", 12, "bold"), bg="#dc3545", fg="#fff", command=cancel_action)
cancel_btn.grid(row=0, column=0, padx=5, pady=5)

tk.Button(btn_frame, text="Add Contact", font=("Arial", 10, "bold"), bg="#28a745", fg="#fff", command=addcontact).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="Update Contact", font=("Arial", 10, "bold"), bg="#ffc107", fg="#fff", command=update).grid(row=0, column=2, padx=5, pady=5)
tk.Button(btn_frame, text="Delete Contact", font=("Arial", 10, "bold"), bg="#dc3545", fg="#fff", command=delete).grid(row=0, column=3, padx=5, pady=5)
tk.Button(btn_frame, text="Search Contact", font=("Arial", 10, "bold"), bg="#007bff", fg="#fff", command=search_contact).grid(row=0, column=4, padx=5, pady=5)

listbox_frame = tk.Frame(root, bg="#f4f4f4")
listbox_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

contact_listbox = tk.Listbox(listbox_frame, font=("Arial", 12), bg="#ffffff", fg="#333", selectbackground="#007bff", height=10, bd=2, relief=tk.RIDGE)
contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
contact_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=contact_listbox.yview)

# Binding selection event to listbox
contact_listbox.bind('<<ListboxSelect>>', on_select)

root.mainloop()
