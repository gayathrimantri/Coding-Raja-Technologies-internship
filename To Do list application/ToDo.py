from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class Todo:
    def __init__(self, root):
        self.root = root
        self.root.title('To-Do List')
        self.root.geometry('650x410+300+150')

        self.label = Label(self.root, text='To-Do List App', font='Arial,25', width=20, bd=5, bg='orange', fg='black')
        self.label.pack(side='top', fill=BOTH)

        self.label2 = Label(self.root, text='Add Task', font='Arial,18', width=10, bd=5, bg='orange', fg='black')
        self.label2.place(x=40, y=54)

        self.label3 = Label(self.root, text='Tasks', font='Arial,18', width=10, bd=5, bg='orange', fg='black')
        self.label3.place(x=320, y=54)

        self.tree = ttk.Treeview(self.root, columns=('Task', 'Due Date', 'Priority', 'Completed'), show='headings')
        self.tree.heading('Task', text='Task')
        self.tree.heading('Due Date', text='Due Date')
        self.tree.heading('Priority', text='Priority')
        self.tree.heading('Completed', text='Completed')
        self.tree.column('Task', width=240)
        self.tree.column('Due Date', width=80)
        self.tree.column('Priority', width=50)
        self.tree.column('Completed', width=70)
        self.tree.place(x=200, y=100)

        self.text = Entry(self.root, bd=5, width=15, font='Arial,10')
        self.text.place(x=20, y=100)

        self.label_due = Label(self.root, text='Due Date', font='Arial,12', width=8, bd=3, bg='orange', fg='black')
        self.label_due.place(x=20, y=150)
        
        self.due_date = Entry(self.root, bd=5, width=15, font='Arial,10')
        self.due_date.place(x=20, y=180)

        self.label_priority = Label(self.root, text='Priority', font='Arial,12', width=8, bd=3, bg='orange', fg='black')
        self.label_priority.place(x=20, y=220)

        self.priority_var = StringVar()
        self.priority_var.set("Low")
        self.priority_menu = OptionMenu(self.root, self.priority_var, "Low", "Medium", "High")
        self.priority_menu.config(width=10)
        self.priority_menu.place(x=20, y=250)

        def add():
            content = self.text.get()
            due_date = self.due_date.get()
            priority = self.priority_var.get()
            if content.strip():
                task_info = f"{content}, {due_date}, {priority}, No"
                self.tree.insert('', 'end', values=(content, due_date, priority, "No"))
                with open('data.txt', 'a') as file:
                    file.write(task_info + '\n')
                self.text.delete(0, END)
                self.due_date.delete(0, END)
            else:
                messagebox.showwarning("Empty Task", "Please enter a task.")

        def delete():
            selected_item = self.tree.selection()[0]
            task = self.tree.item(selected_item)['values'][0]
            self.tree.delete(selected_item)
            with open('data.txt', 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if task not in line:
                        file.write(line)
                file.truncate()

        def mark_completed():
            selected_item = self.tree.selection()[0]
            task_index = self.tree.index(selected_item)
            completed = self.tree.item(selected_item, 'values')[3]
            if completed == "No":
                self.tree.item(selected_item, values=(self.tree.item(selected_item, 'values')[0], self.tree.item(selected_item, 'values')[1], self.tree.item(selected_item, 'values')[2], "Yes"))
                with open('data.txt', 'r') as file:
                    lines = file.readlines()
                with open('data.txt', 'w') as file:
                    for line in lines:
                        if line.startswith(self.tree.item(selected_item, 'values')[0]):
                            line = line.replace("No", "Yes")
                        file.write(line)
            else:
                self.tree.item(selected_item, values=(self.tree.item(selected_item, 'values')[0], self.tree.item(selected_item, 'values')[1], self.tree.item(selected_item, 'values')[2], "No"))
                with open('data.txt', 'r') as file:
                    lines = file.readlines()
                with open('data.txt', 'w') as file:
                    for line in lines:
                        if line.startswith(self.tree.item(selected_item, 'values')[0]):
                            line = line.replace("Yes", "No")
                        file.write(line)

        try:
            with open('data.txt', 'r') as file:
                for line in file:
                    task, due_date, priority, completed = line.strip().split(', ')
                    self.tree.insert('', 'end', values=(task, due_date, priority, completed))
        except FileNotFoundError:
            pass

        self.button = Button(self.root, text='Add', font='Arial,20', width=10, bd=5, bg='orange', fg='black', command=add)
        self.button.place(x=20, y=290)

        self.button2 = Button(self.root, text='Delete', font='Arial,20', width=10, bd=5, bg='orange', fg='black', command=delete)
        self.button2.place(x=20, y=350)

        self.button3 = Button(self.root, text='Mark as Completed', font='Arial,12', width=15, bd=3, bg='orange', fg='black', command=mark_completed)
        self.button3.place(x=200, y=350)

def main():
    root = Tk()
    ui = Todo(root)
    root.mainloop()

if __name__ == "__main__":
    main()
