from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image
import os,glob
import mysql.connector
from mysql.connector import Error

class Search(Tk):
    def __init__(self):
        super().__init__()
        f = StringVar()
        g = StringVar()
        self.title("Recherche Client")
        self.maxsize(1000, 800)
        self.minsize(1000, 800)
        self.canvas = Canvas(width=1366, height=768, bg='#e5e5e5')
        self.canvas.pack()
        self.iconbitmap(r'libico.ico')
        l1=Label(self,text="Search Student",bg='#e5e5e5', font=("Courier new",20,'bold')).place(x=290,y=40)
        l = Label(self, text="Search By",bg='#e5e5e5', font=("Courier new", 15, 'bold')).place(x=180, y=100)
        n = StringVar()
        p = StringVar()
        a = StringVar()
        e = StringVar()
        id = IntVar()
        def insert(data):
            self.listTree.delete(*self.listTree.get_children())
            for row in data:
                self.listTree.insert("","end",text = row[0], values = (row[1],row[2],row[3], row[4]))

        def asi():
            if len(n.get()) < 1:
                messagebox.showinfo("Oop's", "Ajouter le nom svp")
            elif len(p.get()) < 1:
                messagebox.showinfo("Oop's","Ajouter numéro de téléphone svp")
            elif len(a.get()) < 1:
                messagebox.showinfo("Oop's", "Ajouter L'addresse svp")
            else:
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                                        database='library',
                                                        user='root',
                                                        password='')
                    self.myCursor = self.conn.cursor()
                    name1 = n.get()
                    id1=id.get()
                    pn1 = p.get()
                    add1 = a.get()
                    email = e.get()
                    self.myCursor.execute("UPDATE student SET name=%s, phone_number=%s, address=%s , email=%s WHERE stud_id=%s",(name1,pn1,add1, email, id1))
                    self.conn.commit()
                    messagebox.showinfo("Done","Le Client a été ajouter avec succes")
                    ask = messagebox.askyesno("Confirm","Voullez vous modifier un autre client?")
                    if ask:
                     self.destroy()
                     os.system('%s %s' % (py, 'Search_Student.py'))
                    else:
                     self.destroy()
                     self.myCursor.close()
                     self.conn.close()
                except Error:
                    messagebox.showerror("Error","Erreur essayez plus tard s'il vous plaît")


        def ge():
            if (len(self.entry.get())) == 0:
                messagebox.showinfo('Error', 'First select a item')
            elif (len(self.combo.get())) == 0:
                messagebox.showinfo('Error', 'Enter the '+self.combo.get())
            elif self.combo.get() == 'Name':
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                    self.mycursor = self.conn.cursor()
                    name = self.entry.get()
                    self.mycursor.execute("Select * from student where name like %s",['%'+name+'%'])
                    pc = self.mycursor.fetchall()
                    if pc:
                        insert(pc)
                    else:
                        messagebox.showinfo("Oop's","Name not found")
                except Error:
                    messagebox.showerror("Error", "Something goes wrong")
            elif self.combo.get() == 'ID':
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                    self.mycursor = self.conn.cursor()
                    id = self.entry.get()
                    self.mycursor.execute("Select * from student where stud_id = %s", [int(id)])
                    pc = self.mycursor.fetchall()
                    n.set(pc[0][1])
                    p.set(pc[0][2])
                    a.set(pc[0][3])
                    e.set(pc[0][4])
                    if pc:
                        insert(pc)
                        self.c.config(state="normal")
                        self.d.config(state="normal")
                    else:
                        messagebox.showinfo("Oop's", "Id not found")
                except Error:
                    messagebox.showerror("Error", "Something goes wrong")




        self.b= Button(self,text="Rechercher", bg="#fca311" ,width=10,font=("Courier new",8,'bold'),command= ge )
        self.b.id="search"
        self.b.place(x=300,y=170)

        self.c= Button(self,text="Modifier", bg="#fca311", width=10,font=("Courier new",8,'bold'),command= ge )
        self.c.id = "update"
        self.c.place(x=410,y=170)
        self.c.config(state="disabled")
        self.d= Button(self,text="Supprimer", bg="#fca311", width=10,font=("Courier new",8,'bold'),command= ge )
        self.d.id="delete"
        self.d.place(x=510,y=170)
        self.d.config(state="disabled")

        self.combo=ttk.Combobox(self,textvariable=g,values=["Name","ID"],width=40,state="readonly")
        self.combo.place(x = 310, y = 105)
        self.entry = Entry(self,textvariable=f,width=43)
        self.entry.place(x=310,y=145)
        self.la = Label(self, text="Enter",bg = '#e5e5e5', font=("Courier new", 15, 'bold')).place(x=180, y=140)

        def handle(event):
            if self.listTree.identify_region(event.x,event.y) == "separator":
                return "break"

        def selectItem(r):
            curItem = self.listTree.focus()
            idx = self.listTree.item(curItem)
            print(idx)
            n.set(idx['values'][0])
            p.set(idx['values'][1])
            a.set(idx['values'][2])
            e.set(idx['values'][3])
            id.set(int(idx['text']))

        self.listTree = ttk.Treeview(self, height=13,columns=('Student Name', 'Phone Number', 'Address', 'Email','Id'))
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        self.listTree.configure(yscrollcommand=self.vsb.set)
        self.listTree.heading("#0", text='Student ID', anchor='w')
        self.listTree.column("#0", width=100, anchor='w')
        self.listTree.heading("Student Name", text='Student Name')
        self.listTree.column("Student Name", width=200, anchor='center')
        self.listTree.heading("Phone Number", text='Phone Number')
        self.listTree.column("Phone Number", width=200, anchor='center')
        self.listTree.heading("Address", text='Address')
        self.listTree.column("Address", width=200, anchor='center')
        self.listTree.heading("Email", text='Email')
        self.listTree.column("Email", width=200, anchor='center')


        self.listTree.place(x=40, y=200)
        self.vsb.place(x=943,y=200,height=287)
        ttk.Style().configure("Treeview", font=('Times new Roman', 15))
        self.listTree.bind('<ButtonRelease-1>', selectItem)

        Label(self, text='Student Details', bg='#e5e5e5', fg='white', font=('Courier new', 20, 'bold')).place(x=70,y=490)
        Label(self, text='Name:', bg='#e5e5e5', font=('Courier new', 10, 'bold')).place(x=70, y=532)
        Entry(self, textvariable=n, width=30).place(x=200, y=534)
        Label(self, text='Phone Number:', bg='#e5e5e5', font=('Courier new', 10, 'bold')).place(x=70, y=580)
        Entry(self, textvariable=p, width=30).place(x=200, y=582)
        Label(self, text='Address:', bg='#e5e5e5', font=('Courier new', 10, 'bold')).place(x=70, y=630)
        Entry(self, textvariable=a, width=30).place(x=200, y=632)
        Label(self, text='Email:', bg='#e5e5e5', font=('Courier new', 10, 'bold')).place(x=70, y=680)
        Entry(self, textvariable=e, width=30).place(x=200, y=682)
        Label(self, text='Id:', bg='#e5e5e5', font=('Courier new', 10, 'bold')).place(x=70, y=730)
        Entry(self, textvariable=id, width=30).place(x=200, y=732)

        Button(self, text="Submit", bg="#fca311", width=15, command=asi).place(x=230, y=780)
        conn = mysql.connector.connect(host='localhost',
                                       database='library',
                                       user='root',
                                       password='')
        mycursor = conn.cursor()
        mycursor.execute("Select * from student")
        pc = mycursor.fetchall()
        print(pc)
        if pc:
            insert(pc)
        else:
            messagebox.showinfo("Oop's", "Name not found")
Search().mainloop()