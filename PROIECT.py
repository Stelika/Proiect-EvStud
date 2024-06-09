from tkinter import *
import tkinter as tk
from tkinter import ttk 
import mysql.connector
from tkinter import messagebox
import time
from winotify import Notification, audio
from email.message import EmailMessage
import os
import smtplib
import ssl
import pywhatkit 
import pyautogui as pg
import time
from datetime import datetime
import threading, time


##################################################################################################################################################

"""DATABASE"""


db = mysql.connector.connect(host='', user='', password='',
                                   database='')

if (db):
    print("Succes")
else:
    print("Fail")

mycursor = db.cursor()

##################################################################################################################################################


        


def ADD():                      
    
    ID = inputId.get()
    Nume = inputNume.get()
    Prenume = inputPrenume.get()
    Gen = inputGen.get()
    Medie = inputMedie.get()
    Profil = inputProfil.get()
    An_Studiu = inputAn.get()
    cnp = inputCNP.get()
    Nr_Telefon = inputNumar.get()
    Email = inputEmail.get()

    
    
    proceedOrNot = messagebox.askyesno("Adaugare Student", "Doresti sa continui? \nID = {}\nNume = {}\nPrenume = {}\nGen = {}\nMedie = {}\nProfil = {}\nAn_Studiu = {}\nCNP = {}\nNr_Telefon = {}\nEmail = {}".format(ID, Nume, Prenume, Gen, Medie, Profil, An_Studiu, cnp, Nr_Telefon, Email))

    if proceedOrNot == 1:

        mycursor.execute("insert into Student values ('"+ID+"', '"+Nume+"', '"+Prenume+"', '"+Gen+"', '"+Medie+"', '"+Profil+"', '"+An_Studiu+"' , '"+cnp+"', '"+Nr_Telefon+"', '"+Email+"')")
        
        toast = Notification(app_id= "Evstud",
                    title="Adaugare Student",
                    msg="Studentul a fost adaugat cu succes!",
                    duration="short",
                    icon=r'C:\Users\Gabriel\Desktop\ISM AN 2 2023-2024\Sem. 2\PA1 Hurezeanu (python)\Proiect Python\tobi.png')

        toast.show()
        
        db.commit()
        refresh()

    else:

        toast = Notification(app_id= "Evstud",
                    title="Adaugare student",
                    msg="Studentul nu a fost adaugat",
                    duration="short",
                    icon=r'C:\Users\Gabriel\Desktop\ISM AN 2 2023-2024\Sem. 2\PA1 Hurezeanu (python)\Proiect Python\tobi.png')

        toast.show()




def search():
    
    ID = inputId.get()
    nume = inputNume.get()
    Profil = inputProfil.get()

    if tree2.get_children() != ():
        tree2.delete(*tree2.get_children())

    mycursor.execute("select * from Student where nume like '"+nume+"'")

    for i in mycursor:
        tree2.insert("", 0, text=i[0], values=(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]))




def refresh():
    
    tree.delete(*tree.get_children())

    mycursor.execute("select * from Student")

    for i in mycursor:
        tree.insert("", 0, text=i[0], values=(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]))





def reset():
    
    inputId.delete(0, 40)
    inputNume.delete(0, 40)
    inputPrenume.delete(0, 40)
    inputMedie.delete(0, 40)
    inputProfil.delete(0, 40)
    inputAn.delete(0, 40)
    inputCNP.delete(0, 40)
    inputNumar.delete(0, 40)
    inputEmail.delete(0, 40)
    



def send():
    window = tk.Toplevel()
    window.geometry("300x200")
    window.title("SEND")
    text_label = tk.Label(window, text="Trimite folosind:",font="-family {Segoe UI} -size 14",anchor="center")
    text_label.pack(padx=10, pady=10)



    buttonEMAIL = tk.Button(window, text="EMAIL")
    buttonEMAIL.configure(bg="#b423d8", borderwidth="5", font="-family {Segoe UI} -size 14", fg="#000000",
                   highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''EMAIL''', command=TrimiteMesajEmail)
    
    buttonEMAIL.pack(padx=5, pady=5)


    buttonWhatapp = tk.Button(window, text="WHATAPP")
    buttonWhatapp.configure(bg="#b423d8", borderwidth="5", font="-family {Segoe UI} -size 14", fg="#000000",
                   highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''WHATAPP''', command=TrimiteMesajWhatApp)
   
    buttonWhatapp.pack(padx=5, pady=5)
    
    
    
    
