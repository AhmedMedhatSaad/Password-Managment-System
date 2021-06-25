import sys
import tkinter as tk
from tkinter.constants import N
import webbrowser
from tkinter.messagebox import showinfo
from tkinter import Text, messagebox
from tkinter import ttk
import search
import db


def OpenURL(self):
    print("Open Url : " + self)
    webbrowser.open_new(self)


def FindInList(find, lst):
    lstIndex = []
    for i in range(0, len(lst)):
        if find == lst[i]:
            lstIndex.append(i)
    return lstIndex


lastClickX = 0
lastClickY = 0
arg = list(sys.argv)

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.geometry("1500x700+20+60")
        self.master.title("PassLock")
        self.master.iconbitmap("images\icon.ico")
        # self.master.state('zoomed')
        # -------------------------------
        self.close_button = tk.Button()
        self.expand_button = tk.Button()
        self.minimize_button = tk.Button()
        self.title_bar_title = tk.Label()
        # self.window = tk.Canvas(self.master)

        # self.TitleBar()
        self.frame_left_color = "gray12"
        self.frame_right_color = "gray12"
        self.canvas_right_table_color = "gray70"
        self.font_color = 'thistle1'
        self.master.configure(bg=self.canvas_right_table_color)
        # self.master.state('zoomed')
        # ------------------------Application private variable

        # ---------------------------frame left
        self.frame_left = tk.Frame(self.master)
        # ---------------------------frame right
        self.frame_right = tk.Frame(self.master)
        # ---------------------------Canvas right table
        self.right_table_frame = tk.Frame(
            self.frame_right, bg=self.canvas_right_table_color)
        self.frame_left.pack(side="left", fill='both', anchor='c')
        self.frame_right.pack(side="left", expand='true',
                              fill='both', anchor='c')
        self.right_table_frame.pack(
            side="top", fill='both', anchor='c', expand='true')

        # database 1
        self.folder_lst = []
        self.folder_lst_tkinter = []
        self.folder_lst_wid = []
        self.folder_name = tk.StringVar()
        self.folder_bg_color = []
        # database 2
        self.account_lst = []
        self.account_lst_wid = []
        self.account_bg_color = []
        # ---------------------------Table Scrollbar
        # main Frame
        self.table_main_frame = tk.Frame(
            self.right_table_frame)
        # Canvas for the scrollbar
        self.table_canvas = None
        # add scrollbar Y to canvas
        self.scrollbarY = None
        # add scrollbar X to canvas
        self.scrollbarX = None
        # the new frame
        self.table_frame = None
        # configure the canvas
        self.add_btn = None
        self.HomePage()
        self.FolderTableRefresh()
        

        

    # GUI All the Application
    # ------------------------------------------------------------------------
    def TitleBar(self):
        """
        Create Titlebar
        """
        lgray = '#545454'
        dgray = '#242424'
        rgray = '#2e2e2e'
        self.master.overrideredirect(True)
        title_bar = tk.Frame(self.master, bg='#2e2e2e', relief='raised',
                             bd=0, highlightthickness=0, pady=4, padx=4)

        def save_last_click_pos(event):
            global lastClickX, lastClickY
            lastClickX = event.x
            lastClickY = event.y

        def dragging(event):
            x, y = event.x - lastClickX + self.master.winfo_x(), event.y - lastClickY + \
                self.master.winfo_y()
            self.master.geometry("+%s+%s" % (x, y))

        title_bar.bind('<B1-Motion>', dragging)

        title_bar.bind('<Button-1>', save_last_click_pos)

        def change_x_on_hovering(event):
            self.close_button['bg'] = 'red'

        def return_x_to_normalstate(event):
            self.close_button['bg'] = rgray

        def change_size_on_hovering(event):
            self.expand_button['bg'] = lgray

        def return_size_on_hovering(event):
            self.expand_button['bg'] = rgray

        def change_m_size_on_hovering(event):
            self.minimize_button['bg'] = lgray

        def return_m_size_on_hovering(event):
            self.minimize_button['bg'] = rgray

        def minimize_window():
            self.master.withdraw()
            self.master.overrideredirect(False)
            self.master.iconify()

        def check_map(event):  # apply override on deiconify.
            if str(event) == "<Map event>":
                self.master.overrideredirect(1)

        def restore_down():
            if self.master.state() == 'normal':
                self.master.state('zoomed')
            else:
                self.master.state('normal')
                self.master.geometry("1500x700+20+60")

        # put a close button on the title bar
        self.close_button = tk.Button(title_bar, text='  X  ', command=self.master.destroy, bg=rgray, padx=2, pady=2,
                                      font=("calibri", 10), bd=0, fg='white', highlightthickness=0)
        self.expand_button = tk.Button(title_bar, text=' ■ ', bg=rgray, padx=2, pady=2, bd=0, fg='white',
                                       font=("calibri", 10), command=restore_down,
                                       highlightthickness=0)
        self.minimize_button = tk.Button(title_bar, text=' ─ ', bg=rgray, padx=2, pady=2, bd=0, fg='white',
                                         font=("calibri", 10), highlightthickness=0, command=minimize_window)
        self.title_bar_title = tk.Label(title_bar, text='PassLock', bg=rgray, bd=0, fg='white',
                                        font=("helvetica", 10), padx=21, pady=2,
                                        highlightthickness=0)
        # a canvas for the main area of the window
        self.window.config(bg='black', highlightthickness=0)
        # pack the widgets
        title_bar.pack(fill='x')
        self.close_button.pack(side='right')
        self.expand_button.pack(side='right')
        self.minimize_button.pack(side='right')
        self.title_bar_title.pack(side='left', padx=20)
        self.window.pack(expand=1, fill='both')

        # Animation
        self.close_button.bind('<Enter>', change_x_on_hovering)
        self.close_button.bind('<Leave>', return_x_to_normalstate)
        self.expand_button.bind('<Enter>', change_size_on_hovering)
        self.expand_button.bind('<Leave>', return_size_on_hovering)
        self.minimize_button.bind('<Enter>', change_m_size_on_hovering)
        self.minimize_button.bind('<Leave>', return_m_size_on_hovering)
        # check_map
        # added bindings to pass windows status to function
        self.master.bind('<Map>', check_map)
        self.master.bind('<Unmap>', check_map)

    def HomePage(self):
        """
        Start the Application with new Variable
        """
        about_url = "https://github.com/Ahmed-nd/PassLock#developers"

        self.frame_left.config(bg=self.frame_left_color, relief="groove", borderwidth=2, padx=30,
                               pady=30)
        self.frame_left.pack(side="left", fill='both', anchor='c')
        # ---------------------------frame right
        self.frame_right.config(bg=self.frame_right_color,
                                relief="groove", borderwidth=2, pady=30)
        self.frame_right.pack(side="left", expand='true',
                              fill='both', anchor='c')
        # ---------------------------Canvas right table
        self.right_table_frame.config(bg=self.canvas_right_table_color, relief="ridge",
                                      borderwidth=2)
        self.right_table_frame.pack(
            side="top", fill='both', anchor='c', padx=30, expand='true')

        # ------------------------------left
        btn_enter = tk.Button(self.frame_left, text="All Folders", font="Arial 10 bold", border=0,
                              bg=self.frame_left_color, activebackground=self.frame_left_color,
                              command=self.FolderTableRefresh, fg=self.font_color)
        btn_enter.pack(pady=10)
        btn_enter = tk.Button(self.frame_left, text="Generate\nPassword", font="Arial 10 bold", border=0,
                              bg=self.frame_left_color, activebackground=self.frame_left_color,
                              command=self.GeneratePasswordPage, fg=self.font_color)
        btn_enter.pack(pady=10)
        btn_enter = tk.Button(self.frame_left, text="BackUp", font="Arial 10 bold", border=0, command=self.BackUp,
                              bg=self.frame_left_color, activebackground=self.frame_left_color, fg=self.font_color)
        btn_enter.pack(pady=10)
        btn_enter = tk.Button(self.frame_left, text="About", command=lambda link=about_url: OpenURL(link), font="Arial 10 bold", border=0, fg=self.font_color,
                              bg=self.frame_left_color, activebackground=self.frame_left_color)
        btn_enter.pack(pady=10)
        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        self.folder_lst = [('Folder name', 'View', 'Edit', 'Del')]
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$--database from table 2--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        self.folder_lst_tkinter = None
        self.folder_lst_wid = [30, 10, 10, 10]
        self.folder_name = None
        self.folder_bg_color = ['light cyan',
                                'royal blue', 'lawn green', 'firebrick1']
        # Vaiables for account
        self.account_lst = None
        self.account_fold_name = None
        self.account_lst_wid = [15, 20, 15, 15, 10, 20, 10]
        self.account_web = None
        self.account_url = None
        self.account_username = None
        self.account_password = None
        self.account_bg_color = ['light cyan', 'light cyan', 'light cyan',
                                 'light cyan', 'royal blue', 'lawn green', 'firebrick1']
        # add btn
        self.add_btn = tk.Button(self.table_frame, text="+", font="Arial 12 bold", border=2, width=2,
                                 relief='groove', bg="lawn green", activebackground='green2',
                                 command=self.InsertFolder, fg=self.font_color)

    def TableReset(self):
        """ Reset the Home Table"""
        self.table_main_frame.destroy()
        # main Frame
        self.table_main_frame = tk.Frame(
            self.right_table_frame, bg=self.canvas_right_table_color)
        self.table_main_frame.pack(fill="both", expand='true',)
        # Canvas for the scrollbar
        self.table_canvas = tk.Canvas(
            self.table_main_frame, bg=self.canvas_right_table_color)
        self.table_canvas.grid(row=0, column=0, sticky="nsew")

        # add scrollbar Y to canvas
        self.scrollbarY = ttk.Scrollbar(
            self.table_main_frame, orient='vertical', command=self.table_canvas.yview)
        self.scrollbarY.grid(row=0, column=1, sticky="ns")
        # add scrollbar X to canvas
        self.scrollbarX = ttk.Scrollbar(
            self.table_main_frame, orient='horizontal', command=self.table_canvas.xview)
        self.scrollbarX.grid(row=1, column=0, sticky="ew")
        # configure the canvas
        self.table_canvas.configure(
            yscrollcommand=self.scrollbarY.set, xscrollcommand=self.scrollbarX.set)
        self.table_canvas.bind('<Configure>', lambda e: self.table_canvas.configure(
            scrollregion=self.table_canvas.bbox("all")))
        self.table_canvas.bind_all('<MouseWheel>', lambda e: self.table_canvas.yview_scroll(
            int(-1*(e.delta/120)), "units"))
        self.table_main_frame.grid_rowconfigure(0, weight=1000)
        self.table_main_frame.grid_columnconfigure(0, weight=1000)
        # the new frame
        self.table_frame = tk.Frame(
            self.table_canvas, bg=self.canvas_right_table_color)
        # display the table frame in the window canvas
        self.table_canvas.create_window((0, 0), window=self.table_frame)

    # GUI Folder table
    # ------------------------------------------------------------------------

    def FolderTablePage(self):
        """
        show all the Folders in database
        """
        def Find(search):
            print('search:' + search)
            names_folderlst = [element[0].lower()
                               for element in self.folder_lst]
            if search.lower() in names_folderlst:
                search_indexs = FindInList(search.lower(), names_folderlst)
                curr_index = search_indexs[0]
                top = tk.Toplevel()
                top.title(
                    f"PassLock || The Folder Number is {curr_index + 1} ")
                top.iconbitmap("images\icon.ico")
                top.resizable(0, 0)
                top.geometry("+100+150")
                top_frame = tk.Frame(top, padx=20, pady=20,
                                     bg=self.canvas_right_table_color)
                top_frame.pack()
                print(curr_index)

                def add():
                    print("add")
                    folder_name = self.folder_name.get()
                    names_folderlst = [element[0] for element in self.folder_lst if element[0] == folder_name]
                    print(names_folderlst)
                    if folder_name != '' and len(names_folderlst) == 0:
                        oldFolderName = self.folder_lst[curr_index][0]
                        db.UpdateFolderName(f"'{arg[1]}'",f"'{oldFolderName}'",f"'{folder_name}'")
                        # store Note in the database
                        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
                        top.destroy()
                        self.FolderTableRefresh()

                    else:
                        messagebox.showerror(
                            "PassLock", "Please Enter the data")

                def visit_fun():
                    top.destroy()
                    self.FolderTableTools(curr_index, 1)

                def delete_fun():
                    top.destroy()
                    self.FolderTableTools(curr_index, 3)

                # Data Frame Entry
                entry_frame = tk.Frame(
                    top_frame, padx=20, pady=20, bg=self.canvas_right_table_color)
                entry_frame.pack()

                folder_name_label = tk.Label(
                    entry_frame, text="Name:", font="Arial 14 bold", bg=self.canvas_right_table_color)
                folder_name_label.grid(row=0, column=0, pady=2)

                folder_name_entry = tk.Entry(entry_frame, width=30,
                                             font="Arial 12 bold", relief='raised',
                                             textvariable=self.folder_name)
                self.folder_name.set(self.folder_lst[curr_index][0])
                folder_name_entry.grid(row=0, column=1, padx=20, pady=2)

                #  right side btn add/cancel
                btn_frame_right = tk.Frame(
                    top_frame, padx=20, pady=20, bg=self.canvas_right_table_color)
                btn_frame_right.pack(side="right")
                cancel_btn = tk.Button(btn_frame_right, text="Cancel", font="Arial 12 bold", border=2, width=15,
                                       bg="red", activebackground='red2',
                                       command=top.destroy, )

                cancel_btn.grid(row=0, column=0, pady=2)

                delete_btn = tk.Button(btn_frame_right, text=self.folder_lst[0][3], width=15,
                                       bg=self.folder_bg_color[3],
                                       font="Arial 12 bold", activebackground='antique white',
                                       command=delete_fun)
                delete_btn.grid(row=1, column=0, pady=2)

                # left side btn add/cancel
                btn_frame_left = tk.Frame(
                    top_frame, padx=20, pady=20, bg=self.canvas_right_table_color)
                btn_frame_left.pack(side="left")

                visit_btn = tk.Button(btn_frame_left, text=self.folder_lst[0][1], width=15,
                                      bg=self.folder_bg_color[1],
                                      font="Arial 12 bold", activebackground='antique white',
                                      command=visit_fun)
                visit_btn.grid(row=1, column=0, pady=2)

                edit_btn = tk.Button(btn_frame_left, text="Edit", font="Arial 12 bold", border=2, width=15,
                                     bg="lawn green", activebackground='green2',
                                     command=add, )
                edit_btn.grid(row=2, column=0, pady=2)
                if len(self.folder_lst) < 2:
                        delete_btn['state'] = 'disable'
            else:
                messagebox.showerror(
                    "PassLock || Search error", "Folder name not found")
        total_rows = len(self.folder_lst)
        total_columns = len(self.folder_lst[0])
        
        # floral white
        filename = tk.Label(self.table_frame, text="Folders:", width=10, bg=self.canvas_right_table_color,
                            font="Times 26 bold", )
        filename.grid(row=0, column=0, pady=25)
        # Search box
        search.SearchBox(self.table_frame, command=Find, placeholder="Type and press enter",
                         button_foreground=self.font_color,
                         entry_highlightthickness=0, entry_width=40).grid(row=0, column=3, columnspan=3)
        # menu
        lst_menu = ['Name', 'tools']
        lst_menu_wid = [30, 33]
        for i in range(2, len(lst_menu) + 2):
            e = tk.Label(self.table_frame, text=lst_menu[i - 2], width=lst_menu_wid[i - 2], fg=self.font_color,
                         font="Arial 12 bold", relief='groove', bg=self.frame_left_color, )
            e.grid(row=1, column=i, pady=2)
            if i == 3:
                e.grid(columnspan=3)
        del self.folder_lst_tkinter
        self.folder_lst_tkinter = []
        
        for i in range(2, total_rows + 2):
            temp_tk = []
            e = tk.Label(self.table_frame, text=(i - 1), width=5, bg=self.frame_left_color, fg=self.font_color,
                         font="Arial 12 bold", relief='groove', )
            e.grid(row=i, column=1, padx=2, pady=2, sticky='e')
            temp_tk.append(e)
            for j in range(2, total_columns + 2):
                if j == 2:
                    e = tk.Label(self.table_frame, text=self.folder_lst[i - 2][j - 2], width=self.folder_lst_wid[j - 2], bg=self.folder_bg_color[j - 2],
                                 font="Arial 12 bold", relief='groove', )
                else:
                    e = tk.Button(self.table_frame, text=self.folder_lst[i - 2][j - 2], width=self.folder_lst_wid[j - 2],
                                  bg=self.folder_bg_color[j - 2],
                                  font="Arial 12 bold", activebackground='antique white',
                                  command=lambda row=i - 2, column=j - 2: self.FolderTableTools(row, column))
                temp_tk.append(e)
                e.grid(row=i, column=j, padx=2, pady=2)

            temp_tk = tuple(temp_tk)
            # User can't delete folder if it's the only folder
            if total_rows == 1:
                temp_tk[4]['state'] = 'disable'
            self.folder_lst_tkinter.append(temp_tk)

        self.add_btn = tk.Button(self.table_frame, text="+", font="Arial 12 bold", border=2, width=2,
                                 relief='groove', bg="lawn green", activebackground='green2',
                                 command=self.InsertFolder, )
        self.add_btn.grid(row=total_rows+1, column=total_columns+3)

    def FolderTableRefresh(self):
        """
        refresh the folders with new frame (new data)
        """
       
        self.TableReset()
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$--database from table 1--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        folder_items = []
        
        FolderItemsRaw =db.FetchFolders(f"'{arg[1]}'")
        
        for i in range (len(FolderItemsRaw)):
            folder_items.append(FolderItemsRaw[i][0])

        folder_items = set(folder_items)
        print(folder_items)
        if len(folder_items) > 0: 
            self.folder_lst =[]
            self.folder_lst_tkinter = []
            self.folder_name = tk.StringVar()
            for i in folder_items:
                self.folder_lst.append((f'{i}', 'View', 'Edit', 'Del'))
            print(self.folder_lst)
        self.FolderTablePage()

    def FolderTableTools(self, row, column):
        """
                View folder content and Edit folder name and Delete Folder from database
                this function take the button that have been clicked (row, column) and
                from that it know witch folder and witch code that need to run.
        """
        print(row, column)
        if column == 3:
            db.RemoveFolderFromAppAccount(f"'{self.folder_lst[row][0]}'",f"'{arg[1]}'")
            self.FolderTableRefresh()
        elif column == 2:
            del self.folder_name
            self.folder_name = tk.StringVar()

            def add():
                print("add")
                name = self.folder_name.get()
                names_folderlst = [element[0] for element in self.folder_lst if element[0] != name]
                print(names_folderlst)
                if name != '' and name not in names_folderlst:
                    oldFolderName = self.folder_lst[row][0]
                    db.UpdateFolderName(f"'{arg[1]}'",f"'{oldFolderName}'",f"'{name}'")
                    self.FolderTableRefresh()
                else:
                    messagebox.showerror(
                        "PassLock || Adding error", "Enter folder name")
            self.add_btn.destroy()
            self.add_btn = tk.Button(self.table_frame, text="+", font="Arial 12 bold", border=2, width=2,
                                     relief='groove', bg="lawn green", activebackground='green2',
                                     command=add, )
            self.add_btn.grid(row=row + 2, column=6)
            folder_name_entry = tk.Entry(self.table_frame, width=self.folder_lst_wid[0] + 3,
                                         font="Arial 12 bold", relief='groove',
                                         textvariable=self.folder_name, )
            self.folder_name.set(self.folder_lst[row][0])
            folder_name_entry.grid(row=row + 2, column=2, padx=2, pady=2)

        elif column == 1:
            print("View")
            """
            get the folder's accounts database
            """
            self.account_lst = [('Website', 'www.website.com', 'username', 'password', 'Visit', 'View & Edit', 'Del')]
            self.account_fold_name = self.folder_lst[row][0]
            self.AccountTableRefresh()

    def InsertFolder(self):
        """
                add new folder to database
                take from the user the folder name and the user can't add more than 12 folder
                """
        print("Add folder")
        del self.folder_name
        self.folder_name = tk.StringVar()

        def add():
            print("add")
            
            folder_name = self.folder_name.get()
            Folders_data = [element[0] for element in self.folder_lst]
            if folder_name != '' and folder_name not in Folders_data:
                db.InsertIntoAppAccount("'Website'", "'www.website.com'", "'Username'", "'Password'","'Note'",f"'{folder_name}'",f"'{arg[1]}'")
                top.destroy()
            else:
                messagebox.showerror(
                    "PassLock || Adding error", "Error Invalid Folder Name")
            self.FolderTableRefresh()

        def cancel_fun():
            top.destroy()
            self.FolderTableRefresh()
        top = tk.Toplevel()
        top.title("PassLock || Adding new Folder")
        top.iconbitmap("images\icon.ico")
        top.resizable(0, 0)
        top.geometry("+100+150")
        top_frame = tk.Frame(top, padx=20, pady=20,
                             bg=self.canvas_right_table_color)
        top_frame.pack()

        # Data Frame Entry
        entry_frame = tk.Frame(top_frame, padx=20, pady=20,
                               bg=self.canvas_right_table_color)
        entry_frame.pack()

        folder_name_label = tk.Label(
            entry_frame, text="Name:", font="Arial 14 bold", bg=self.canvas_right_table_color)
        folder_name_label.grid(row=0, column=0, pady=2)

        folder_name_entry = tk.Entry(entry_frame, width=30,
                                     font="Arial 12 bold", relief='raised',
                                     textvariable=self.folder_name)
        folder_name_entry.grid(row=0, column=1, padx=20, pady=2)

        # rigth side btn add/cancel
        btn_frame_right = tk.Frame(
            top_frame, padx=20, pady=20, bg=self.canvas_right_table_color)
        btn_frame_right.pack()

        cancel_btn = tk.Button(btn_frame_right, text="Cancel", font="Arial 12 bold", border=2, width=15,
                               relief='groove', bg="red", activebackground='red2',
                               command=cancel_fun, )
        cancel_btn.grid(row=1, column=2, pady=2)

        add_btn = tk.Button(btn_frame_right, text="Add", font="Arial 12 bold", border=2, width=15,
                            relief='groove', bg="lawn green", activebackground='green2',
                            command=add, )
        add_btn.grid(row=2, column=2, pady=2)

    # GUI account table
    # ------------------------------------------------------------------------

    def AccountTablePage(self):
        """
                show all the accounts in database folder
                """
        def Find(search):
            print('search:' + search)
            websites = [element[0].lower() for element in self.account_lst]
            if search.lower() in websites:
                search_indexs = FindInList(search.lower(), websites)
                global top, curr_index, account_text_entry
                curr_index = 0

                def add():
                    print("add")
                    global account_text_entry
                    web = self.account_web.get()
                    url = self.account_url.get()
                    username = self.account_username.get()
                    password = self.account_password.get()
                    Note = account_text_entry.get('1.0', tk.END)
                    print(Note)
                    if web != '' and username != '' and password != '' and url != '' and Note != '':
                        # store Note in the database
                        db.UpdateAppAccount(f"'{password}'",f"'{Note}'",f"'{web}'",f"'{username}'",f"'{self.account_fold_name}'",f"'{arg[1]}'")
                        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
                        top.destroy()
                        self.AccountTableRefresh()
                    else:
                        messagebox.showerror(
                            "PassLock || Search error", "Please Enter the data")

                def visit_fun():
                    self.AccountsTableTools(search_indexs[curr_index], 4)

                def delete_fun():
                    top.destroy()
                    self.AccountsTableTools(search_indexs[curr_index], 6)

                def next_fun():
                    global curr_index, top
                    curr_index = curr_index + 1
                    top.destroy()
                    top_page()

                def previous_fun():
                    global curr_index, top
                    curr_index = curr_index - 1
                    top.destroy()
                    top_page()

                def top_page():
                    global top, account_text_entry
                    top = tk.Toplevel()
                    top.title(
                        f"PassLock || The Account Number is {search_indexs[curr_index] + 1} ")
                    top.iconbitmap("images\icon.ico")
                    top.resizable(0, 0)
                    top.geometry("+100+150")
                    top_frame = tk.Frame(
                        top, padx=20, pady=20, bg=self.canvas_right_table_color)
                    top_frame.pack()
                    self.account_web = tk.StringVar()
                    self.account_url = tk.StringVar()
                    self.account_username = tk.StringVar()
                    self.account_password = tk.StringVar()

                    # next and previous Buttons
                    change_next_frame = tk.Frame(
                        top_frame, padx=20, pady=20, bg=self.canvas_right_table_color)
                    change_next_frame.pack(fill='x')
                    next_btn = tk.Button(change_next_frame, text="Next", font="Arial 12 bold", border=2, width=10,
                                         relief='groove', bg=self.frame_left_color,
                                         command=next_fun, fg=self.font_color)

                    next_btn.pack(side='right')
                    previous_btn = tk.Button(change_next_frame, text="Previous", font="Arial 12 bold", border=2, width=10,
                                             relief='groove', bg=self.frame_left_color,
                                             command=previous_fun, fg=self.font_color)

                    previous_btn.pack(side='left')
                    # Data Frame Entry
                    entry_frame = tk.Frame(
                        top_frame, padx=20, pady=20, bg=self.canvas_right_table_color)
                    entry_frame.pack()
                    account_web_label = tk.Label(entry_frame, text="       Website :  ", font="Arial 14 bold",
                                                 bg=self.canvas_right_table_color)
                    account_web_label.grid(row=0, column=0, pady=2)
                    account_web_entry = tk.Entry(entry_frame, width=30,
                                                 font="Arial 12 bold",
                                                 textvariable=self.account_web)
                    self.account_web.set(
                        self.account_lst[search_indexs[curr_index]][0])
                    account_web_entry.grid(row=0, column=1, pady=2)

                    account_url_label = tk.Label(entry_frame, text="              URL :  ", font="Arial 14 bold",
                                                 bg=self.canvas_right_table_color)
                    account_url_label.grid(row=1, column=0, pady=2)
                    account_url_entry = tk.Entry(entry_frame, width=30,
                                                 font="Arial 12 bold",
                                                 textvariable=self.account_url)
                    self.account_url.set(
                        self.account_lst[search_indexs[curr_index]][1])
                    account_url_entry.grid(row=1, column=1, pady=2)

                    account_username_label = tk.Label(entry_frame, text="   Username :  ", font="Arial 14 bold",
                                                      bg=self.canvas_right_table_color)
                    account_username_label.grid(row=2, column=0, pady=2)
                    account_username_entry = tk.Entry(entry_frame, width=30,
                                                      font="Arial 12 bold",
                                                      textvariable=self.account_username)
                    self.account_username.set(
                        self.account_lst[search_indexs[curr_index]][2])
                    account_username_entry.grid(row=2, column=1, pady=2)

                    account_password_label = tk.Label(entry_frame, text="   Password :  ", font="Arial 14 bold",
                                                      bg=self.canvas_right_table_color)
                    account_password_label.grid(row=3, column=0, pady=2)
                    account_password_entry = tk.Entry(entry_frame, width=30,
                                                      font="Arial 12 bold",
                                                      textvariable=self.account_password)
                    self.account_password.set(
                        self.account_lst[search_indexs[curr_index]][3])
                    account_password_entry.grid(row=3, column=1, pady=2)

                    account_text_label = tk.Label(entry_frame, text="            Note :  ", font="Arial 14 bold",
                                                  bg=self.canvas_right_table_color)
                    account_text_label.grid(row=4, column=0, pady=2)
                    account_text_entry = tk.Text(entry_frame, width=30, height=10,
                                                 font="Arial 12 bold", relief='raised')

                    AppName = self.account_lst[search_indexs[curr_index]][0]
                    UserName = self.account_lst[search_indexs[curr_index]][2]
                    NoteDB = db.FetchNote(AppName,UserName,self.account_fold_name,arg[1])
                    account_text_entry.insert(
                        '1.0', NoteDB)
                    account_text_entry.grid(row=4, column=1, pady=5)

                    # right side btn add/cancel
                    right_btn_frame = tk.Frame(
                        top_frame, padx=20, pady=20, bg=self.canvas_right_table_color)
                    right_btn_frame.pack(side='right')
                    cancel_btn = tk.Button(right_btn_frame, text="Cancel", font="Arial 12 bold", border=2, width=15,
                                           relief='groove', bg="red", activebackground='red2',
                                           command=top.destroy, )

                    cancel_btn.grid(row=0, column=0, pady=2)
                    delete_btn = tk.Button(right_btn_frame, text=self.account_lst[search_indexs[curr_index]][6], font="Arial 12 bold",
                                        border=2, width=15,
                                        bg=self.account_bg_color[6], activebackground='antique white',
                                        command=delete_fun, relief='groove')
                    delete_btn.grid(row=1, column=0, pady=2)
                    # left side btn add/cancel
                    left_btn_frame = tk.Frame(
                        top_frame, padx=20, pady=20, bg=self.canvas_right_table_color)
                    left_btn_frame.pack()
                    visit_btn = tk.Button(left_btn_frame, text=self.account_lst[search_indexs[curr_index]][4], font="Arial 12 bold", border=2, width=15,
                                          relief='groove', bg=self.account_bg_color[4], activebackground='antique white',
                                          command=visit_fun, )

                    visit_btn.grid(row=0, column=0, pady=2)
                    edit_btn = tk.Button(left_btn_frame, text="Save", font="Arial 12 bold", border=2, width=15,
                                         relief='groove', bg="lawn green", activebackground='green2',
                                         command=add, )
                    edit_btn.grid(row=1, column=0, pady=2)

                    if curr_index == 0:
                        previous_btn['state'] = 'disable'
                    else:
                        previous_btn['state'] = 'normal'
                    if curr_index == len(search_indexs) - 1:
                        next_btn['state'] = 'disable'
                    else:
                        next_btn['state'] = 'normal'
                    if len(self.account_lst) < 2:
                        delete_btn['state'] = 'disable'
                top_page()
            else:
                messagebox.showerror("PassLock", "Folder name not found")

        # folder name
        filename = tk.Label(self.table_frame, text=self.account_fold_name + ":", width=40, bg=self.canvas_right_table_color,
                            font="Times 26 bold", anchor='w')
        filename.grid(row=0, column=0, pady=25, columnspan=10, sticky='w')
        # search box
        search.SearchBox(self.table_frame, command=Find, placeholder="Type and press enter",
                         entry_highlightthickness=0, button_foreground=self.font_color, entry_width=40).grid(row=0, column=6, columnspan=3)
        lst_menu = ['Website', 'URL', 'Username', 'Password', 'Tools']
        lst_menu_wid = [15, 20, 15, 15, 44]
        for i in range(2, len(lst_menu) + 2):
            e = tk.Label(self.table_frame, text=lst_menu[i - 2], width=lst_menu_wid[i - 2],
                         font="Arial 12 bold", relief='groove', fg=self.font_color, bg=self.frame_left_color)
            e.grid(row=1, column=i, pady=2)
            if i == 6:
                e.grid(columnspan=4)
        del self.folder_lst_tkinter
        self.folder_lst_tkinter = []
        total_rows = len(self.account_lst)
        total_columns = len(self.account_lst[0])
        for i in range(2, total_rows + 2):
            temp_tk = []
            e = tk.Label(self.table_frame, text=(i - 1), width=5,
                         font="Arial 12 bold", relief='groove', fg=self.font_color, bg=self.frame_left_color)
            e.grid(row=i, column=1, padx=2, pady=2)
            temp_tk.append(e)
            for j in range(2, total_columns + 2):
                if j <= 5:
                    e = tk.Label(self.table_frame, text=self.account_lst[i - 2][j - 2], width=self.account_lst_wid[j - 2],
                                 bg=self.account_bg_color[j - 2], font="Arial 12 bold", relief='groove', )
                else:
                    e = tk.Button(self.table_frame, text=self.account_lst[i - 2][j - 2], width=self.account_lst_wid[j - 2],
                                  bg=self.account_bg_color[j -
                                                           2], font="Arial 12 bold",
                                  activebackground='antique white',
                                  command=lambda row=i - 2, column=j - 2: self.AccountsTableTools(row, column))
                temp_tk.append(e)
                e.grid(row=i, column=j, padx=2, pady=2)

            temp_tk = tuple(temp_tk)
            if total_rows == 1:
                temp_tk[7]['state'] = 'disable'
            self.folder_lst_tkinter.append(temp_tk)

            # self.e.insert(END, folder_lst[i][j])
        self.add_btn = tk.Button(self.table_frame, text="+", font="Arial 12 bold", border=2, width=2,
                                 relief='groove', bg="lawn green", activebackground='green2',
                                 command=self.InsertAccount)
        self.add_btn.grid(row=total_rows + 1, column=total_columns + 3)

    def AccountTableRefresh(self):
        """
        refresh the folders with new frame (new data)
        """
        self.TableReset()
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$--database from table 2--$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        account_items = db.FetchAccount(f"'{arg[1]}'",f"'{self.account_fold_name}'")
        print(account_items)
        if len(account_items) > 0: 
            self.account_lst =[]
            #self.folder_lst_tkinter = []
            for i in account_items:
                self.account_lst.append((f'{i[0]}',f'{i[1]}', f'{i[2]}',f'{i[3]}','View', 'Edit', 'Del'))
        self.AccountTablePage()

    def AccountsTableTools(self, row, column):
        """
            View folder content and Edit folder name and Delete Folder from database
            this function take the button that have been clicked (row, column) and
            from that it know witch folder and witch code that need to run.
                """
        print(row, column)
        if column == 6:
            # delete record
            web=self.account_lst[row][0]
            username=self.account_lst[row][2]
            db.RemoveAppFromAppAccount(f"'{web}'",f"'{username}'",f"'{self.account_fold_name}'",f"'{arg[1]}'")
            
            self.AccountTableRefresh()
        elif column == 5:
            # Edit record
            # Create Top level
            # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
            top = tk.Toplevel()
            top.title(
                f"PassLock || Viewing and editing account number {row + 1}")
            top.iconbitmap("images\icon.ico")
            top.resizable(0, 0)
            top.geometry("+100+150")

            top_frame = tk.Frame(top, padx=20, pady=20,
                                 bg=self.canvas_right_table_color)
            top_frame.pack()
            self.account_web = tk.StringVar()
            self.account_url = tk.StringVar()
            self.account_username = tk.StringVar()
            self.account_password = tk.StringVar()

            def add():
                print("add")
                web = self.account_web.get()
                url = self.account_url.get()
                username = self.account_username.get()
                password = self.account_password.get()
                Note = account_text_entry.get('1.0', tk.END)
                print(Note)
                if web != '' and username != '' and password != '' and url != '':
                    
                    # store Note in the 
                    
                    db.UpdateAppAccount(f"'{password}'",f"'{Note}'",f"'{web}'",f"'{username}'",f"'{self.account_fold_name}'",f"'{arg[1]}'")
                    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
                    top.destroy()
                  
                    self.AccountTableRefresh()
                else:
                    messagebox.showerror(
                        "PassLock || Viewing and editing account error", "Please Enter the data")
            
            # Data Frame Entry
            entry_frame = tk.Frame(
                top_frame, padx=20, pady=20, bg=self.canvas_right_table_color)
            entry_frame.pack()
            account_web_label = tk.Label(entry_frame, text="       Website :  ", font="Arial 14 bold",
                                         bg=self.canvas_right_table_color)
            account_web_label.grid(row=0, column=0, pady=2)
            account_web_entry = tk.Entry(entry_frame, width=30,
                                         font="Arial 12 bold",
                                         textvariable=self.account_web)
            self.account_web.set(self.account_lst[row][0])
            account_web_entry.grid(row=0, column=1, pady=2)

            account_url_label = tk.Label(entry_frame, text="              URL :  ", font="Arial 14 bold",
                                         bg=self.canvas_right_table_color)
            account_url_label.grid(row=1, column=0, pady=2)
            account_url_entry = tk.Entry(entry_frame, width=30,
                                         font="Arial 12 bold",
                                         textvariable=self.account_url)
            self.account_url.set(self.account_lst[row][1])
            account_url_entry.grid(row=1, column=1, pady=2)

            account_username_label = tk.Label(entry_frame, text="   Username :  ", font="Arial 14 bold",
                                              bg=self.canvas_right_table_color)
            account_username_label.grid(row=2, column=0, pady=2)
            account_username_entry = tk.Entry(entry_frame, width=30,
                                              font="Arial 12 bold",
                                              textvariable=self.account_username)
            self.account_username.set(self.account_lst[row][2])
            account_username_entry.grid(row=2, column=1, pady=2)

            account_password_label = tk.Label(entry_frame, text="   Password :  ", font="Arial 14 bold",
                                              bg=self.canvas_right_table_color)
            account_password_label.grid(row=3, column=0, pady=2)
            account_password_entry = tk.Entry(entry_frame, width=30,
                                              font="Arial 12 bold",
                                              textvariable=self.account_password)
            self.account_password.set(self.account_lst[row][3])
            account_password_entry.grid(row=3, column=1, pady=2)

            account_text_label = tk.Label(entry_frame, text="             Note :  ", font="Arial 14 bold",
                                          bg=self.canvas_right_table_color)
            account_text_label.grid(row=4, column=0, pady=2)
            account_text_entry = tk.Text(entry_frame, width=30, height=10,
                                         font="Arial 12 bold", relief='raised')


            AppName = self.account_lst[row][0]
            UserName = self.account_lst[row][2]
            NoteDB = db.FetchNote(AppName,UserName,self.account_fold_name,arg[1])
            account_text_entry.insert('1.0', NoteDB)
            account_text_entry.grid(row=4, column=1, pady=5)
            #  btn add/cancel
            btn_frame = tk.Frame(top_frame, padx=20, pady=20,
                                 bg=self.canvas_right_table_color)
            btn_frame.pack()
            self.add_btn = tk.Button(btn_frame, text="Cancel", font="Arial 12 bold", border=2, width=15,
                                     relief='groove', bg="red", activebackground='red2',
                                     command=top.destroy, )

            self.add_btn.grid(row=5, column=0, pady=2)
            self.add_btn = tk.Button(btn_frame, text="Add", font="Arial 12 bold", border=2, width=15,
                                     relief='groove', bg="lawn green", activebackground='green2',
                                     command=add, )
            self.add_btn.grid(row=6, column=0, pady=2)

        elif column == 4:
            # visit record link
            OpenURL(self.account_lst[row][1])

    def InsertAccount(self):
        """
        insert account in the folder
        """
        print("Add folder")
        del self.account_web
        del self.account_url
        del self.account_username
        del self.account_password

        def add():
            print("add")
            web = self.account_web.get()
            url = self.account_url.get()
            username = self.account_username.get()
            password = self.account_password.get()
            Note = account_text_entry.get('1.0', tk.END)
            print(Note)
            if web != '' and username != '' and password != '' and url != '':
                db.InsertIntoAppAccount(f"'{web}'",f"'{url}'",f"'{username}'",f"'{password}'",f"'{Note}'",f"'{self.account_fold_name}'",f"'{arg[1]}'")
                top.destroy()
            else:
                messagebox.showerror(
                    "PassLock || Adding error", "Please Enter the data")
            self.AccountTableRefresh()

        def cancel_fun():
            top.destroy()
            self.AccountTableRefresh()

        top = tk.Toplevel()
        top.title("PassLock || Adding new account")
        top.iconbitmap("images\icon.ico")
        top.resizable(0, 0)
        top.geometry("+100+150")
        top_frame = tk.Frame(top, padx=20, pady=20,
                             bg=self.canvas_right_table_color)
        top_frame.pack()
        self.account_web = tk.StringVar()
        self.account_url = tk.StringVar()
        self.account_username = tk.StringVar()
        self.account_password = tk.StringVar()

        # Data Frame Entry
        entry_frame = tk.Frame(top_frame, padx=20, pady=20,
                               bg=self.canvas_right_table_color)
        entry_frame.pack()

        account_web_label = tk.Label(entry_frame, text="           Website :", font="Arial 14 bold",
                                     bg=self.canvas_right_table_color)
        account_web_label.grid(row=0, column=0, pady=2)
        account_web_entry = tk.Entry(entry_frame, width=30,
                                     font="Arial 12 bold", relief='raised',
                                     textvariable=self.account_web)
        account_web_entry.grid(row=0, column=1, pady=2)

        account_url_label = tk.Label(entry_frame, text="                  URL :", font="Arial 14 bold",
                                     bg=self.canvas_right_table_color)
        account_url_label.grid(row=1, column=0, pady=2)
        account_url_entry = tk.Entry(entry_frame, width=30,
                                     font="Arial 12 bold", relief='raised',
                                     textvariable=self.account_url)
        account_url_entry.grid(row=1, column=1, padx=20, pady=2)

        account_username_label = tk.Label(entry_frame, text="       Username :", font="Arial 14 bold",
                                          bg=self.canvas_right_table_color)
        account_username_label.grid(row=2, column=0, pady=2)
        account_username_entry = tk.Entry(entry_frame, width=30,
                                          font="Arial 12 bold", relief='raised',
                                          textvariable=self.account_username)
        account_username_entry.grid(row=2, column=1, padx=20, pady=2)

        account_password_label = tk.Label(entry_frame, text="       Password :", font="Arial 14 bold",
                                          bg=self.canvas_right_table_color)
        account_password_label.grid(row=3, column=0, pady=2)
        account_password_entry = tk.Entry(entry_frame, width=30,
                                          font="Arial 12 bold", relief='raised',
                                          textvariable=self.account_password)
        account_password_entry.grid(row=3, column=1, padx=20, pady=2)

        account_text_label = tk.Label(
            entry_frame, text="               Note :", font="Arial 14 bold", bg=self.canvas_right_table_color)
        account_text_label.grid(row=4, column=0, pady=2)
        account_text_entry = tk.Text(entry_frame, width=30, height=10,
                                     font="Arial 12 bold", relief='raised')
        account_text_entry.grid(row=4, column=1, padx=20, pady=5)
        #  btn add/cancel
        btn_frame = tk.Frame(top_frame, padx=20, pady=20,
                             bg=self.canvas_right_table_color)
        btn_frame.pack()
        self.add_btn = tk.Button(btn_frame, text="Cancel", font="Arial 12 bold", border=2, width=15,
                                 relief='groove', bg="red", activebackground='red2',
                                 command=cancel_fun, )

        self.add_btn.grid(row=5, column=1, pady=2)
        self.add_btn = tk.Button(btn_frame, text="Add", font="Arial 12 bold", border=2, width=15,
                                 relief='groove', bg="lawn green", activebackground='green2',
                                 command=add, )
        self.add_btn.grid(row=6, column=1, pady=2)

    # GUI generate password
    # ------------------------------------------------------------------------

    def GeneratePasswordPage(self):

        import random
        import array
        strong_pass = tk.StringVar()
        current_value = tk.DoubleVar()

        def generate_password(max_len):
            # MAX_LEN
            # maximum length of password needed
            # this can be changed to suit your password length

            # declare arrays of the character that we need in out password
            # Represented as chars to enable easy string concatenation
            digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            lowercase_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                                    'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                                    'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                                    'z']

            uppercase_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                    'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                                    'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                                    'Z']

            symbols = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>', '*', '(', ')', '<', '+', '-', "'",
                       ".", ","]

            # combines all the character arrays above to form one array
            combined_list = digits + uppercase_characters + lowercase_characters + symbols

            # randomly select one character from each character set above
            rand_digit = random.choice(digits)
            rand_upper = random.choice(uppercase_characters)
            rand_lower = random.choice(lowercase_characters)
            rand_symbol = random.choice(symbols)

            # combine the character randomly selected above
            # at this stage, the password contains only 4 characters but
            # we want a 12-character password
            temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

            # now that we are sure we have at least one character from each
            # set of characters, we fill the rest of
            # the password length by selecting randomly from the combined
            # list of character above.
            for x in range(max_len - 4):
                temp_pass = temp_pass + random.choice(combined_list)

                # convert temporary password into array and shuffle to
                # prevent it from having a consistent pattern
                # where the beginning of the password is predictable
                temp_pass_list = array.array('u', temp_pass)
                random.shuffle(temp_pass_list)

            # traverse the temporary password array and append the chars
            # to form the password
            password = ""
            for x in temp_pass_list:
                password = password + x
            strong_pass.set(password)

            # triggered off left button click on text_field

        def copy_text_to_clipboard():
            field_value = strong_pass.get()
            self.master.clipboard_clear()  # clear clipboard contents
            # append new value to clipbaord
            self.master.clipboard_append(field_value)

        top = tk.Toplevel()
        top.title("PassLock || Generate Password")
        top.iconbitmap("images\icon.ico")
        top.resizable(0, 0)
        top.geometry("+100+150")

        top_frame = tk.Frame(top, padx=20, pady=20,
                             bg=self.canvas_right_table_color)
        top_frame.pack()
        # Frame 1 generate_frame
        generate_frame = tk.Frame(
            top_frame, bg=self.canvas_right_table_color)
        generate_frame.pack(pady=10)
        strong_pass_entry = tk.Entry(generate_frame, width=50,
                                     font="Arial 12 bold", relief='groove',
                                     textvariable=strong_pass)

        strong_pass_entry.pack(side='left')
        btn_generate = tk.Button(generate_frame, text="Generate", font="Arial 12 bold", border=2,
                                 relief='groove', bg="lawn green", activebackground='green2',
                                 command=lambda: generate_password(int(current_value.get())))
        btn_generate.pack(side='left')
        btn_copy = tk.Button(generate_frame, text="Copy", font="Arial 12 bold", border=2,
                             relief='groove', bg="light goldenrod", activebackground='gold',
                             command=copy_text_to_clipboard)
        btn_copy.pack(side='left')
        # Frame 2 pass_len_frame
        pass_len_frame = tk.Frame(
            top_frame, bg=self.canvas_right_table_color)
        pass_len_frame.pack()
        # scale Value
        current_value.set(5)
        scroll_num = tk.Scale(pass_len_frame, from_=5, to=45, orient='horizontal', length=310,
                              variable=current_value, bg=self.canvas_right_table_color)
        scroll_num.pack(side='left')

    # GUI BackUp
    # ------------------------------------------------------------------------

    def BackUp(self):
        from Backend import BackUp
        import time

        def increment(*args):
            global btn, process_state, accounts
            for i in range(100):
                if process_state:
                    p1["value"] = i+1
                    top_frame.update()
                    time.sleep(0.1)
                else:
                    break
            if process_state:
                self.folder_lst.append(
                    (f'Chrome{lastClickX}', 'View', 'Edit', 'Del'))
                self.account_lst.extend(accounts)

        def fetch_fun(_):
            global btn, process_state, accounts
            try:
                accounts = BackUp.FetchAccounts()
                btn['state'] = 'disabled'
            except:
                messagebox.showerror(
                    "PassLock || BackUp Error", "There is something wrong on the user Chrome installation")
                process_state = 0
        top = tk.Toplevel()
        top.title("PassLock || BackUp")
        top.iconbitmap("images\icon.ico")
        top.resizable(0, 0)
        top.geometry("+100+150")

        top_frame = tk.Frame(top, padx=20, pady=20,
                             bg=self.canvas_right_table_color)
        top_frame.pack()
        top_label = tk.Label(top_frame, text="BackUp only work if you have\n Chrome in your device", font="Arial 8 bold",
                             bg=self.canvas_right_table_color, fg='red')
        top_label.grid(row=3, column=0, columnspan=3, pady=30)
        p1 = ttk.Progressbar(top_frame, length=200, cursor='spider',
                             mode="determinate",
                             orient=tk.HORIZONTAL)
        p1.grid(row=1, column=1)
        global btn, process_state
        process_state = 1
        btn = ttk.Button(top_frame, text="Start", command=increment)
        btn.grid(row=1, column=0)
        btn.bind('<Button-1>', fetch_fun)


if __name__ == "__main__":
    # Create Datebase
    # Create object
    form = tk.Tk()
    app = Application(form)
    # Adjust size
    form.mainloop()
