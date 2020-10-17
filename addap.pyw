from tkinter import *
import sqlite3
import sys
import os

root = Tk()
root.title("Multivendor WLAN: Rogue AP Detection System")
width = 600
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

#==============================VARIABLES======================================
USERNAME = StringVar()
MACADDRESS = StringVar()
SSID = StringVar()
ENCRYPTION = StringVar()
 
#==============================FRAMES=========================================
Top = Frame(root, bd=2,  relief=RIDGE)
Top.pack(side=TOP, fill=X)
Form = Frame(root, height=400)
Form.pack(side=TOP, pady=20)
 
#==============================LABELS=========================================
lbl_title = Label(Top, text = "Add Access Point", font=('arial', 15))
lbl_title.pack(fill=X)
lbl_macaddress = Label(Form, text = "MAC Address:", font=('arial', 14), bd=15)
lbl_macaddress.grid(row=0, sticky="e")
lbl_ssid = Label(Form, text = "SSID:", font=('arial', 14), bd=15)
lbl_ssid.grid(row=1, sticky="e")
lbl_encryption = Label(Form, text = "Encryption Type:", font=('arial', 14), bd=15)
lbl_encryption.grid(row=2, sticky="e")
lbl_text = Label(Form)
lbl_text.grid(row=3, columnspan=2)
 
#==============================ADD AP ENTRY WIDGETS==================================
macaddress = Entry(Form, textvariable=MACADDRESS, font=(14))
macaddress.grid(row=0, column=1)
ssid = Entry(Form, textvariable=SSID, font=(14))
ssid.grid(row=1, column=1)
encryption = Entry(Form, textvariable=ENCRYPTION, font=(14))
encryption.grid(row=2, column=1)
 
def Addap(event=None):
    Database()
    if MACADDRESS.get() == "" or SSID.get() == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `authorizedap` WHERE `mac_address` = ?", (MACADDRESS.get(),))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO `authorizedap` (mac_address,ssid,encryption) VALUES(?,?,?)", (MACADDRESS.get(), SSID.get(), ENCRYPTION.get()))
            conn.commit()
            MACADDRESS.set("")
            SSID.set("")
            ENCRYPTION.set("")
            lbl_text.config(text="AP added successfuly", fg="green")
            #HomeWindow()
        else:
            lbl_text.config(text="This AP already exist. Add a different one", fg="red")
            MACADDRESS.set(MACADDRESS.get())
            SSID.set(SSID.get())
            ENCRYPTION.set(ENCRYPTION.get())
    cursor.close()
    conn.close()

def viewap(event=None):
    root.destroy()
    os.system('viewandsearch.pyw')
    
def viewrogues(event=None):
    root.destroy()
    os.system('viewrogues.py')

def viewwaiting(event=None):
    root.destroy()
    os.system('viewwaiting.pyw')

#==============================HOME WINDOW =========================================
def HomeWindow():
    Database()
   #==============================FRAMES=========================================
    Top2 = Frame(root, bd=2,  relief=RIDGE)
    Top2.pack(side=TOP, fill=X)
    Form2 = Frame(root, height=200)
    Form2.pack(side=TOP, pady=20)
    lbl_home = Label(Top2, text="Choose what to see ...", font=('times new roman', 14)).pack(side=LEFT)
    btn_back = Button(Form2, text='Authorized APs', command=viewap).pack(side=LEFT)
    btn_back = Button(Form2, text='Waiting APs', command=viewwaiting).pack(side=LEFT)
    btn_back = Button(Form2, text='See Rogue APs', command=viewrogues).pack(side=LEFT)
    btn_back = Button(Form2, text='Exit System', command=logoff).pack(side=LEFT)
    #btn_back = Button(Home, text='Close System', command=quit).pack(pady=20, fill=X)
    
#==============================ADD AP BUTTON WIDGETS=================================
btn_addap = Button(Form, text="+ ADD", width=45, command=Addap)
btn_addap.grid(pady=25, row=4, columnspan=2)
btn_addap.bind('<Return>', Addap)
btn_viewap = Button(Form, text="VIEW Access Points >", width=45, command=HomeWindow)
btn_viewap.grid(pady=25, row=5, columnspan=2)
btn_viewap.bind('<Return>', HomeWindow)


#==============================METHODS========================================
def Database():
    global conn, cursor
    conn = sqlite3.connect("roguedetect.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `user` (user_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, firstname TEXT, lastname TEXT, email TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `login` (login_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `authorizedap` (ap_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, mac_address TEXT UNIQUE, ssid TEXT, encryption TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `rogueap` (ap_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, mac_address TEXT UNIQUE, ssid TEXT, encryption TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `waitingap` (ap_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, mac_address TEXT UNIQUE, ssid TEXT, encryption TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `parameters` (param_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, param_type TEXT)")
    cursor.execute("SELECT * FROM `login` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `login` (username, password) VALUES('admin', 'admin')")
        conn.commit()  
def Back():
    Home.destroy()
    root.deiconify()
    
def logoff(event=None):
    root.destroy()
    
    #==============================INITIALIATION==================================
if __name__ == '__main__':
    root.iconbitmap('rogueap.ico')
    root.mainloop()