def TrimiteMsjWhatapp():
    nume = inputNume.get()
    print(nume)
    mycursor.execute("select Nr_Telefon from Student where nume like '"+nume+"' ")
    nrTelefonStudent = mycursor.fetchone()

    mycursor.execute("select * from Student where nume like '"+nume+"'")
    dateStudent = mycursor.fetchall()
    

    nrStudent = ("+4" + str(nrTelefonStudent))
    print(nrStudent)

    nrTelefon = "" #phone number of the receiver

    now = datetime.now()
    hour = now.hour
    minute = now.minute


    pywhatkit.sendwhatmsg(nrTelefon, ("MESAJ TRIMIS AUTOMAT !\nDatele dvs:\n" + str(dateStudent)), hour, minute+1)

  
def TrimiteMesajWhatApp():
    toast = Notification(app_id="Evstud",
                         title="TRIMITERE MESAJ WHATAPP",
                         msg="Mesajul va fi trimis in aprox. 1 min",
                         duration="short",
                         icon=r'C:\Users\Gabriel\Desktop\ISM AN 2 2023-2024\Sem. 2\PA1 Hurezeanu (python)\Proiect Python\tobi.png')
    toast.show()

    thread = threading.Thread(target=TrimiteMsjWhatapp)
    thread.start()


    
    
def TrimiteEmail():
    
    nume = inputNume.get()
    

    mycursor.execute("select email from Student where nume like '"+nume+"' ")
    emailStudent = mycursor.fetchone()
    
    mycursor.execute("select * from Student where nume like '"+nume+"'")
    dateStudent = mycursor.fetchall()
    
    print(str(emailStudent))
    
    email_sender = ""
    email_password = ""
    email_receiver = ''

    subject = 'INFO FACULTATE'
    body = ("""MESAJ TRIMIS AUTOMAT !\nDatele dvs:\n""" + str(dateStudent))

    em= EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver, em.as_string())
 
 
 
 

def TrimiteMesajEmail():
    
    toast = Notification(app_id= "Evstud",
                    title="TRIMITERE EMAIL",
                    msg="Email ul a fost trimit cu succes !",
                    duration="short",
                    icon=r'C:\Users\Gabriel\Desktop\ISM AN 2 2023-2024\Sem. 2\PA1 Hurezeanu (python)\Proiect Python\tobi.png')

    toast.show()
    
    thread = threading.Thread(target=TrimiteEmail)
    thread.start()

 
 
 

    
    
 
##################################################################################################################################################

"""HERE IS THE STRUCTURE OF THE GRAFIC INTERFACE"""

root = Tk()  

icon = PhotoImage(file=r'C:\Users\Gabriel\Desktop\ISM AN 2 2023-2024\Sem. 2\PA1 Hurezeanu (python)\Proiect Python\tobi.png')
root.iconphoto(True, icon)

root.configure(bg="#201658")

titlu = Label(root, text="Evidenta Studenti", font=('family {OCR A Std}', 30, 'bold'), fg='black', bg='#0066cc',
              padx=1000, pady=5)
titlu.pack()

root.attributes('-fullscreen', True)
root.title("Evidenta Elevi")  


##################################################################################################################################################



full_info = tk.Toplevel()
full_info.title("New Window")
full_info.attributes('-fullscreen', True)
label = tk.Label(full_info)
label.pack()
    
def more():
    full_info.lift
    
    
    
##################################################################################################################################################

""" Text for the inputs """

#LABEL STANGA
labelStanga = tk.LabelFrame()
labelStanga.place(relx=0.004, rely=0.099, relheight=0.800, relwidth=0.377)
labelStanga.configure(relief='groove', text='Date Student',
                      font="-family {Segoe UI} -size 18 -weight bold -slant italic ", fg="black", bg="#98abee")

