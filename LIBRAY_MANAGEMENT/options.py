from tkinter import *
import tkinter as tk
from tkinter import messagebox
import os
import sys
from tkinter import ttk
from PIL import ImageTk, Image
import mysql.connector
from mysql.connector import Error

py=sys.executable

#creating window
class MainWin(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'libico.ico')
        self.configure(bg='gray')
        image = ImageTk.PhotoImage(file='index.jpg')
        self.canvas = Canvas(width=1366, height=768, bg='gray')
        self.canvas.create_image(1366, 768, image=image, anchor= NW)
        self.canvas.pack()

        #window = tk.Toplevel()
        #window.title("Join")
        #window.geometry("300x300")
        #window.configure(background='grey')
        #img = ImageTk.PhotoImage(Image.open('index.jpg'))
        #panel = tk.Label(window, image=img)
        #panel.pack(side="bottom", fill="both", expand="yes")
        #window.mainloop()


        self.maxsize(1320, 768)
        self.minsize(1320,768)
        self.state('zoomed')
        self.title('GESTION DES BIBLIOTHEQUE')
        self.a = StringVar()
        self.b = StringVar()
        self.mymenu = Menu(self)
#calling scripts
        def a_s():
            os.system('%s %s' % (py, 'Add_Student.py'))

        def a_b():
            os.system('%s %s' % (py, 'Add_Books.py'))

        def a_c():
            os.system('%s %s' % (py, 'Add_Category.py'))

        def r_b():
            os.system('%s %s' % (py, 'remove_book.py'))

        def r_s():
            os.system('%s %s' % (py, 'Remove_student.py'))

        def ib():
            os.system('%s %s' % (py, 'issueTable.py'))

        def ret():
            os.system('%s %s' % (py, 'ret.py'))

        def sea():
            os.system('%s %s' % (py,'Search.py'))

        def log():
            conf = messagebox.askyesno("Confirm", "Êtes-vous sûr de vouloir vous déconnecter?")
            if conf:
             self.destroy()
             os.system('%s %s' % (py, 'Main.py'))



      # def handle(event):
        #     if self.listTree.identify_region(event.x,event.y) == "separator":
        #         return "break"
        def add_user():
            os.system('%s %s' % (py, 'Reg.py'))
        def rem_user():
            os.system('%s %s' % (py, 'Rem.py'))

        def add_cat():
            os.system('%s %s' % (py, 'Add_Category.py'))
        def add_fou():
            os.system('%s %s' % (py, 'Add_Provider.py'))
        def sest():
            os.system('%s %s' % (py,'Search_Student.py'))
        def adbk():
            os.system('%s %s' % (py,'Add_Books.py'))
        def adst():
            os.system('%s %s' % (py,'Add_Student.py'))
