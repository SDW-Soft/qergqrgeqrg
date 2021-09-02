from tkinter import *
from tkinter import messagebox
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
        self.maxsize(480,360 )
        self.minsize(480,360)
        self.title('Ajouter un type de livre')
        self.canvas = Canvas(width=500, height=500, bg='#e5e5e5')
        self.canvas.pack()
        a = StringVar()
        b = StringVar()
        c = StringVar()
        #verifying Input
        def b_q():
            if len(b.get()) == 0:
                messagebox.showerror("Error","Remplir tout les champs")
            else:
                g = 'YES'
                try:
                    self.conn = mysql.connector.connect(host='localhost',
                                         database='library',
                                         user='root',
                                         password='')
                    self.myCursor = self.conn.cursor()
                    self.myCursor.execute("Insert into categories(name) values (%s)",[b.get()])
                    self.conn.commit()
                    messagebox.showinfo('Info', "les données a été insérer avec succes")
                    ask = messagebox.askyesno("Confirm", "Voullez vous insérer une autre catégorie")
                    if ask:
                        self.destroy()
                        os.system('%s %s' % (py, 'Add_Category.py'))
                    else:
                        self.destroy()
                except Error:
                    messagebox.showerror("Error","Vérifier les données")
        #creating input box and label
        Label(self, text='').pack()
        Label(self, text='Détails de Categorie',bg='#e5e5e5',fg='black',font=('Courier new', 20, 'bold')).place(x=45, y=70)
        Label(self, text='').pack()
        Label(self, text='Nom:',bg='#e5e5e5',fg='black', font=('Courier new', 10, 'bold')).place(x=60, y=180)
        Entry(self, textvariable=b, width=30).place(x=170, y=182)
        Button(self, text="Envoyer", command=b_q).place(x=245, y=300)
Add().mainloop()