# LABEL ID STUDENT
idStudent = tk.Label(labelStanga)
idStudent.place(relx=0.077, rely=0.080, height=31, width=160, bordermode='ignore')
idStudent.configure(bg="#613b84", font="-family {Segoe UI} -size 17", fg="white", text="ID Student: ", anchor="center")

# LABEL NUME STUDENT
numeStudent = tk.Label(labelStanga)
numeStudent.place(relx=0.077, rely=0.165, height=31, width=160, bordermode='ignore')
numeStudent.configure(bg="#613b84", font="-family {Segoe UI} -size 17", fg="white", text="Nume: ", anchor="center")

# LABEL PRENUME STUDENT
prenumeStudent = tk.Label(labelStanga)
prenumeStudent.place(relx=0.077, rely=0.250, height=31, width=160, bordermode='ignore')
prenumeStudent.configure(bg="#613b84", font="-family {Segoe UI} -size 17", fg="white", text="Prenume: ",
                         anchor="center")

# LABEL GEN
genStudent = tk.Label(labelStanga)
genStudent.place(relx=0.077, rely=0.335, height=31, width=160, bordermode='ignore')
genStudent.configure(bg="#613b84", font="-family {Segoe UI} -size 17", fg="white", text="Gen Student:", anchor="center")

# LABEL medieStudent
medieStudent = tk.Label(labelStanga)
medieStudent.place(relx=0.077, rely=0.420, height=31, width=160, bordermode='ignore')
medieStudent.configure(bg="#613b84", font="-family {Segoe UI} -size 17", fg="white", text="Medie: ", anchor="center")

# LABEL PROFIL
Profil = tk.Label(labelStanga)
Profil.place(relx=0.077, rely=0.505, height=31, width=160, bordermode='ignore')
Profil.configure(bg="#613b84", font="-family {Segoe UI} -size 17", fg="white", text="Profil: ", anchor="center")

# LABEL AN STUDIU
an_Studiu = tk.Label(labelStanga)
an_Studiu.place(relx=0.077, rely=0.590, height=31, width=160, bordermode='ignore')
an_Studiu.configure(bg="#613b84", font="-family {Segoe UI} -size 17", fg="white", text="An Studiu: ", anchor="center")

# LABEL CNP
cnp = tk.Label(labelStanga)
cnp.place(relx=0.077, rely=0.675, height=31, width=160, bordermode='ignore')
cnp.configure(bg="#613b84", font="-family {Segoe UI} -size 17", fg="white", text="CNP: ", anchor="center")

# LABEL NR TELEFON
nr_telefon = tk.Label(labelStanga)
nr_telefon.place(relx=0.077, rely=0.760, height=31, width=160, bordermode='ignore')
nr_telefon.configure(bg="#613b84", font="-family {Segoe UI} -size 17", fg="white", text="Numar Telefon: ", anchor="center")

# LABEL Email
email = tk.Label(labelStanga)
email.place(relx=0.077, rely=0.845, height=31, width=160, bordermode='ignore')
email.configure(bg="#613b84", font="-family {Segoe UI} -size 17", fg="white", text="Email: ", anchor="center")



##################################################################################################################################################



inputId = tk.Entry(labelStanga)
inputId.place(relx=0.442, rely=0.080, height=30, relwidth=0.488, bordermode='ignore')
inputId.configure(bg="black", font="-family {Segoe UI} -size 14 -weight bold", fg="white")
inputId.insert(0, "")

inputNume = tk.Entry(labelStanga)
inputNume.place(relx=0.442, rely=0.165, height=29, relwidth=0.488, bordermode='ignore')
inputNume.configure(bg="black", font="-family {Segoe UI} -size 14 -weight bold", fg="white")
inputNume.insert(0, "")

inputPrenume = tk.Entry(labelStanga)
inputPrenume.place(relx=0.442, rely=0.250, height=29, relwidth=0.488, bordermode='ignore')
inputPrenume.configure(bg="black", font="-family {Segoe UI} -size 14 -weight bold", fg="white")
inputPrenume.insert(0, "")

