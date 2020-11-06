from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
root = Tk( )
def OpenFile():
    name = askopenfilename(
            initialdir='/home',
            filetypes =(('Text File', '*.txt'),('All Files','*.*')),
            title = 'Choose a file.'
        )
    print (name)
    try:
        with open(name,'r') as UseFile:
            print(UseFile.read())
 
    except:
        print('No files opened')
        Title = root.title('File Opener')
        label = ttk.Label(root, text ='File Open',foreground='red',font=('Helvetica', 16))
        label.pack()
 
menu = Menu(root)
 
root.config(menu=menu)
file = Menu(menu)
file.add_command(label = 'Open', command = OpenFile)
file.add_command(label = 'Exit', command = lambda:exit())
menu.add_cascade(label = 'File', menu = file)
 
root.mainloop()