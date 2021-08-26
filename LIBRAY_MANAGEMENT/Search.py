from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from tkcalendar import Calendar,DateEntry


class Search(Tk):
    def __init__(self):
        super().__init__()
        f = StringVar()
        g = StringVar()
        self.title("Rechercher un livre")
        self.maxsize(1500, 950)
        self.minsize(1500, 950)
        self.canvas = Canvas(width=1500, height=950, bg='gray')
        self.canvas.pack()
        self.iconbitmap(r'libico.ico')
        l1=Label(self,text="Search Library",bg='gray', font=("Courier new",20,'bold')).place(x=290,y=20)
        l = Label(self, text="Search By",bg='gray', font=("Courier new", 15, 'bold')).place(x=60, y=96)

        a = StringVar()
        book = StringVar()
        cat = StringVar()
        author = StringVar()
        pa = StringVar()
        pv = StringVar()
        edition = StringVar()
        qte = IntVar()
        def insert(data):
            self.listTree.delete(*self.listTree.get_children())
            for row in data:
                self.listTree.insert("", 'end', text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6], row[8]))
        def b_q():
            self.conn = mysql.connector.connect(host='localhost',
                                                database='library',
                                                user='root',
                                                password='')
            self.myCursor = self.conn.cursor()
            self.myCursor.execute("select * from categories WHERE name=%s", [cat.get()])
            idkey = self.myCursor.fetchall()
            for row in idkey:
                id = row[0]

            curItem = self.listTree.focus()
            idx = self.listTree.item(curItem)
            idbook = int(idx['text'])

            self.myCursor = self.conn.cursor()
            self.myCursor.execute(
                "UPDATE book SET name=%s,author=%s,availability=%s, buy=%s, sell=%s, category_id=%s, edition=%s WHERE book_id=%s", [book.get(), author.get(), qte.get(), pa.get(), pv.get(), int(id), edition.get(), idbook])
            self.conn.commit()
            messagebox.showinfo('Info', 'Le livre a été modifier avec succes')
            ask = messagebox.askyesno("Confirm", "Voullez vous inséré un autre livre?")
            if ask:
                self.destroy()
                os.system('%s %s' % (py, 'Add_Books.py'))
            else:
                self.destroy()
        def ge():
            if (len(g.get())) == 0:
                messagebox.showinfo('Error', 'First select a item')
            elif (len(f.get())) == 0:
                messagebox.showinfo('Error', 'Enter the '+g.get())
            elif g.get() == 'Book Name':
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select * from book where name LIKE %s",['%'+f.get()+'%'])
                    self.pc = self.mycursor.fetchall()
                    if self.pc:
                        insert(self.pc)
                    else:
                        messagebox.showinfo("Oop's","Either Book Name is incorrect or it is not available")
                except Error:
                    messagebox.showerror("Error","Something goes wrong")
            elif g.get() == 'Author Name':
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select * from book where author LIKE %s", ['%'+f.get()+'%'])
                    self.pc = self.mycursor.fetchall()
                    if self.pc:
                        insert(self.pc)
                    else:
                        messagebox.showinfo("Oop's","Author Name not found")
                except Error:
                    messagebox.showerror("Error","Something goes wrong")
            elif g.get() == 'Book Id':
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select * from book where book_id LIKE %s", ['%'+f.get()+'%'])
                    self.pc = self.mycursor.fetchall()
                    if self.pc:
                        insert(self.pc)
                    else:
                        messagebox.showinfo("Oop's","Either Book Id is incorrect or it is not available")
                except Error:
                    messagebox.showerror("Error","Something goes wrong")
        b=Button(self,text="Find",width=15,bg='gray',font=("Courier new",10,'bold'),command=ge).place(x=460,y=148)
        c=ttk.Combobox(self,textvariable=g,values=["Book Name","Author Name","Book Id"],width=40,state="readonly").place(x = 180, y = 100)
        en = Entry(self,textvariable=f,width=43).place(x=180,y=155)
        la = Label(self, text="Enter",bg='gray', font=("Courier new", 15, 'bold')).place(x=100, y=150)

        def selectItem(event):
            curItem = self.listTree.focus()
            idx = self.listTree.item(curItem)
            print(idx['values'])
            book.set(idx['values'][0])
            author.set(idx['values'][1])
            pa.set(idx['values'][2])
            pv.set(idx['values'][3])
            qte.set(idx['values'][4])
            edition.set(idx['values'][5])
            #id.set(int(idx['text']))
            #print(combobox.findText(idx['values'][6]));
            cat.set(idx['values'][6])


        self.listTree = ttk.Treeview(self, height=13,columns=('Book Name', 'Book Author', 'Availability', 'Prix Achat', 'Prix Vente', 'Date Edition', 'Category'))
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        self.hsb = ttk.Scrollbar(self,orient="horizontal",command=self.listTree.yview)
        self.listTree.configure(yscrollcommand=self.vsb.set)
        self.listTree.heading("#0", text='Book ID', anchor='center')
        self.listTree.column("#0", width=120, anchor='center')
        self.listTree.heading("Book Name", text='Book Name')
        self.listTree.column("Book Name", width=200, anchor='center')
        self.listTree.heading("Book Author", text='Book Author')
        self.listTree.column("Book Author", width=200, anchor='center')
        self.listTree.heading("Availability", text='Availability')
        self.listTree.column("Availability", width=200, anchor='center')
        self.listTree.heading("Prix Achat", text='Prix Achat')
        self.listTree.column("Prix Achat", width=200, anchor='center')
        self.listTree.heading("Prix Vente", text='Prix Vente')
        self.listTree.column("Prix Vente", width=200, anchor='center')
        self.listTree.heading("Date Edition", text='Date Edition')
        self.listTree.column("Date Edition", width=200, anchor='center')
        self.listTree.heading("Category", text='Category')
        self.listTree.column("Category", width=200, anchor='center')
        self.listTree.bind('<ButtonRelease-1>', selectItem)
        #self.listTree.bind('<Button-1>', handle)
        self.listTree.place(x=40, y=200)
        #self.vsb.place(x=763,y=200,height=287)
        ttk.Style().configure("Treeview", font=('Times new Roman', 15))

        self.conn = mysql.connector.connect(host='localhost',
                                            database='library',
                                            user='root',
                                            password='')
        self.myCursor = self.conn.cursor()
        self.myCursor.execute("select * from categories")
        results = self.myCursor.fetchall()
        self.myCursor.close()
        self.conn.close()
        results_for_combobox = [result[1] for result in results]

        Label(self, text='').pack()

        Label(self, text='Book Category:', bg='gray', fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=540)
        combobox = ttk.Combobox(self, textvariable=cat, values=results_for_combobox, width=40, state="readonly").place(x=160,
                                                                                                            y=540)

        Label(self, text='Book Details:', bg='gray', fg='black', font=('Courier new', 20, 'bold')).place(x=170, y=490)
        Label(self, text='').pack()
        Label(self, text='Titre:', bg='gray', fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=590)
        Entry(self, textvariable=book, width=30).place(x=170, y=592)
        Label(self, text='Author:', bg='gray', fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=640)
        Entry(self, textvariable=author, width=30).place(x=170, y=642)
        Label(self, text='Prix Achat:', bg='gray', fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=690)
        Entry(self, textvariable=pa, width=30).place(x=170, y=692)
        Label(self, text='Prix Vente:', bg='gray', fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=740)
        Entry(self, textvariable=pv, width=30).place(x=170, y=742)
        Label(self, text='Quantite:', bg='gray', fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=790)
        Entry(self, textvariable=qte, width=30).place(x=170, y=792)
        Label(self, text='Date Edition:', bg='gray', fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=840)
        DateEntry(self, textvariable=edition, width=30).place(x=170, y=842)

        Button(self, text="Submit", command=b_q).place(x=245, y=890)

        conn = mysql.connector.connect(host='localhost',
                                       database='library',
                                       user='root',
                                       password='')
        mycursor = conn.cursor()
        mycursor.execute("Select b.*, c.name, c.id as cid from book b LEFT JOIN categories c ON c.id=b.category_id")
        pc = mycursor.fetchall()
        print(pc)
        if pc:
            insert(pc)
        else:
            messagebox.showinfo("Oop's", "Name not found")
Search().mainloop()