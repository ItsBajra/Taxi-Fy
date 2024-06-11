from tkinter import messagebox
from tkinter.messagebox import askyesno

import customtkinter as ctk
from PIL import Image

from .admin_dashboard import show_dashboard
from .backend import login_admin

# admin log in window
def admin_class(window, bg_label, second_frame):
    window_width = 1000
    window_height = 800

    # ----WINDOW APPEAR IN THE MIDDLE OF THE SCREEN----
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')
    window.configure(fg_color='#0a2135')

    # ---Mouse enter and leave actions---
    def on_enter_entry(event, widget):
        widget.configure(border_color='#fffc04')

    def on_leave_entry(event, widget):
        widget.configure(border_color='gray')

    def on_enter_back_button(event, widget):
        widget.configure(fg_color='#243a48')

    def on_leave_back_button(event, widget):
        widget.configure(fg_color='#333333')

    # ---QUIT BUTTON---
    def quit_fun():
        yes_no = askyesno('Confirmation', 'Do you really want to quit?')

        if yes_no:
            window.destroy()

    def show_password_login_fun():
        if show_password_login_var.get():
            password_login_entry.configure(show='')
        else:
            password_login_entry.configure(show='*')

    # ---Go back to previous screen---
    def back_to_main():
        welcome_label.place_forget()
        logo_label.place_forget()
        login_frame.place_forget()
        window_width = 800
        window_height = 800

        # ----WINDOW APPEAR IN THE MIDDLE OF THE SCREEN----
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        window.geometry(f'{window_width}x{window_height}+{x}+{y}')
        window.configure(fg_color='#0a2135')
        bg_label.place(relx=0.5, rely=0.45, anchor='center')
        second_frame.place(relx=0.5, rely=0.75, anchor='center')

    # ---Login Function---
    def login_function():
        account_info = login_admin(email=email_login_entry.get(), password=password_login_entry.get())
        if (account_info != None):
            welcome_label.place_forget()
            logo_label.place_forget()
            bg_label.place_forget()
            login_frame.place_forget()
            email_login_entry.delete(0, ctk.END)
            password_login_entry.delete(0, ctk.END)
            window_width = 1200
            window_height = 800

            # ----WINDOW APPEAR IN THE MIDDLE OF THE SCREEN----
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            window.geometry(f'{window_width}x{window_height}+{x}+{y}')
            show_dashboard(account_info, window, welcome_label, logo_label, login_frame)


        else:
            messagebox.showerror('Taxi-Fy says', 'Incorrect email or password!')

    # ----WIDGETS----
    # ----LOGO----
    welcome_picture = ctk.CTkImage(Image.open(r'Resources/welcome.png'), size=(150, 20))
    welcome_label = ctk.CTkLabel(window, width=150, height=20, image=welcome_picture, text='')
    welcome_label.place(relx=0.5, rely=0.03, anchor='center')

    logo_picture = ctk.CTkImage(Image.open(r'Resources/taxi-fy-trans.png'), size=(230, 110))
    logo_label = ctk.CTkLabel(window, width=230, height=110, image=logo_picture, text='')
    logo_label.place(relx=0.5, rely=0.13, anchor='center')


    login_frame = ctk.CTkFrame(window, border_width=0, width=700, height=610, corner_radius=40, fg_color='#19181A')
    login_frame.place(relx=0.5, rely=0.6, anchor='center')

    login_label = ctk.CTkLabel(login_frame, text='A D M I N    L O G I N')
    login_label.place(relx=0.5, rely=0.05, anchor='center')

    # -------------------LOGIN-----------------
    # email
    email_login_frame = ctk.CTkFrame(login_frame, width=300, height=55, border_width=2, border_color='gray',
                                     corner_radius=10)
    email_login_frame.place(relx=0.5, rely=0.2, anchor='center')
    email_login = ctk.CTkLabel(email_login_frame, text='Email', text_color='gray',
                               font=('Ariel', 12), height=10)
    email_login.place(relx=0.035, rely=0.2, anchor='w')

    # email entry
    email_login_entry = ctk.CTkEntry(email_login_frame, border_width=0, width=290, height=30,
                                     fg_color='#2b2b2b', font=('Verdana', 14))
    email_login_entry.place(relx=0.5, rely=0.6, anchor='center')
    email_login_entry.bind('<Enter>', lambda event: on_enter_entry(event, email_login_entry))
    email_login_entry.bind('<Leave>', lambda event: on_leave_entry(event, email_login_entry))

    # password
    password_login_frame = ctk.CTkFrame(login_frame, width=300, height=55, border_width=2,
                                        border_color='gray',
                                        corner_radius=10)
    password_login_frame.place(relx=0.5, rely=0.33, anchor='center')
    password_login = ctk.CTkLabel(password_login_frame, text='Password', text_color='gray',
                                  font=('Ariel', 12), height=10)
    password_login.place(relx=0.035, rely=0.2, anchor='w')

    # password entry
    password_login_entry = ctk.CTkEntry(password_login_frame, border_width=0, width=290, height=30,
                                        fg_color='#2b2b2b', font=('Verdana', 14), show='*')
    password_login_entry.place(relx=0.5, rely=0.6, anchor='center')
    password_login_entry.bind('<Enter>', lambda event: on_enter_entry(event, password_login_entry))
    password_login_entry.bind('<Leave>', lambda event: on_leave_entry(event, password_login_entry))

    # show password
    show_password_login_var = ctk.BooleanVar(value=False)
    show_password_login = ctk.CTkCheckBox(login_frame, text='Show password', command=show_password_login_fun,
                                          variable=show_password_login_var, font=('Ariel', 14), hover_color='#fffc04',
                                          corner_radius=20)
    show_password_login.place(relx=0.64, rely=0.44, anchor='center')

    # submit button
    submit_login = ctk.CTkButton(login_frame, text='Submit', font=('Ariel', 13),
                                 corner_radius=20, width=150, height=40, command=login_function)
    submit_login.place(relx=0.37, rely=0.57, anchor='center')

    # quit button
    quit_btn_login = ctk.CTkButton(login_frame, text='Quit', font=('Ariel', 13),
                                   corner_radius=20, width=150, height=40, command=quit_fun)
    quit_btn_login.place(relx=0.63, rely=0.57, anchor='center')

    # ---BACK BUTTON---
    back_button_picture = ctk.CTkImage(Image.open(r'Resources/back.png'), size=(15, 15))
    back_button_login = ctk.CTkButton(login_frame, text='', image=back_button_picture, text_color='WHITE',
                                      width=5, fg_color='#333333', corner_radius=40, height=10, command=back_to_main)
    back_button_login.place(relx=0.08, rely=0.13, anchor='center')
    back_button_login.bind('<Enter>', lambda event: on_enter_back_button(event, back_button_login))
    back_button_login.bind('<Leave>', lambda event: on_leave_back_button(event, back_button_login))

    window.mainloop()
