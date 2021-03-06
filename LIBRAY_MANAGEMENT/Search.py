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
        self.canvas = Canvas(width=1500, height=950, bg='#e5e5e5')
        self.canvas.pack()
        self.iconbitmap(r'libico.ico')
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
            elif g.get() == 'Nom de livre':
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select b.*, c.name, c.id as cid from book b LEFT JOIN categories c ON c.id=b.category_id where b.name LIKE %s",['%'+f.get()+'%'])
                    self.pc = self.mycursor.fetchall()
                    if self.pc:
                        insert(self.pc)
                    else:
                        messagebox.showinfo("Oop's","Either Book Name is incorrect or it is not available")
                except Error:
                    messagebox.showerror("Error","Something goes wrong")
            elif g.get() == 'Author':
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select b.*, c.name, c.id as cid from book b LEFT JOIN categories c ON c.id=b.category_id where b.author LIKE %s", ['%'+f.get()+'%'])
                    self.pc = self.mycursor.fetchall()
                    if self.pc:
                        insert(self.pc)
                    else:
                        messagebox.showinfo("Oop's","Author Name not found")
                except Error:
                    messagebox.showerror("Error","Something goes wrong")
            elif g.get() == 'Livre Id':
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select b.*, c.name, c.id as cid from book b LEFT JOIN categories c ON c.id=b.category_id where b.book_id = %s", [f.get()])
                    self.pc = self.mycursor.fetchall()
                    if self.pc:
                        insert(self.pc)
                    else:
                        messagebox.showinfo("Oop's","Either Book Id is incorrect or it is not available")
                except Error:
                    messagebox.showerror("Error","Something goes wrong")
        l1=Label(self,text="Rechercher dans la bibliotheque",bg='#e5e5e5', font=("Courier new",20,'bold')).place(x=350,y=20)
        l = Label(self, text="Chercher avec",bg='#e5e5e5', font=("Courier new", 15, 'bold')).place(x=60, y=96)



        b=Button(self,text="Rechercher",width=15,bg='#fca311',font=("Courier new",10,'bold'),command=ge).place(x=1060,y=96)
        c=ttk.Combobox(self,textvariable=g,values=["Nom de livre","Author","Livre Id"],width=40,state="readonly").place(x = 780, y = 96)
        en = Entry(self,textvariable=f,width=43).place(x=280,y=96)
        la = Label(self, text="Enter",bg='#e5e5e5', font=("Courier new", 15, 'bold')).place(x=700, y=93)

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


        self.listTree = ttk.Treeview(self, height=13,columns=('Nom de livre', 'Author', 'Quantité', 'Prix Achat', 'Prix Vente', 'Date Edition', 'Category'))
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        self.hsb = ttk.Scrollbar(self,orient="horizontal",command=self.listTree.yview)
        self.listTree.configure(yscrollcommand=self.vsb.set)
        self.listTree.heading("#0", text='Book ID', anchor='center')
        self.listTree.column("#0", width=120, anchor='center')
        self.listTree.heading("Nom de livre", text='Nom de livre')
        self.listTree.column("Nom de livre", width=200, anchor='center')
        self.listTree.heading("Author", text='Author')
        self.listTree.column("Author", width=200, anchor='center')
        self.listTree.heading("Quantité", text='Quantité')
        self.listTree.column("Quantité", width=200, anchor='center')
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

        Label(self, text='Categorie de livre:', bg='#e5e5e5', fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=540)
        combobox = ttk.Combobox(self, textvariable=cat, values=results_for_combobox, width=150, state="readonly").place(x=170,
                                                                                                            y=540)

        Label(self, text='Livre information', bg='#e5e5e5', fg='black', font=('Courier new', 20, 'bold')).place(x=170, y=490)
        Label(self, text='').pack()
        Label(self, text='Titre:', bg='#e5e5e5', fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=590)
        Entry(self, textvariable=book, width=60).place(x=170, y=592)
        Label(self, text='Author:', bg='#e5e5e5', fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=640)
        Entry(self, textvariable=author, width=60).place(x=170, y=642)
        Label(self, text='Prix Achat:', bg='#e5e5e5', fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=690)
        Entry(self, textvariable=pa, width=60).place(x=170, y=692)

        Label(self, text='Prix Vente:', bg='#e5e5e5', fg='black', font=('Courier new', 10, 'bold')).place(x=660, y=590)
        Entry(self, textvariable=pv, width=48).place(x=800, y=590)
        Label(self, text='Quantite:', bg='#e5e5e5', fg='black', font=('Courier new', 10, 'bold')).place(x=660, y=640)
        Entry(self, textvariable=qte, width=48).place(x=800, y=640)
        Label(self, text='Date Edition:', bg='#e5e5e5', fg='black', font=('Courier new', 10, 'bold')).place(x=660, y=690)
        DateEntry(self, textvariable=edition, width=45).place(x=800, y=690)

        Button(self, text="Submit", bg="#fca311", command=b_q, width=130).place(x=170, y=750)

        conn = mysql.connector.connect(host='localhost',
                                       database='library',
                                       user='root',
                                       password='')
        mycursor = conn.cursor()
        mycursor.execute("Select b.*, c.name, c.id as cid from book b LEFT JOIN categories c ON c.id=b.category_id")
        pc = mycursor.fetchall()
        if pc:
            insert(pc)
        else:
            messagebox.showinfo("Oop's", "Name not found")
Search().mainloop()