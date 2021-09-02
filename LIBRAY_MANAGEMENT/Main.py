from tkinter import *
from tkinter import messagebox
import os,sys
import mysql.connector
from mysql.connector import Error
py=sys.executable


#creating window
class Lib(Tk):
    def __init__(self):
        super().__init__()
        self.a = StringVar()
        self.b = StringVar()
        self.maxsize(1200, 700)
        self.minsize(1200, 700)
        self.configure(bg="#e5e5e5")
        self.title("Bienvenu sur la bibliotheque")


#verifying input
        def chex():
            if len(self.user_text.get()) < 0:
                messagebox.showinfo(" INVALID USERNAME OR PASSWORD" )
            elif len(self.pass_text.get()) < 0:
                messagebox.showinfo(" INVALID USERNAME OR PASSWORD")
            else:
                try:
                    conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                    cursor = conn.cursor()
                    user = self.user_text.get()
                    password = self.pass_text.get()
                    cursor.execute('Select * from `admin` where user= %s AND password = %s ',(user,password,))
                    pc = cursor.fetchone()
                    if pc:
                        self.destroy()
                        os.system('%s %s' % (py, 'options.py'))
                    else:
                        print(pc)
                        messagebox.showinfo('Error', 'Username and password not found')
                        self.user_text.delete(0, END)
                        self.pass_text.delete(0, END)
                except Error:
                    messagebox.showinfo('Error',"Something Goes Wrong,Try restarting")

        def check():


                    self.label = Label(self, text="authentification", bg = '#e5e5e5' , fg = 'black', font=("courier-new", 24,'bold'))
                    self.label.place(x=550, y=90)
                    self.label1 = Label(self, text="User-Id" , bg = '#e5e5e5' , fg = 'black', font=("courier-new", 18, 'bold'))
                    self.label1.place(x=370, y=180)
                    self.user_text = Entry(self, textvariable=self.a, width=45)
                    self.user_text.place(x=480, y=190)
                    self.label2 = Label(self, text="Mot de passe" , bg = '#e5e5e5' , fg = 'black', font=("courier-new", 18, 'bold'))
                    self.label2.place(x=340, y=250)
                    self.pass_text = Entry(self, show='*', textvariable=self.b, width=45)
                    self.pass_text.place(x=480, y=255)
                    self.butt = Button(self, text="Login",bg ='white', font=10, width=8, command=chex).place(x=580, y=300)
                    self.label3 = Label(self, text="LIBRARY MANAGEMENT SYSTEM", bg='#e5e5e5', fg='black', font=("courier-new", 24, 'bold'))
                    self.label3.place(x=350, y=30)


        check()

Lib().mainloop()