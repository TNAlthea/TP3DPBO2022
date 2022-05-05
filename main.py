from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from PIL import ImageTk, Image
import os
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_praktikum"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)
    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")
    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    # Input 3
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label4 = Label(dframe, text="Jurusan").grid(row=2, column=0, sticky="w")
    input4 = OptionMenu(dframe, input_jurusan, *options)
    input4.grid(row=2, column=1, padx=20, pady=10, sticky='w')
    #Input 4
    label5 = Label(dframe, text="Jenis Kelamin").grid(row=3, column=0, sticky="w")
    input_JK = StringVar(value = "Laki-laki")
    
    R1 = Radiobutton(dframe,text="Laki-laki",value = "Laki-laki", variable = input_JK).grid(row=3, column=1, padx = (20, 0), sticky=W)
    R2 = Radiobutton(dframe,text="Perempuan",value = "Perempuan", variable = input_JK).grid(row=3, column=1, padx = (100, 0), sticky=W)

    #Input 5
    label6 = Label(dframe, text="Hobi").grid(row=4, column=0, sticky="w")
    input_hobi = StringVar(value = "Bermain Game")
    ComboboxHobi = ttk.Combobox(dframe, values = ["Bermain Game", "Belajar sebentar lalu istirahat lama", "Rebahan", "Menyusun Teori Konspirasi"], textvariable=input_hobi, width=30).grid(row=4, column = 1, padx=20, sticky=W)
    
    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    check = 0
    
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[checkKosong(top, input_nama, input_nim, input_JK, input_jurusan, input_hobi), top.withdraw()])
    btn_submit.grid(row=5, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Gak jadi / Kembali", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=5, column=1, padx=10)


def checkKosong(parent, nama, nim, JK, jurusan, hobi):
    global root
    top = Toplevel()
    # cek kolom kosong hanya pada field nama dan nim karena field lain sudah mempunyai nilai default 
    if (len(nama.get()) and nim.get().isdigit()):
        insertData(parent, nama, nim, JK, jurusan, hobi)
        top.destroy()
    else: 
        messagebox.showinfo("Perhatian!", "Data masih ada yang kosong!/Tidak Valid!")
        top.destroy()
        root.deiconify()
        inputs()
        

# Untuk memasukan data
def insertData(parent, nama, nim, JK, jurusan, hobi):
    top = Toplevel()
    # Get data
    nama = nama.get()
    nim = nim.get()
    jurusan = jurusan.get()
    JK = JK.get()
    hobi = hobi.get()

    #insert SQL
    sql = "INSERT INTO mahasiswa (nim, nama, Jenis_Kelamin, jurusan, hobi) VALUES (%s, %s, %s, %s, %s)"
    val = (nim, nama, JK, jurusan, hobi)
    dbcursor.execute(sql, val)

    mydb.commit()
    
    # Input data di sini
    btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
    btn_ok.pack(padx=10, pady=10)
  
# Window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title6 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=5)
    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label5 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label6 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=5)
        i += 1



imgIdx = 0
currentIdx = 0
#menset path image
path = os.getcwd()
path = path + "/image"
#me-list nama file yang akan dibaca
imgName = os.listdir(path)
#memasukkan img dalam array
img = []
i = 0
for i in imgName:
    #membaca image + resizing
    img.append(ImageTk.PhotoImage(Image.open("image/" + i).resize((500, 500))))
    imgIdx+=1

def viewFacility():
    # Hide root window
    global root
    global imgIdx, img
    root.withdraw()
    
    #user control
    def nextBtn(label):
        global currentIdx
        currentIdx+=1
        if (currentIdx > imgIdx-1): currentIdx = 0
        label = Label(frame, image = img[currentIdx]).grid(row = 0, column = 1)

    def prevBtn(label):
        global currentIdx
        currentIdx-=1
        if (currentIdx < 0): currentIdx = imgIdx-1
        label = Label(frame, image = img[currentIdx]).grid(row = 0, column = 1)

    top = Toplevel()
    top.title("Fasilitas Kampus")
    frame = LabelFrame(top, borderwidth = 0)
    frame.pack()

    currentIdx = 0
    label = Label(frame, image = img[currentIdx]).grid(row = 0, column = 1, padx=5, pady=5)

    # Prev-Next Button
    btn_prev = Button(frame, text="Prev", anchor="s", command=lambda:[prevBtn(label)])
    btn_prev.grid(row=5, column=0, padx=10)

    btn_next = Button(frame, text="Next", anchor="s", command=lambda:[nextBtn(label)])
    btn_next.grid(row=5, column=2, padx=10)
    
    # Cancel Button
    btn_cancel = Button(frame, text="Cancel", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=5, column=1, padx=10)

    




# Dialog konfirmasi hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

def delAll():
    top = Toplevel()
    # Delete data disini
    dbcursor.execute("TRUNCATE TABLE mahasiswa")
    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(pady=20)

# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=2, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Semua Fasiltias Kampus", command=viewFacility, width=30)
b_clear.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()
