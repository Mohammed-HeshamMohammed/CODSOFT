import tkinter as tk
from tkinter import messagebox, simpledialog

# Create main window with dark theme
root = tk.Tk()
root.title("Contact List")
root.geometry("575x600")
root.config(bg="#1e1e2e")  # Dark background

contacts = {}  # Dictionary to store contacts

# Function to add a contact
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if name and phone:  # Basic validation for name and phone
        contacts[name] = {"Phone": phone, "Email": email, "Address": address}
        refresh()
        clear_entries()
    else:
        messagebox.showwarning("Input Error", "Name and Phone Number are required.")

# Function to update contacts
def update_contact():
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
def delete_contact():
    selected_contact = get_selected()
    if selected_contact:
        del contacts[selected_contact]
        refresh()
        clear_entries()
    else:
        messagebox.showwarning("Selection Error", "Please select a contact to delete.")

# Function to search contacts
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

# Cancel function to clear fields and refresh
def cancel():
    clear_entries()
    refresh()

# Function to refresh contact listbox
def refresh():
    contact_listbox.delete(0, tk.END)
    for name in contacts:
        contact_listbox.insert(tk.END, name)

# Function to clear input text fields
def clear_entries():
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

# Function to get selected contact name from listbox
def get_selected():
    try:
        selected_index = contact_listbox.curselection()[0]
        return contact_listbox.get(selected_index)
    except IndexError:
        return None

#-----------------------------------------GUI-------------------------------------------

# GUI Layout
tk.Label(root, text="Contact Manager", font=("Helvetica", 18, "bold"), bg="#1e1e2e", fg="#ffffff").pack(pady=15)

# Frame for input fields
form_frame = tk.Frame(root, bg="#2e2e3e", bd=2, relief=tk.FLAT)
form_frame.pack(pady=10, padx=20, fill=tk.X)

# Input fields with Friendly UI Design
entry_style = {"font": ("Helvetica", 10), "bg": "#3e3e4e", "fg": "#ffffff", "insertbackground": "white"}

tk.Label(form_frame, text="Name", font=("Helvetica", 10, "bold"), bg="#2e2e3e", fg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(form_frame, **entry_style)
name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

tk.Label(form_frame, text="Phone", font=("Helvetica", 10, "bold"), bg="#2e2e3e", fg="#ffffff").grid(row=1, column=0, padx=10, pady=5, sticky="w")
phone_entry = tk.Entry(form_frame, **entry_style)
phone_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

tk.Label(form_frame, text="Email", font=("Helvetica", 10, "bold"), bg="#2e2e3e", fg="#ffffff").grid(row=2, column=0, padx=10, pady=5, sticky="w")
email_entry = tk.Entry(form_frame, **entry_style)
email_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

tk.Label(form_frame, text="Address", font=("Helvetica", 10, "bold"), bg="#2e2e3e", fg="#ffffff").grid(row=3, column=0, padx=10, pady=5, sticky="w")
address_entry = tk.Entry(form_frame, **entry_style)
address_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

# Managing Buttons contacts with style
btn_frame = tk.Frame(root, bg="#1e1e2e")
btn_frame.pack(pady=10)

# Defining button style
button_style = {
    "font": ("Helvetica", 10, "bold"),
    "fg": "#ffffff",
    "bd": 0,
    "width": 12,
    "height": 1,
    "relief": tk.FLAT,
    "activeforeground": "#ffffff",
}

# Hover effect functions for buttons
def on_enter(event, color):
    event.widget.config(bg=color)

def on_leave(event, color):
    event.widget.config(bg=color)

# Creating buttons with hover effects
add_btn = tk.Button(btn_frame, text="Add Contact", command=add_contact, bg="#5a9f65", **button_style)
add_btn.grid(row=0, column=0, padx=5, pady=5)
add_btn.bind("<Enter>", lambda event: on_enter(event, "#7fc97a"))
add_btn.bind("<Leave>", lambda event: on_leave(event, "#5a9f65"))

update_btn = tk.Button(btn_frame, text="Update Contact", command=update_contact, bg="#ffc107", **button_style)
update_btn.grid(row=0, column=1, padx=5, pady=5)
update_btn.bind("<Enter>", lambda event: on_enter(event, "#ffd95a"))
update_btn.bind("<Leave>", lambda event: on_leave(event, "#ffc107"))

delete_btn = tk.Button(btn_frame, text="Delete Contact", command=delete_contact, bg="#e76f51", **button_style)
delete_btn.grid(row=0, column=2, padx=5, pady=5)
delete_btn.bind("<Enter>", lambda event: on_enter(event, "#f09477"))
delete_btn.bind("<Leave>", lambda event: on_leave(event, "#e76f51"))

search_btn = tk.Button(btn_frame, text="Search Contact", command=search_contact, bg="#6495ed", **button_style)
search_btn.grid(row=0, column=3, padx=5, pady=5)
search_btn.bind("<Enter>", lambda event: on_enter(event, "#85baf6"))
search_btn.bind("<Leave>", lambda event: on_leave(event, "#6495ed"))

cancel_btn = tk.Button(btn_frame, text="❌ Cancel", command=cancel, bg="#6c757d", **button_style)
cancel_btn.grid(row=0, column=4, padx=5, pady=5)
cancel_btn.bind("<Enter>", lambda event: on_enter(event, "#9ca2a8"))
cancel_btn.bind("<Leave>", lambda event: on_leave(event, "#6c757d"))

# Listbox for displaying contacts
listbox_frame = tk.Frame(root, bg="#1e1e2e")
listbox_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

contact_listbox = tk.Listbox(listbox_frame, font=("Helvetica", 12), bg="#2e2e3e", fg="#ffffff", selectbackground="#5c5c7c", selectforeground="#ffffff", height=10, bd=2, relief=tk.FLAT)
contact_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
contact_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=contact_listbox.yview)

# Hover effect functions for listbox items
def highlight(event):
    widget = event.widget
    index = widget.nearest(event.y)
    if index >= 0:  # Only proceed if the index is valid
        # Unhighlight all items
        for i in range(widget.size()):
            widget.itemconfig(i, {'bg': '#2e2e3e'})

        # Highlight the current item
        widget.itemconfig(index, {'bg': '#3e3e4e'})


def unhighlight(event):
    widget = event.widget
    # Optionally, you can keep unhighlighting logic if needed.
    for i in range(widget.size()):
        widget.itemconfig(i, {'bg': '#2e2e3e'})

# Binding selection event to listbox
contact_listbox.bind('<<ListboxSelect>>', on_select)
contact_listbox.bind('<Motion>', highlight)
contact_listbox.bind('<Leave>', unhighlight)

# Start the main loop
root.mainloop()
