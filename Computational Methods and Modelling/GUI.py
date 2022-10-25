from tkinter import TK

root = TK()

root.title("FPUT User Interface")

screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()

gui_width = screen_width/2
gui_height = screen_height/2

root.geometry(f"{gui_width}x{gui_height}+{gui_width}+{gui_height}")

def my_callback():
    print("you clicked the button....")

entry =Entry(root)
entry.pack()
#print the contents of entry box in a console
def printMsg():
    print(entry.get())

msg_button=Button(root,text='click here',command=my_callback)
msg_button.pack()

entry_button=Button(root,text='print msg',command=printMsg)
entry_button.pack()

root.mainloop()