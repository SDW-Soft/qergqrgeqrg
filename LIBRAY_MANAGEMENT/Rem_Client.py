from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
#creating widow
class Rem(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'libico.ico')
        self.maxsize(400, 200)
        self.minsize(400, 200)
        self.title("Supprimer un Client")
        self.canvas = Canvas(width=1366, height=768, bg='#e5e5e5')
        self.canvas.pack()
        a = StringVar()
        def ent():
            if len(a.get()) ==0:
                messagebox.showinfo("Error","Verifier l Id")
            else:
                d = messagebox.askyesno("Confirm", "Voullez vous vraiment supprimer ce client?")
                if d:
                    try:
                        self.conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                        self.myCursor = self.conn.cursor()
                        self.myCursor.execute("Delete from student where id = %s",[a.get()])
                        self.conn.commit()
                        self.myCursor.close()
                        self.conn.close()
                        messagebox.showinfo("Confirm","Le Client a été supprimer")
                        a.set("")
                    except:
                        messagebox.showerror("Error","Something goes wrong")
        Label(self, text = "Client Id: ",bg='#e5e5e5',fg='black',font=('Courier new', 15, 'bold')).place(x = 5,y = 40)
        Entry(self,textvariable = a,width = 37).place(x = 160,y = 44)
        Button(self, text='Supprimer', bg="#fca311", width=15, font=('arial', 10),command = ent).place(x=200, y = 90)



Rem().mainloop()