from tkinter import *
from tkinter import messagebox

# Main Window Initializing
root=Tk()
root.geometry("450x300")
root.title("To DO List")

# LabelFrame to label listbox
lb=LabelFrame(root,text="List")
listb=Listbox(lb, width="50",height="10")
listb.pack(padx=10,pady=10)
lb.pack(pady=10)
#Entry textbox
en=Entry(root,width=40)

# Add task to list
def addtolist():
    task=en.get()
    if task:
        listb.insert(END,task)
        en.delete(0, END)         #Clearing Entry textbox
    else:
        messagebox.showwarning("Warning", "Please Enter A Task.")

# Mark tasks as done
def markasdone():
    try:
        select_task=listb.curselection()[0]
        task = listb.get(select_task)
        listb.delete(select_task)
        listb.insert(select_task,f"✔ {task}")
        listb.itemconfig(select_task, {'fg': 'green'})
    except IndexError:
        messagebox.showwarning("Warning","Please Select A Task To Be Marked As Done")

# Remove selected task
def removetask():
    try:
        select_task=listb.curselection()[0]
        listb.delete(select_task)
    except IndexError:
        messagebox.showwarning("Warning","Please Select A Task")

# Edit selected task
def editlist():
   try:
       select_task=listb.curselection()[0]
       task = listb.get(select_task)
       en.delete(0,END)    #Clearing Entry textbox
       en.insert(0,task)
       listb.delete(select_task)
   except IndexError:
        messagebox.showwarning("Warning","Please Select A Task")

# Refresh the task list
def refresh():
    # Creating list to hold the remaining tasks
    remaining_tasks = []

    # Iterate through each task in the Listbox
    for i in range(listb.size()):
        task = listb.get(i)
        if not task.startswith("✔"):  # Checking if the task is not marked as done
            remaining_tasks.append(task)  # Add it to the remaining tasks

    # Clearing Listbox and fill it with remaining tasks
    listb.delete(0, END)  # Clearing tasks
    for task in remaining_tasks:
        listb.insert(END, task)  # Readding remaining tasks

#Buttons for various Tasks
btn=Button(root,text="Add to List",command=addtolist)
btn2=Button(root,text="Mark As Done",command=markasdone)
btn3=Button(root,text="Remove From List",command=removetask)
btn4=Button(root,text="Edit Task",command=editlist)
btn5=Button(root,text="Refresh",command=refresh)


# Layout for User Management
en.pack(pady=10,padx=10)
btn.place(x=25,y=265)
btn2.place(x=100,y=265)
btn3.place(x=190,y=265)
btn4.place(x=301,y=265)
btn5.place(x=365,y=265)

#Starting Tkinter main loop
root.mainloop()