inputGen = ttk.Combobox(root, values=["Barbat","Femeie"], state='readonly')
inputGen.pack()
inputGen.place(relx=0.171, rely=0.37, height=29)
inputGen.current(0)

inputMedie = tk.Entry(labelStanga)
inputMedie.place(relx=0.442, rely=0.420, height=29, relwidth=0.488, bordermode='ignore')
inputMedie.configure(bg="black", font="-family {Segoe UI} -size 14 -weight bold", fg="white")
inputMedie.insert(0, "")

inputProfil = tk.Entry(labelStanga)
inputProfil.place(relx=0.442, rely=0.505, height=29, relwidth=0.488, bordermode='ignore')
inputProfil.configure(bg="black", font="-family {Segoe UI} -size 14 -weight bold", fg="white")
inputProfil.insert(0, "")

inputAn = tk.Entry(labelStanga)
inputAn.place(relx=0.442, rely=0.590, height=29, relwidth=0.488, bordermode='ignore')
inputAn.configure(bg="black", font="-family {Segoe UI} -size 14 -weight bold", fg="white")
inputAn.insert(0, "")

inputCNP = tk.Entry(labelStanga)
inputCNP.place(relx=0.442, rely=0.675, height=29, relwidth=0.488, bordermode='ignore')
inputCNP.configure(bg="black", font="-family {Segoe UI} -size 14 -weight bold", fg="white")
inputCNP.insert(0, "")

inputNumar = tk.Entry(labelStanga)
inputNumar.place(relx=0.442, rely=0.760, height=29, relwidth=0.488, bordermode='ignore')
inputNumar.configure(bg="black", font="-family {Segoe UI} -size 14 -weight bold", fg="white")
inputNumar.insert(0, "")

inputEmail = tk.Entry(labelStanga)
inputEmail.place(relx=0.442, rely=0.845, height=29, relwidth=0.488, bordermode='ignore')
inputEmail.configure(bg="black", font="-family {Segoe UI} -size 14 -weight bold", fg="white")
inputEmail.insert(0, "")

##################################################################################################################################################


labelButoane = tk.Frame()
labelButoane.place(relx=0.004, rely=0.890, relheight=0.10, relwidth=0.377)
labelButoane.configure(relief='groove', borderwidth="2", bg="#E4a400")

ButonAdd = tk.Button(labelButoane)
ButonAdd.place(relx=0.020, rely=0.200, height=40, width=70)
ButonAdd.configure(bg="#b423d8", borderwidth="5", font="-family {Segoe UI} -size 14", fg="#000000",
                   highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''ADD''', command=ADD)

ButonSearch = tk.Button(labelButoane)
ButonSearch.place(relx=0.200, rely=0.200, height=40, width=85)
ButonSearch.configure(bg="#b423d8", borderwidth="5", font="-family {Segoe UI} -size 14", fg="#000000",
                      highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''SEARCH''', command= search)

ButonSend = tk.Button(labelButoane)
ButonSend.place(relx=0.410, rely=0.200, height=40, width=85)
ButonSend.configure(bg="#b423d8", borderwidth="5", font="-family {Segoe UI} -size 14", fg="#000000",
                       highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''SEND''', command=send)

ButonExit = tk.Button(titlu)
ButonExit.place(relx=0.955, rely=0.200, height=40, width=80)
ButonExit.configure(bg="#b423d8", borderwidth="5", font="-family {Segoe UI} -size 14", fg="#000000",
                    highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''EXIT''', command=root.destroy)

ButonReset = tk.Button(labelButoane)
ButonReset.place(relx=0.815, rely=0.200, height=40, width=80)
ButonReset.configure(bg="#b423d8", borderwidth="5", font="-family {Segoe UI} -size 14", fg="#000000",
                     highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''RESET''', command=reset)

ButonMore = tk.Button(labelButoane)
ButonMore.place(relx=0.610, rely=0.200, height=40, width=80)
ButonMore.configure(bg="#b423d8", borderwidth="5", font="-family {Segoe UI} -size 14", fg="#000000",
                    highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''MORE''', command=more)

