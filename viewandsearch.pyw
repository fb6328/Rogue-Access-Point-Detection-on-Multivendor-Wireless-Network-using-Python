from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import sys
import os

root = Tk()
root.title("Multivendor WLAN: Rogue AP Detection System")
width = 500
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

#=====================================METHODS==============================================
def Database():
    conn = sqlite3.connect("roguedetect.db")
    cursor = conn.cursor()     
    cursor.execute("SELECT * FROM `authorizedap` ORDER BY `ap_id` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    
def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("roguedetect.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `authorizedap` WHERE `ap_id` LIKE ? OR `mac_address` LIKE ? OR `ssid` LIKE ? OR `encryption` LIKE ?", ('%'+str(SEARCH.get())+'%', '%'+str(SEARCH.get())+'%', '%'+str(SEARCH.get())+'%', '%'+str(SEARCH.get())+'%'))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
def Reset():
    conn = sqlite3.connect("roguedetect.db")
    cursor = conn.cursor()
    tree.delete(*tree.get_children())
    cursor.execute("SELECT * FROM `authorizedap` ORDER BY `ap_id` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()
    
def addap(event=None):
    root.destroy()
    os.system('addap.pyw')

def viewrogues(event=None):
    root.destroy()
    os.system('viewrogues.py')

def viewwaiting(event=None):
    root.destroy()
    os.system('viewwaiting.pyw')
    
#=====================================VARIABLES============================================
SEARCH = StringVar()

#=====================================FRAME================================================
Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
TopFrame = Frame(root, width=500)
TopFrame.pack(side=TOP)
TopForm= Frame(TopFrame, width=300)
TopForm.pack(side=LEFT, pady=10)
TopMargin = Frame(TopFrame, width=260)
TopMargin.pack(side=LEFT)
MidFrame = Frame(root, width=500)
MidFrame.pack(side=TOP)

#=====================================LABEL WIDGET=========================================
lbl_title = Label(Top, width=500, font=('arial', 18), text="Authorized Access Points", bg="light green")
lbl_title.pack(side=TOP, fill=X)

#=====================================ENTRY WIDGET=========================================
search = Entry(TopForm, textvariable=SEARCH)
search.pack(side=LEFT)

#=====================================BUTTON WIDGET========================================
btn_search = Button(TopForm, text="Search", bg="#006dcc", command=Search)
btn_search.pack(side=LEFT)
btn_reset = Button(TopForm, text="Reset", command=Reset)
btn_reset.pack(side=LEFT)
btn_reset = Button(TopForm, text="+Add AP", command=addap)
btn_reset.pack(side=LEFT)
btn_reset = Button(TopForm, text="Rogues", command=viewrogues)
btn_reset.pack(side=LEFT)
btn_reset = Button(TopForm, text="Waiting", command=viewwaiting)
btn_reset.pack(side=LEFT)
#=====================================Table WIDGET=========================================
scrollbarx = Scrollbar(MidFrame, orient=HORIZONTAL)
scrollbary = Scrollbar(MidFrame, orient=VERTICAL)
tree = ttk.Treeview(MidFrame, columns=("ap_id", "mac_address", "ssid", "encryption"), selectmode="extended", height=400, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('ap_id', text="Count",anchor=W)
tree.heading('mac_address', text="MAC Address",anchor=W)
tree.heading('ssid', text="SSID",anchor=W)
tree.heading('encryption', text="Encryption",anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=50)
tree.column('#2', stretch=NO, minwidth=0, width=180)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=120)
tree.pack()

#=====================================INITIALIZATION=======================================
if __name__ == '__main__':
    Database()
    root.iconbitmap('rogueap.ico')
    root.mainloop()

