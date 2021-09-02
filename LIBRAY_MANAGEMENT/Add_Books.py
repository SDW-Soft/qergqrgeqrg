from tkinter import *
from tkinter import messagebox, ttk
from tkcalendar import Calendar,DateEntry
import mysql.connector
from mysql.connector import Error
import os
import sys
py = sys.executable

#creating window
class Add(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'libico.ico')
        self.maxsize(480,600)
        self.minsize(480,600)
        self.title('Ajouter un livre')
        self.canvas = Canvas(width=500, height=700, bg='#e5e5e5')
        self.canvas.pack()
        a = StringVar()
        b = StringVar()
        cat = StringVar()
        c = StringVar()
        pa = StringVar()
        pv = StringVar()
        e = StringVar()
        q = IntVar()
        #verifying Input
        def b_q():
            if len(b.get()) == 0:
                messagebox.showerror("Error","Please Enter The Details")
            else:
                g = 'YES'
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                    self.myCursor = self.conn.cursor()
                    self.myCursor.execute("select * from categories WHERE name=%s", [cat.get()])
                    idkey = self.myCursor.fetchall()
                    for row in idkey:
                        id=row[0]
                    print(id)
                    self.myCursor = self.conn.cursor()
                    self.myCursor.execute("Insert into book(name,author,availability, buy, sell, category_id, edition) values (%s,%s,%s,%s,%s,%s,%s)",[b.get(),c.get(),q.get(),pa.get(), pv.get(), int(id), e.get()])
                    self.conn.commit()
                    messagebox.showinfo('Info', 'Le livre a été ajouter avec succes')
                    ask = messagebox.askyesno("Confirm", "Voullez vous inséré un autre livre?")
                    if ask:
                        self.destroy()
                        os.system('%s %s' % (py, 'Add_Books.py'))
                    else:
                        self.destroy()
                except Error:
                    messagebox.showerror("Error","Vérifier vos information")
        #creating input box and label
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

        Label(self, text='Category de livre:',bg='#e5e5e5',fg='black',font=('Courier new', 10, 'bold')).place(x=20, y=150)
        ttk.Combobox(self, textvariable=cat, values=results_for_combobox, width=40, state="readonly").place(x=160, y=150)

        Label(self, text='Ajouter un livre',bg='#e5e5e5',fg='black',font=('Courier new', 20, 'bold')).place(x=120, y=40)
        Label(self, text='').pack()
        Label(self, text='Titre:',bg='#e5e5e5',fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=180)
        Entry(self, textvariable=b, width=30).place(x=170, y=182)
        Label(self, text='Author:',bg='#e5e5e5',fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=230)
        Entry(self, textvariable=c, width=30).place(x=170, y=232)
        Label(self, text='Prix Achat:',bg='#e5e5e5',fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=280)
        Entry(self, textvariable=pa, width=30).place(x=170, y=282)
        Label(self, text='Prix Vente:',bg='#e5e5e5',fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=320)
        Entry(self, textvariable=pv, width=30).place(x=170, y=322)
        Label(self, text='Quantite:',bg='#e5e5e5',fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=370)
        Entry(self, textvariable=q, width=30).place(x=170, y=372)
        Label(self, text='Date Edition:',bg='#e5e5e5',fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=420)
        DateEntry(self, textvariable=e, width=30).place(x=170, y=422)

        Button(self, text="Envoyer", bg="#fca311", command=b_q).place(x=245, y=470)
Add().mainloop()