from tkinter import messagebox
from tkinter.messagebox import askyesno

import customtkinter as ctk
from PIL import Image

from .backend import login_passenger, register_passenger
from .passenger_dashboard import show_dashboard

# passenger dashboard main function
def passenger_class(window, bg_label, second_frame):
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

    # ---Show password button function---
    def show_password_fun():
        if show_password_var.get():
            password_entry.configure(show='')
            repeat_password_entry.configure(show='')

        else:
            password_entry.configure(show='*')
            repeat_password_entry.configure(show='*')

    def show_password_login_fun():
        if show_password_login_var.get():
            password_login_entry.configure(show='')
        else:
            password_login_entry.configure(show='*')

    # ---Go back to previous screen---
    def back_to_main():
        welcome_label.place_forget()
        logo_label.place_forget()
        tabview.place_forget()
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
        account_info = login_passenger(email=email_login_entry.get(), password=password_login_entry.get())
        if (account_info != None):
            welcome_label.place_forget()
            logo_label.place_forget()
            bg_label.place_forget()
            tabview.place_forget()
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
            show_dashboard(account_info, window, welcome_label, logo_label, tabview)


        else:
            messagebox.showerror('Taxi-Fy says', 'Incorrect email or password!')

    # ---REGISTRATION FUNCTION---
    def registration_function():
        first_name = firstname_entry.get()
        last_name = lastname_entry.get()
        email_ = email_entry.get()
        gender_ = gender_value.get()
        age_value = int(age_slider_display.get())
        address_ = address_entry.get()
        phone_number = number_entry.get()
        payment_method_ = payment_method_cmbbox.get()
        password_ = password_entry.get()
        repeat_password_ = repeat_password_entry.get()

        # checking if all the information is filled
        if not all([first_name, last_name, email_, gender_, age_value, address_, phone_number, payment_method_,
                    password_]):
            messagebox.showwarning('Invalid!', 'Please fill out all the information!')
            return

        if '@' in email_ and '.com' in email_:  # validation rule for email
            if age_value > 16 and age_value < 100:  #valication rule for age
                if phone_number.isdigit() and len(phone_number) == 10: #validation rule for phonenumber
                    if password_ == repeat_password_:
                        registration = register_passenger(first_name, last_name, email_, gender_, age_value, address_,
                                                          phone_number,
                                                          payment_method_,
                                                          password_)

                        if registration:
                            messagebox.showinfo('Taxi-Fy says', 'Registration Successful! Please proceed to login!')
                            clear_widgets()

                    else:
                        messagebox.showwarning('Invalid!', 'The passwords do not match!')

                else:
                    messagebox.showwarning('Invalid!', 'Phone number is invalid!')

            else:
                messagebox.showwarning('Invalid!', 'Please enter an appropriate age!')

        else:
            messagebox.showwarning('Invalid!', 'The email is not valid!')

    # ---Clear entries----
    def clear_widgets():
        firstname_entry.delete(0, ctk.END)
        lastname_entry.delete(0, ctk.END)
        email_entry.delete(0, ctk.END)

        address_entry.delete(0, ctk.END)
        number_entry.delete(0, ctk.END)
        password_entry.delete(0, ctk.END)
        repeat_password_entry.delete(0, ctk.END)
        tabview.set('S I G N    I N')

    # ----Switch to login screen----
    def switch_login():
        tabview.set('S I G N    I N')

    def switch_registration():
        tabview.set('S I G N    U P')

    # --- SLIDER EVENT ---
    def slider_event(value):
        value = int(value)
        entry_var.set(value)

    def update_slider_from_entry(event):
        try:
            value = int(entry_var.get())
            if 16 <= value <= 100:
                age_slider.set(value)
                entry_var.set(value)
            else:
                entry_var.set(age_slider.get())
        except ValueError:
            pass

    # ----WIDGETS----
    # ----LOGO----
    welcome_picture = ctk.CTkImage(Image.open(r'Resources/welcome.png'), size=(150, 20))
    welcome_label = ctk.CTkLabel(window, width=150, height=20, image=welcome_picture, text='')
    welcome_label.place(relx=0.5, rely=0.03, anchor='center')

    logo_picture = ctk.CTkImage(Image.open(r'Resources/taxi-fy-trans.png'), size=(230, 110))
    logo_label = ctk.CTkLabel(window, width=230, height=110, image=logo_picture, text='')
    logo_label.place(relx=0.5, rely=0.13, anchor='center')

    # ---- SETTING UP TAB VIEW----
    tabview = ctk.CTkTabview(window, border_width=0, width=700, height=610, border_color='white',
                             segmented_button_selected_color='#0a2135', corner_radius=40, fg_color='#19181A',
                             segmented_button_unselected_color='#302f31',
                             segmented_button_selected_hover_color='#0a2135',
                             segmented_button_unselected_hover_color='#302f31')
    tabview.place(relx=0.5, rely=0.6, anchor='center')

    tabview.add("S I G N    U P")
    tabview.add("S I G N    I N")
    tabview.set("S I G N    I N")

    sign_up_frame = ctk.CTkScrollableFrame(tabview.tab('S I G N    U P'), width=450, height=500, fg_color='#19181A')
    sign_up_frame.place(relx=0.63, rely=0.5, anchor='center')

    # firstname
    firstname_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                   corner_radius=10)
    firstname_frame.grid(row=1, column=1, stick='n', pady=5)

    firstname = ctk.CTkLabel(firstname_frame, text='First Name', text_color='gray', font=('Ariel', 12), height=10)
    firstname.place(relx=0.035, rely=0.2, anchor='w')

    firstname_entry = ctk.CTkEntry(firstname_frame, border_width=0, width=290, height=30, fg_color='#2b2b2b',
                                   font=('Verdana', 14))
    firstname_entry.place(relx=0.5, rely=0.6, anchor='center')
    firstname_entry.bind('<Enter>', lambda event: on_enter_entry(event, firstname_entry))
    firstname_entry.bind('<Leave>', lambda event: on_leave_entry(event, firstname_entry))

    # lastname
    lastname_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                  corner_radius=10)
    lastname_frame.grid(row=2, column=1, stick='n', pady=5)

    lastname = ctk.CTkLabel(lastname_frame, text='Last Name', text_color='gray', font=('Ariel', 12), height=10)
    lastname.place(relx=0.035, rely=0.2, anchor='w')

    lastname_entry = ctk.CTkEntry(lastname_frame, border_width=0, width=290, height=30, fg_color='#2b2b2b',
                                  font=('Verdana', 14))
    lastname_entry.place(relx=0.5, rely=0.6, anchor='center')
    lastname_entry.bind('<Enter>', lambda event: on_enter_entry(event, lastname_entry))
    lastname_entry.bind('<Leave>', lambda event: on_leave_entry(event, lastname_entry))

    # email
    email_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                               corner_radius=10)
    email_frame.grid(row=3, column=1, stick='n', pady=5)

    email = ctk.CTkLabel(email_frame, text='Email', text_color='gray', font=('Ariel', 12), height=10)
    email.place(relx=0.035, rely=0.2, anchor='w')

    email_entry = ctk.CTkEntry(email_frame, border_width=0, width=290, height=30, fg_color='#2b2b2b',
                               font=('Verdana', 14))
    email_entry.place(relx=0.5, rely=0.6, anchor='center')
    email_entry.bind('<Enter>', lambda event: on_enter_entry(event, email_entry))
    email_entry.bind('<Leave>', lambda event: on_leave_entry(event, email_entry))

    # gender
    gender_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                corner_radius=10)
    gender_frame.grid(row=4, column=1, stick='n', pady=5)

    gender = ctk.CTkLabel(gender_frame, text='Gender', text_color='gray', font=('Ariel', 12), height=10)
    gender.place(relx=0.035, rely=0.2, anchor='w')

    # gender radiobutton
    gender_value = ctk.StringVar(value='Male')
    male_radiobtn = ctk.CTkRadioButton(gender_frame, text='Male', value='Male', variable=gender_value,
                                       border_color='gray', hover_color='#fffc04')
    male_radiobtn.place(relx=0.38, rely=0.6, anchor='center')
    female_radiobtn = ctk.CTkRadioButton(gender_frame, text='Female', value='Female', hover_color='#fffc04',
                                         border_color='gray', variable=gender_value)
    female_radiobtn.place(relx=0.72, rely=0.6, anchor='center')

    # age
    entry_var = ctk.StringVar()
    age_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                             corner_radius=10)
    age_frame.grid(row=5, column=1, stick='n', pady=5)

    age = ctk.CTkLabel(age_frame, text='Age', text_color='gray', font=('Ariel', 12), height=10)
    age.place(relx=0.035, rely=0.2, anchor='w')

    age_slider = ctk.CTkSlider(age_frame, from_=16, to=100, width=150, height=13, border_width=1,
                               border_color='gray', command=slider_event)
    age_slider.place(relx=0.3, rely=0.6, anchor='center')

    age_slider_display = ctk.CTkEntry(age_frame, font=('Ariel', 14), width=40, textvariable=entry_var)
    age_slider_display.place(relx=0.75, rely=0.6, anchor='center')

    age_slider_display.bind('<Return>', update_slider_from_entry)
    age_slider_display.bind('<FocusOut>', update_slider_from_entry)

    # address
    address_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                 corner_radius=10)
    address_frame.grid(row=6, column=1, stick='n', pady=5)
    address = ctk.CTkLabel(address_frame, text='Address', text_color='gray', font=('Ariel', 12), height=10)

    address.place(relx=0.035, rely=0.2, anchor='w')

    # address entry
    address_entry = ctk.CTkEntry(address_frame, border_width=0, width=290, height=30, fg_color='#2b2b2b',
                                 font=('Verdana', 14))
    address_entry.place(relx=0.5, rely=0.6, anchor='center')
    address_entry.bind('<Enter>', lambda event: on_enter_entry(event, address_entry))
    address_entry.bind('<Leave>', lambda event: on_leave_entry(event, address_entry))

    # number
    number_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                corner_radius=10)
    number_frame.grid(row=7, column=1, stick='n', pady=5)
    number = ctk.CTkLabel(number_frame, text='Phone number', text_color='gray', font=('Ariel', 12), height=10)
    number.place(relx=0.035, rely=0.2, anchor='w')

    # number entry
    number_entry = ctk.CTkEntry(number_frame, border_width=0, width=290, height=30, fg_color='#2b2b2b',
                                font=('Verdana', 14))
    number_entry.place(relx=0.5, rely=0.6, anchor='center')
    number_entry.bind('<Enter>', lambda event: on_enter_entry(event, number_entry))
    number_entry.bind('<Leave>', lambda event: on_leave_entry(event, number_entry))

    # payment_method
    payment_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                 corner_radius=10)
    payment_frame.grid(row=8, column=1, stick='n', pady=5)

    # payment_method combobox
    payment_method_cmbbox = ctk.CTkComboBox(payment_frame, state='readonly', width=290, fg_color='#2b2b2b',
                                            values=['Credit Card', 'E-Wallet', 'Cash'], border_width=1, height=40,
                                            dropdown_hover_color='#0a2135')
    payment_method_cmbbox.set('Select Payment Method:')
    payment_method_cmbbox.place(relx=0.5, rely=0.5, anchor='center')
    payment_method_cmbbox.bind('<Enter>', lambda event: on_enter_entry(event, payment_method_cmbbox))
    payment_method_cmbbox.bind('<Leave>', lambda event: on_leave_entry(event, payment_method_cmbbox))

    # password
    password_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                  corner_radius=10)
    password_frame.grid(row=9, column=1, stick='n', pady=5)
    password = ctk.CTkLabel(password_frame, text='New Password', text_color='gray', font=('Ariel', 12), height=10)
    password.place(relx=0.035, rely=0.2, anchor='w')

    # password entry
    password_entry = ctk.CTkEntry(password_frame, border_width=0, width=290, height=30, fg_color='#2b2b2b',
                                  font=('Verdana', 14), show='*')
    password_entry.place(relx=0.5, rely=0.6, anchor='center')
    password_entry.bind('<Enter>', lambda event: on_enter_entry(event, password_entry))
    password_entry.bind('<Leave>', lambda event: on_leave_entry(event, password_entry))

    # repeat password
    repeat_password_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                         corner_radius=10)
    repeat_password_frame.grid(row=10, column=1, stick='n', pady=5)
    repeat_password = ctk.CTkLabel(repeat_password_frame, text='Re-enter Password', text_color='gray',
                                   font=('Ariel', 12), height=10)
    repeat_password.place(relx=0.035, rely=0.2, anchor='w')

    # repeat password entry
    repeat_password_entry = ctk.CTkEntry(repeat_password_frame, border_width=0, width=290, height=30,
                                         fg_color='#2b2b2b',
                                         font=('Verdana', 14), show='*')
    repeat_password_entry.place(relx=0.5, rely=0.6, anchor='center')
    repeat_password_entry.bind('<Enter>', lambda event: on_enter_entry(event, repeat_password_entry))
    repeat_password_entry.bind('<Leave>', lambda event: on_leave_entry(event, repeat_password_entry))

    # show password
    show_password_var = ctk.BooleanVar(value=False)
    show_password = ctk.CTkCheckBox(sign_up_frame, text='Show password', variable=show_password_var,
                                    command=show_password_fun, font=('Ariel', 12), border_color='gray',
                                    hover_color='#fffc04', corner_radius=20)
    show_password.grid(row=11, column=1, stick='e', pady=5)

    # submit button
    submit_btn = ctk.CTkButton(sign_up_frame, text='Submit', text_color='WHITE', width=140,
                               corner_radius=20, height=40, command=registration_function)
    submit_btn.grid(row=13, column=1, stick='w', pady=5)

    # quit button
    quit_btn = ctk.CTkButton(sign_up_frame, text='Quit', text_color='WHITE', width=140,
                             corner_radius=25, height=40, command=quit_fun)
    quit_btn.grid(row=13, column=1, stick='e', pady=5)

    # already have an account button
    registration_button = ctk.CTkButton(sign_up_frame, text='Already have an account? Click me',
                                        text_color='WHITE', width=250, corner_radius=20,
                                        height=40, command=switch_login)
    registration_button.grid(row=15, column=1, stick='s', pady=5)

    # ---BACK BUTTON---
    back_button_picture = ctk.CTkImage(Image.open(r'Resources/back.png'), size=(15, 15))
    back_button_signup = ctk.CTkButton(tabview.tab('S I G N    U P'), text='', image=back_button_picture,
                                       text_color='WHITE',
                                       width=5, fg_color='#333333',
                                       corner_radius=40, height=10, command=back_to_main)
    back_button_signup.place(relx=0.03, rely=0.03, anchor='center')
    back_button_signup.bind('<Enter>', lambda event: on_enter_back_button(event, back_button_signup))
    back_button_signup.bind('<Leave>', lambda event: on_leave_back_button(event, back_button_signup))

    # -------------------LOGIN-----------------

    # email
    email_login_frame = ctk.CTkFrame(tabview.tab('S I G N    I N'), width=300, height=55, border_width=2,
                                     border_color='gray',
                                     corner_radius=10)
    email_login_frame.place(relx=0.5, rely=0.1, anchor='center')
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
    password_login_frame = ctk.CTkFrame(tabview.tab('S I G N    I N'), width=300, height=55, border_width=2,
                                        border_color='gray',
                                        corner_radius=10)
    password_login_frame.place(relx=0.5, rely=0.23, anchor='center')
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
    show_password_login = ctk.CTkCheckBox(tabview.tab('S I G N    I N'), text='Show password',
                                          command=show_password_login_fun,
                                          variable=show_password_login_var, font=('Ariel', 14), hover_color='#fffc04',
                                          corner_radius=20)
    show_password_login.place(relx=0.64, rely=0.34, anchor='center')

    # submit button
    submit_login = ctk.CTkButton(tabview.tab('S I G N    I N'), text='Submit', font=('Ariel', 13),
                                 corner_radius=20, width=150, height=40, command=login_function)
    submit_login.place(relx=0.37, rely=0.47, anchor='center')

    # quit button
    quit_btn_login = ctk.CTkButton(tabview.tab('S I G N    I N'), text='Quit', font=('Ariel', 13),
                                   corner_radius=20, width=150, height=40, command=quit_fun)
    quit_btn_login.place(relx=0.63, rely=0.47, anchor='center')

    # create an account button
    login_button = ctk.CTkButton(tabview.tab('S I G N    I N'), text='Create an account? Click Me', font=('Ariel', 13),
                                 corner_radius=20, width=200, height=40,
                                 command=switch_registration)
    login_button.place(relx=0.5, rely=0.59, anchor='center')

    # ---BACK BUTTON---
    back_button_login = ctk.CTkButton(tabview.tab('S I G N    I N'), text='', image=back_button_picture,
                                      text_color='WHITE',
                                      width=5, fg_color='#333333', corner_radius=40, height=10, command=back_to_main)
    back_button_login.place(relx=0.03, rely=0.03, anchor='center')
    back_button_login.bind('<Enter>', lambda event: on_enter_back_button(event, back_button_login))
    back_button_login.bind('<Leave>', lambda event: on_leave_back_button(event, back_button_login))

    window.mainloop()
