from tkinter import *
import sqlite3
import sys
import os

root = Tk()
root.title("Multivendor WLAN: Rogue AP Detection System")
width = 400
height = 280
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

#==============================VARIABLES======================================
USERNAME = StringVar()
PASSWORD = StringVar()
MACADDRESS = StringVar()
SSID = StringVar()
ENCRYPTION = StringVar()
 
#==============================FRAMES=========================================
Top = Frame(root, bd=2,  relief=RIDGE)
Top.pack(side=TOP, fill=X)
Form = Frame(root, height=200)
Form.pack(side=TOP, pady=20)
 
#==============================LABELS=========================================
lbl_title = Label(Top, text = "Authentication Required", font=('arial', 15))
lbl_title.pack(fill=X)
lbl_username = Label(Form, text = "Username:", font=('arial', 14), bd=15)
lbl_username.grid(row=0, sticky="e")
lbl_password = Label(Form, text = "Password:", font=('arial', 14), bd=15)
lbl_password.grid(row=1, sticky="e")
lbl_text = Label(Form)
lbl_text.grid(row=2, columnspan=2)
 
#==============================LOGIN ENTRY WIDGETS==================================
username = Entry(Form, textvariable=USERNAME, font=(14))
username.grid(row=0, column=1)
password = Entry(Form, textvariable=PASSWORD, show="*", font=(14))
password.grid(row=1, column=1)
 
def Login(event=None):
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `login` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            HomeWindow()
            USERNAME.set("")
            PASSWORD.set("")
            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")   
    cursor.close()
    conn.close()
#==============================LOGIN BUTTON WIDGETS=================================
btn_login = Button(Form, text="Login", width=45, command=Login)
btn_login.grid(pady=25, row=3, columnspan=2)
btn_login.bind('<Return>', Login)

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
    if cursor.fetchone()is None:
        cursor.execute("INSERT INTO `login` (username, password) VALUES('admin', 'admin')")
        conn.commit()

def HomeWindow():
    Database()
    global Home
    root.withdraw()
    viewap()

def viewap(event=None):
    root.destroy()
    os.system('viewandsearch.pyw')
    
def viewrogues(event=None):
    root.destroy()
    os.system('viewrogues.py')

def viewwaiting(event=None):
    root.destroy()
    os.system('viewwaiting.pyw')    

def Back():
    Home.destroy()
    root.deiconify()
    
def Addap(event=None):
    root.destroy()
    os.system('addap.pyw')
 
    #==============================INITIALIATION==================================
if __name__ == '__main__':
    root.iconbitmap('rogueap.ico')
    root.mainloop()
