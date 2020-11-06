from tkinter import *
from tkinter import ttk

from ftp_handler import FTPHandler
from local_handler import LocalHandler

root = Tk()
root.title('FTP Communication program')
root.geometry('1000x500')

conn = None
local_conn = LocalHandler()

def create_connect_frame(parent):
    connect_frame = Frame(parent)
    connect_frame.pack(pady=20)

    # Labels
    ip_lbl = Label(connect_frame, text='IP Address')
    ip_lbl.grid(row=0, column=0)
    user_lbl = Label(connect_frame, text='User')
    user_lbl.grid(row=0, column=1)
    password_lbl = Label(connect_frame, text='Pass')
    password_lbl.grid(row=0, column=2)
    port_lbl = Label(connect_frame, text='Port')
    port_lbl.grid(row=0, column=3)
    connected_lbl = Label(connect_frame, text='Not connected')
    connected_lbl.grid(row=2, column=0)

    # Entries
    ip_box = Entry(connect_frame)
    ip_box.insert(END, '192.168.1.21')
    ip_box.grid(row=1, column=0)
    user_box = Entry(connect_frame)
    user_box.insert(END, 'buikhoi')
    user_box.grid(row=1, column=1)
    pass_box = Entry(connect_frame, show='*')
    pass_box.insert(END, '297586')
    pass_box.grid(row=1, column=2)
    port_box = Entry(connect_frame)
    port_box.insert(END, '2121')
    port_box.grid(row=1, column=3)

    def connect():
        global conn
        try:
            conn = FTPHandler(
                ip_box.get(),
                user_box.get(),
                pass_box.get()
            )
            connected_lbl.config(text='Connected')
            refresh_server_tree(server_tree, conn)
        except:
            connected_lbl.config(text='Wrong credentials')

    # Button
    connect_button = Button(connect_frame, text='Connect', command=connect)
    connect_button.grid(row = 1, column=4)
    return {
        'ip': ip_box,
        'user': user_box,
        'pass': pass_box,
        'port': port_box
    }

def create_tree_view(parent, grid_row, grid_col):
    tree_frame = Frame(parent)
    tree_frame.grid(row=grid_row, column=grid_col)

    tree_view = ttk.Treeview(tree_frame, selectmode='browse')
    tree_view.pack(side='left')

    tree_view['columns'] = ('Name', 'Size', 'Last modified')
    tree_view.column('#0', width=0, stretch=NO)
    tree_view.column('Name', anchor=W, width=200)
    tree_view.column('Size', anchor=E, width=50)
    tree_view.column('Last modified', anchor=E, width=100)

    tree_view.heading('#0', text='', anchor=W)
    tree_view.heading('Name', text='Name', anchor=W)
    tree_view.heading('Size', text='Size', anchor=E)
    tree_view.heading('Last modified', text='Last modified', anchor=E)

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_view.yview)
    vsb.pack(side='right', fill='y')

    tree_view.configure(yscrollcommand=vsb.set)

    return tree_view

def create_file_accessing(parent):
    file_access = Frame(parent)
    file_access.pack(pady=20)

    local_tree = create_tree_view(file_access, 0, 0)
    server_tree = create_tree_view(file_access, 0, 2)

    def onLocalDoubleClick(event):
        global local_conn, local_tree
        selection = local_tree.selection()[0]
        if selection == '0':
            local_conn.back_folder()
        else:
            fld_name = local_tree.item(selection)['values'][0]
            local_conn.open_folder(fld_name)
        refresh_local_tree(local_tree, local_conn)

    def onServerDoubleClick(event):
        global conn, server_tree
        selection = server_tree.selection()[0]
        fld_name = server_tree.item(selection)['values'][0]
        conn.open_folder(fld_name)
        refresh_server_tree(server_tree, conn)

    local_tree.bind('<Double-1>', onLocalDoubleClick)
    server_tree.bind('<Double-1>', onServerDoubleClick)

    loader_frame = Frame(file_access)
    loader_frame.grid(row=0, column=1)

    local_to_server_btn = Button(loader_frame, text='Upload to server', command=to_server)
    local_to_server_btn.grid(row=0, column=0)

    server_to_local_btn = Button(loader_frame, text='Download to local', command=to_local)
    server_to_local_btn.grid(row=1, column=0)

    return local_tree, server_tree

def refresh_local_tree(local_tree, local_handler):
    data = get_items(local_handler)
    fill_tree_data(local_tree, data)

def get_items(handler):
    items = handler.get_folder_items()
    all_items = []
    if not handler.check_root():
        all_items.append(['..', '', ''])
    for item in items:
        if item[0] == '.':
            continue
        all_items.append([item, '1024', '07-11-2020'])
    return all_items

def refresh_server_tree(server_tree, server_handler):
    data = get_items(server_handler)
    fill_tree_data(server_tree, data)

def clear_tree(tree):
    tree.delete(*tree.get_children())

def fill_tree_data(tree, data):
    clear_tree(tree)
    count = 0
    for record in data:
        tree.insert(parent='', index='end', iid=count, text='', values=record)
        count += 1

def to_server():
    global local_conn, conn, server_tree, local_tree
    selection = local_tree.selection()[0]
    file_path = local_conn.get_current_folder() + local_tree.item(selection)['values'][0]
    conn.upload_file(file_path)

    refresh_server_tree(server_tree, conn)

def to_local():
    global local_conn, conn, local_tree, server_tree
    selection = server_tree.selection()[0]
    file_name = server_tree.item(selection)['values'][0]
    conn.download_file(file_name, local_conn.get_current_folder())

    refresh_local_tree(local_tree, local_conn)

create_connect_frame(root)

local_tree, server_tree = create_file_accessing(root)

refresh_local_tree(local_tree, local_conn)

root.mainloop()