#creating table

        self.listTree = ttk.Treeview(self,height=14,columns=('Client','Livre',"Date d'émission",'Date de retour'))
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        self.hsb = ttk.Scrollbar(self,orient="horizontal",command=self.listTree.xview)
        self.listTree.configure(yscrollcommand=self.vsb.set,xscrollcommand=self.hsb.set)
        self.listTree.heading("#0", text='ID')
        self.listTree.column("#0", width=50,minwidth=50,anchor='center')
        self.listTree.heading("Client", text='Student')
        self.listTree.column("Client", width=200, minwidth=200,anchor='center')
        self.listTree.heading("Livre", text='Book')
        self.listTree.column("Livre", width=200, minwidth=200,anchor='center')
        self.listTree.heading("Date d'émission", text='Issue Date')
        self.listTree.column("Date d'émission", width=125, minwidth=125,anchor='center')
        self.listTree.heading("Date de retour", text='Return Date')
        self.listTree.column("Date de retour", width=125, minwidth=125, anchor='center')

        self.listTree.place(x=320,y=360)
        self.vsb.place(x=1028,y=361,height=287)
        self.hsb.place(x=320,y=650,width=700)
        ttk.Style().configure("Treeview",font=('Times new Roman',15))

        list1 = Menu(self)
        list1.add_command(label="Client", command=a_s)
        list1.add_command(label="Livre", command=a_b)

        list3 = Menu(self)
        list3.add_command(label = "Ajouter un utilisateur",command = add_user)
        list3.add_command(label = "Supprimer l'utilisateur",command = rem_user)
        list3.add_command(label="Fournisseur", command=add_fou)
        list3.add_command(label= "Ajouter Category", command = add_cat)


        self.mymenu.add_cascade(label='Ajouter', menu=list1)
        self.mymenu.add_cascade(label = "Les outils d'administration ", menu = list3)

        self.config(menu=self.mymenu)

        def ser():
            if(len(self.studid.get())==0):
                messagebox.showinfo("Error", "Empty Field!")
            else:

             try:
                conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                cursor = conn.cursor()
                change = int(self.studid.get())
                cursor.execute("Select bi.issue_id,s.name,b.name,bi.issue_date,bi.return_date from issue_book bi,student s,book b where s.stud_id = bi.stud_id and b.book_id = bi.book_id and s.stud_id = %s",[change])
                pc = cursor.fetchall()
                if pc:
                    self.listTree.delete(*self.listTree.get_children())
                    for row in pc:
                        self.listTree.insert("",'end',text=row[0] ,values = (row[1],row[2],row[3],row[4]))
                else:
                    messagebox.showinfo("Error", "Either ID is wrong or The book is not yet issued on this ID")
             except Error:
                #print(Error)
              messagebox.showerror("Error","Quelque chose ne va pas")
        def ent():
            if (len(self.bookid.get()) == 0):
                messagebox.showinfo("Error", "Champ vide!")
            else:
             try:
                self.conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                self.myCursor = self.conn.cursor()
                book = int(self.bookid.get())
                self.myCursor.execute("Select bi.issue_id,s.name,b.name,bi.issue_date,bi.return_date from issue_book bi,student s,book b where s.stud_id = bi.stud_id and b.book_id = bi.book_id and b.book_id = %s",[book])
                self.pc = self.myCursor.fetchall()
                if self.pc:
                    self.listTree.delete(*self.listTree.get_children())
                    for row in self.pc:
                        self.listTree.insert("", 'end', text=row[0],values=(row[1], row[2], row[3], row[4]))
                else:
                    messagebox.showinfo("Error", "Either ID is wrong or The book is not yet issued")
             except Error:
                messagebox.showerror("Error", "Something Goes Wrong")

        def check():
            try:
                conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                mycursor = conn.cursor()
                mycursor.execute("Select * from admin")
                z = mycursor.fetchone()
                if not z:
                    messagebox.showinfo("Error", "Please Register A user")
                    x = messagebox.askyesno("Confirm","Do you want to register a user")
                    if x:
                        self.destroy()
                        os.system('%s %s' % (py, 'Reg.py'))
                else:

                    #label and input box
                    self.label3 = Label(self, text='SYSTÈME DE GESTION DE LA BIBLIOTHÈQUE',fg='black',bg="gray" ,font=('Courier new', 30, 'bold'))
                    self.label3.place(x=350, y=22)
                    self.label4 = Label(self, text="ENTRER CLIENT",bg="gray", font=('Courier new', 18, 'bold'))
                    self.label4.place(x=130, y=107)
                    self.studid = Entry(self, textvariable=self.a, width=90)
                    self.studid.place(x=405, y=110)
                    self.srt = Button(self, text='Rechercher', width=15, font=('arial', 10),command = ser).place(x=1000, y=106)
                    self.label5 = Label(self, text="ENTRER L'ID DU LIVRE",bg="gray", font=('Courier new', 18, 'bold'))
                    self.label5.place(x=75, y=150)
                    self.bookid = Entry(self, textvariable=self.b, width=90)
                    self.bookid.place(x=405, y=160)
                    self.brt = Button(self, text='Trouve', width=15, font=('arial', 10),command = ent).place(x=1000, y=150)
                    self.label6 = Label(self, text="INFORMATIONS DÉTAILS",bg="gray",  font=('Courier new', 15, 'underline', 'bold'))
                    self.label6.place(x=560, y=300)
                    self.button = Button(self, text='Rechercher un étudiant', width=25, font=('Courier new', 10), command=sest).place(x=240,y=250)
                    self.button = Button(self, text='Rechercher un livre', width=25, font=('Courier new', 10), command=sea).place(x=520,y=250)
                    self.brt = Button(self, text="émettre livre", width=15, font=('Courier new', 10), command=ib).place(x=800, y=250)
                    self.brt = Button(self, text="Livre de retour", width=15, font=('Courier new', 10), command=ret).place(x=1000, y=250)
                    self.brt = Button(self, text="SE DÉCONNECTER", width=15,bg="red", font=('Courier new', 10), command=log).place(x=1150, y=105)
            except Error:
                messagebox.showerror("Error", "Quelque chose ne va pas")
        check()

MainWin().mainloop()
