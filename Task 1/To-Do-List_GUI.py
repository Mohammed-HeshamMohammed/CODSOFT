import tkinter as tk
from tkinter import messagebox

# Main Window Initializing
root = tk.Tk()
root.geometry("450x300")
root.title("To-Do List")

# LabelFrame to label listbox
lb = tk.LabelFrame(root, text="List")
listb = tk.Listbox(lb, width=50, height=10)
listb.pack(padx=10, pady=10)
lb.pack(pady=10)

# Entry textbox
en = tk.Entry(root, width=40)

# Add task to list
def addtolist():
    task = en.get()
    if task:
        listb.insert(tk.END, task)
        en.delete(0, tk.END)  # Clearing Entry textbox
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

# Mark tasks as done
def markasdone():
    try:
        select_task = listb.curselection()[0]
        task = listb.get(select_task)
        listb.delete(select_task)
        listb.insert(select_task, f"✔ {task}")
        listb.itemconfig(select_task, {'fg': 'green'})
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to mark as done.")

# Remove selected task
def removetask():
    try:
        select_task = listb.curselection()[0]
        listb.delete(select_task)
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task.")

# Edit selected task
def editlist():
   try:
       select_task = listb.curselection()[0]
       task = listb.get(select_task)
       en.delete(0, tk.END)  # Clearing Entry textbox
       en.insert(0, task)
       listb.delete(select_task)
   except IndexError:
        messagebox.showwarning("Warning", "Please select a task.")

# Refresh the task list
def refresh():
    # Create a list to hold the remaining tasks
    remaining_tasks = []

    # Iterate through each task in the Listbox
    for i in range(listb.size()):
        task = listb.get(i)
        if not task.startswith("✔"):  # Check if the task is not marked as done
            remaining_tasks.append(task)  # Add it to the remaining tasks

    # Clear Listbox and fill it with remaining tasks
    listb.delete(0, tk.END)  # Clear tasks
    for task in remaining_tasks:
        listb.insert(tk.END, task)  # Re-add remaining tasks

# Buttons for various tasks
btn = tk.Button(root, text="Add to List", command=addtolist)
btn2 = tk.Button(root, text="Mark As Done", command=markasdone)
btn3 = tk.Button(root, text="Remove From List", command=removetask)
btn4 = tk.Button(root, text="Edit Task", command=editlist)
btn5 = tk.Button(root, text="Refresh", command=refresh)

# Layout for User Management
en.pack(pady=10, padx=10)
btn.place(x=25, y=265)
btn2.place(x=100, y=265)
btn3.place(x=190, y=265)
btn4.place(x=301, y=265)
btn5.place(x=365, y=265)

# Start Tkinter main loop
root.mainloop()