ButonExit = tk.Button()
ButonExit.place(relx=0.955, rely=0.200, height=40, width=80)
ButonExit.configure(bg="#b423d8", borderwidth="5", font="-family {Segoe UI} -size 14", fg="#000000",
                    highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''EXIT''', command=root.destroy)



##################################################################################################################################################


labelDreapta = tk.Frame()
labelDreapta.place(relx=0.388, rely=0.099, relheight=0.890, relwidth=0.607)
labelDreapta.configure(relief='groove', borderwidth="2", bg="#98abee")

labelInfoStudent = tk.Label(labelDreapta)
labelInfoStudent.place(relx=0.020, rely=0.050, relheight=0.050, relwidth=0.960)
labelInfoStudent.configure(bg="#613b84", font="-family {Segoe UI} -size 17", fg="white", text="Informatii Student",
                           anchor="center")

displaySus = tk.Listbox(labelDreapta)
displaySus.place(relx=0.020, rely=0.100, relheight=0.300, relwidth=0.960)

displayJos = tk.Listbox(labelDreapta)
displayJos.place(relx=0.020, rely=0.600, relheight=0.300, relwidth=0.960)
displayJos.configure(bg="white", font="-family {Segoe UI} -size 14", fg="white", highlightbackground="white",
                     highlightcolor="black")

labelCautare = tk.Label(labelDreapta)
labelCautare.place(relx=0.020, rely=0.550, relheight=0.050, relwidth=0.960)
labelCautare.configure(bg="#613b84", font="-family {Segoe UI} -size 17", fg="white", text="Informatii Student Cautat",
                       anchor="center")


tree = ttk.Treeview(displaySus, columns=('ID', ' Nume', 'Prenume', 'Gen', 'Media', 'Profil', 'An_Studiu', 'CNP', 'Nr_Telefon', 'Email'))
tree.place(relx=0.060, rely=0.050, relheight=0.050, relwidth=1)
tree.heading('#0', text='ID')
tree.heading('#1', text='Nume')
tree.heading('#2', text='Prenume')
tree.heading('#3', text='Gen')
tree.heading('#4', text='Media')
tree.heading('#5', text='Profil')
tree.heading('#6', text='An_Studiu')
tree.heading('#7', text='CNP')
tree.heading('#8', text='Nr_Telefon')
tree.heading('#9', text='Email')
tree.column('#0', width=30, anchor='center')
tree.column('#1', width=150, anchor='center')
tree.column('#2', width=250, anchor='center')
tree.column('#3', width=90, anchor='center')
tree.column('#4', width=90, anchor='center')
tree.column('#5', width=90, anchor='center')
tree.column('#6', width=90, anchor='center')
tree.column('#7', width=120, anchor='center')
tree.column('#8', width=229, anchor='center')
tree.column('#9', width=229, anchor='center')
tree.pack()



tree2 = ttk.Treeview(displayJos, columns=('ID', ' Nume', 'Prenume', 'Gen', 'Media', 'Profil', 'An_Studiu', 'CNP', 'Nr_Telefon', 'Email'))
tree2.place(relx=0.020, rely=0.600, relheight=0.300, relwidth=0.960)
tree2.heading('#0', text='ID')
tree2.heading('#1', text='Nume')
tree2.heading('#2', text='Prenume')
tree2.heading('#3', text='Gen')
tree2.heading('#4', text='Media')
tree2.heading('#5', text='Profil')
tree2.heading('#6', text='An_Studiu')
tree2.heading('#7', text='CNP')
tree2.heading('#8', text='Nr_Telefon')
tree2.heading('#9', text='Email')
tree2.column('#0', width=30, anchor='center')
tree2.column('#1', width=150, anchor='center')
tree2.column('#2', width=250, anchor='center')
tree2.column('#3', width=90, anchor='center')
tree2.column('#4', width=90, anchor='center')
tree2.column('#5', width=90, anchor='center')
tree2.column('#6', width=90, anchor='center')
tree2.column('#7', width=120, anchor='center')
tree2.column('#8', width=229, anchor='center')
tree2.column('#9', width=229, anchor='center')
tree2.pack()

refresh()







root.mainloop() 





