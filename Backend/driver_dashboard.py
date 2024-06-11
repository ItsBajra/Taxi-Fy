from tkinter import messagebox

import customtkinter as ctk
import geocoder
import tkintermapview
from CTkTable import CTkTable
from PIL import Image

from .backend import trip_information, complete_trip, fetch_trip_info_all

# driver dashboard
def show_dashboard(account_info, window, welcome_label, logo_label, tabview):
    trip_history_table_all = None

    # bar frame that shows the menu icon, profile icon and welcome info
    bar_frame = ctk.CTkFrame(window, width=1200, height=40, corner_radius=10, fg_color='#19181A')
    bar_frame.place(relx=0.5, rely=0.025, anchor='center')

    # trip information if the driver has been assigned to any booking
    trip_info_frame = ctk.CTkFrame(window, width=1150, height=50, corner_radius=10, fg_color='#19181A')
    trip_info_frame.place(relx=0.5, rely=0.09, anchor='center')
    trip_info_label = ctk.CTkLabel(trip_info_frame, width=1100, height=45, text='', text_color='#ffcc66')
    trip_info_label.place(relx=0.5, rely=0.5, anchor='center')

    welcome_text = ctk.CTkLabel(bar_frame, text=f"Welcome to Taxi-Fy, {account_info[1]}!", font=('Harry Plain', 14))
    welcome_text.place(relx=0.5, rely=0.5, anchor='center')

    right_dashboard_frame = ctk.CTkFrame(window, width=565, height=300, corner_radius=20, fg_color='#19181A')
    right_dashboard_frame.place(relx=0.74, rely=0.32, anchor='center')
    right_dashboard_label = ctk.CTkLabel(right_dashboard_frame, text='T R I P   D E T A I L S', text_color='#e9896a')
    right_dashboard_label.place(relx=0.5, rely=0.1, anchor='center')

    left_dashboard_frame = ctk.CTkFrame(window, width=565, height=300, corner_radius=20, fg_color='#19181A')
    left_dashboard_frame.place(relx=0.26, rely=0.32, anchor='center')
    left_dashboard_label = ctk.CTkLabel(left_dashboard_frame, text='P A S S E N G E R   D E T A I L S',
                                        text_color='#25dae9')
    left_dashboard_label.place(relx=0.5, rely=0.1, anchor='center')

    lower_dashboard_frame = ctk.CTkFrame(window, width=1150, height=355, corner_radius=20, fg_color='#19181A')
    lower_dashboard_frame.place(relx=0.5, rely=0.75, anchor='center')

    map_widget = tkintermapview.TkinterMapView(lower_dashboard_frame, width=1150, height=355, corner_radius=20)
    map_widget.place(relx=0.5, rely=0.5, anchor='center')
    map_widget.set_position(27.6839, 85.3186)
    map_widget.set_zoom(12)

    # get the trip information
    def trip_info():
        global trip_details, pickup_marker, dropoff_marker

        trip_details = trip_information(account_info[0])

        if (trip_details != None):
            pickup_location = geocoder.osm(trip_details[2])
            dropoff_location = geocoder.osm(trip_details[3])

            pickup_coordinates = pickup_location.latlng
            dropoff_coordinates = dropoff_location.latlng

            pickup_marker = map_widget.set_marker(pickup_coordinates[0], pickup_coordinates[1], text='Pickup Location')
            dropoff_marker = map_widget.set_marker(dropoff_coordinates[0], dropoff_coordinates[1],
                                                   text='Drop-off Location')

            pickup_address_label.configure(text=trip_details[2][:38], anchor='w')
            dropoff_address_label.configure(text=trip_details[3][:38], anchor='w')
            date_label.configure(text=trip_details[4], anchor='w')
            time_label.configure(text=trip_details[5], anchor='w')
            distance_label.configure(text=trip_details[6], anchor='w')
            price_label.configure(text=trip_details[7], anchor='w')
            firstname_label.configure(text=trip_details[12], anchor='w')
            lastname_label.configure(text=trip_details[13], anchor='w')
            email_label.configure(text=trip_details[14], anchor='w')
            gender_label.configure(text=trip_details[15], anchor='w')
            age_label.configure(text=trip_details[16], anchor='w')
            phone_number_label.configure(text=trip_details[18], anchor='w')
            payment_method_label.configure(text=trip_details[19], anchor='w')

            trip_info_label.configure(
                text='Y O U   H A V E   A N   U P C O M I N G   T R I P !  C H E C K   D E T A I L S   B E L O W !')

        else:
            trip_info_label.configure(
                text='N O   U P C O M I N G   T R I P S ! ! !')

    # complete a trip
    def complete_trip_fun():

        if (trip_details != None):
            confirmation = messagebox.askyesno('Taxi-Fy says', 'Are you sure you want to complete this trip?')
            if confirmation:
                trip_status = complete_trip(trip_details[0], account_info[0])

                if trip_status:
                    messagebox.showinfo('Taxi-Fy says', 'Trip Completed! Please wait for your next Trip!')
                    pickup_address_label.configure(text='', anchor='w')
                    dropoff_address_label.configure(text='', anchor='w')
                    date_label.configure(text='', anchor='w')
                    time_label.configure(text='', anchor='w')
                    distance_label.configure(text='', anchor='w')
                    price_label.configure(text='', anchor='w')
                    firstname_label.configure(text='', anchor='w')
                    lastname_label.configure(text='', anchor='w')
                    email_label.configure(text='', anchor='w')
                    gender_label.configure(text='', anchor='w')
                    age_label.configure(text='', anchor='w')
                    phone_number_label.configure(text='', anchor='w')
                    payment_method_label.configure(text='', anchor='w')

                    map_widget.delete(pickup_marker)
                    map_widget.delete(dropoff_marker)

                    trip_info()
                else:
                    messagebox.showerror('Taxi-Fy says', 'An error has occurred!')

            else:
                messagebox.showwarning('Taxi-Fy says', 'No trips to complete!')

    # show the past trip completed by the current driver
    def trip_history_fun():
        global trip_history_frame_all
        nonlocal trip_history_table_all

        id = account_info[0]
        columns, records = fetch_trip_info_all(id)

        trip_history_frame_all = ctk.CTkFrame(window, width=1150, height=700, corner_radius=20, fg_color='#19181A')
        trip_history_label = ctk.CTkLabel(trip_history_frame_all, text='Y O U R   T R I P   H I S T O R Y!',
                                          text_color='#6b5b95')
        trip_history_label.pack()

        num_empty_rows = 23 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:17] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        trip_history_table_all = CTkTable(master=trip_history_frame_all, row=23, column=len(values[0]), values=values,
                                          header_color="#406080", wraplength=100, justify='left', width=85)
        trip_history_table_all.pack(anchor='nw', padx=20, pady=(0, 20))

        return trip_history_table_all

    # updates the trip history table
    def update_trip_history_fun():
        nonlocal trip_history_table_all

        if trip_history_table_all:
            trip_history_table_all.place_forget()
            trip_history_table_all.destroy()
            trip_history_table_all = None

        id = account_info[0]
        columns, records = fetch_trip_info_all(id)

        num_empty_rows = 23 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:17] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        trip_history_table_all = CTkTable(master=trip_history_frame_all, row=23, column=len(values[0]), values=values,
                                          header_color="#406080", wraplength=100, justify='left', width=85)
        trip_history_table_all.pack(anchor='nw', padx=20, pady=(0, 20))

        return trip_history_table_all

    # menu icon button function
    def menu_toggle():
        global menu_frame

        try:
            profile_frame.place_forget()

        except:
            pass

        menu_frame = ctk.CTkFrame(window, width=300, height=800, fg_color='#171617')
        menu_frame.place(relx=0, rely=0)

        def menu_off_toggle():
            menu_frame.place_forget()

        menu_close_image = ctk.CTkImage(Image.open(r'Resources/close.png'), size=(40, 40))
        menu_close = ctk.CTkButton(menu_frame, image=menu_close_image, text='', command=menu_off_toggle, width=20,
                                   height=10, fg_color='#171617', hover_color='#171617')
        menu_close.place(relx=0.1, rely=0.025, anchor='center')

        def add_button(relx, rely, text, fgcolor, textcolor, command):
            def on_enter(event):
                Button.configure(fg_color=textcolor, text_color=fgcolor)

            def on_leave(event):
                Button.configure(fg_color=fgcolor, text_color=textcolor)

            Button = ctk.CTkButton(menu_frame, width=300, height=40, text=text, fg_color=fgcolor,
                                   text_color=textcolor, command=command)
            Button.bind('<Enter>', on_enter)
            Button.bind('<Leave>', on_leave)

            Button.place(relx=relx, rely=rely, anchor='center')

        add_button(0.5, 0.125, 'H O M E', '#171617', '#ffcc66', home_fun)
        add_button(0.5, 0.185, 'T R I P    H I S T O R Y', '#171617', '#25dae9', trip_history_btn_fun)
        add_button(0.5, 0.245, 'P R O F I L E', '#171617', '#2ecc71', profile_toggle)
        add_button(0.5, 0.305, 'L O G   O U T', '#171617', '#e74c3c', log_out_function)

        return menu_frame

    # profile icon button function
    def profile_toggle():
        global profile_frame

        try:
            menu_frame.place_forget()

        except:
            pass

        profile_frame = ctk.CTkFrame(window, width=300, height=800, fg_color='#19181A')
        profile_frame.place(relx=0.75, rely=0)

        def profile_off_toggle():
            profile_frame.place_forget()

        def add_button(relx, rely, text, fgcolor, textcolor, command):
            def on_enter(event):
                Button.configure(fg_color=textcolor, text_color=fgcolor)

            def on_leave(event):
                Button.configure(fg_color=fgcolor, text_color=textcolor)

            Button = ctk.CTkButton(profile_frame, width=300, height=40, text=text, fg_color=fgcolor,
                                   text_color=textcolor, command=command)
            Button.bind('<Enter>', on_enter)
            Button.bind('<Leave>', on_leave)

            Button.place(relx=relx, rely=rely, anchor='center')

        # add_button(0.5, 0.33, 'E D I T   P R O F I L E', '#171617', '#ffcc66')
        # add_button(0.5, 0.39, 'A C T I V I T Y', '#19181A', '#25dae9', home_fun)
        add_button(0.5, 0.33, 'L O G   O U T', '#19181A', '#e74c3c', log_out_function)

        profile_label = ctk.CTkLabel(profile_frame, text='Profile', font=('Ariel', 18))
        profile_label.place(relx=0.5, rely=0.06, anchor='center')

        profile_close_image = ctk.CTkImage(Image.open(r'Resources/close.png'), size=(40, 40))
        profile_close = ctk.CTkButton(profile_frame, image=profile_close_image, text='', command=profile_off_toggle,
                                      width=20, height=10, fg_color='#171617', hover_color='#171617')
        profile_close.place(relx=0.9, rely=0.025, anchor='center')

        profile_user_image = ctk.CTkImage(Image.open(r'Resources/profile_user.png'), size=(60, 60))
        profile_user = ctk.CTkLabel(profile_frame, image=profile_user_image, text='', width=60, height=60,
                                    fg_color='#171617')
        profile_user.place(relx=0.5, rely=0.145, anchor='center')

        name_label = ctk.CTkLabel(profile_frame, text=account_info[1] + ' ' + account_info[2], font=('Ariel', 16))
        name_label.place(relx=0.5, rely=0.22, anchor='center')

        email_label = ctk.CTkLabel(profile_frame, text=account_info[3], font=('Ariel', 14), text_color='gray')
        email_label.place(relx=0.5, rely=0.26, anchor='center')

        return profile_frame

    # home button function
    def home_fun():
        trip_history_frame_all.place_forget()
        trip_info_frame.place(relx=0.5, rely=0.09, anchor='center')
        right_dashboard_frame.place(relx=0.74, rely=0.32, anchor='center')
        left_dashboard_frame.place(relx=0.26, rely=0.32, anchor='center')
        lower_dashboard_frame.place(relx=0.5, rely=0.75, anchor='center')

    # trip history button function
    def trip_history_btn_fun():
        right_dashboard_frame.place_forget()
        left_dashboard_frame.place_forget()
        lower_dashboard_frame.place_forget()
        trip_info_frame.place_forget()
        update_trip_history_fun()
        trip_history_frame_all.place(relx=0.5, rely=0.07, anchor='n')

    # log out button function
    def log_out_function():
        logout = messagebox.askyesno('Taxi-Fy says', 'Do you really want to log out?')
        if logout:
            right_dashboard_frame.place_forget()
            left_dashboard_frame.place_forget()
            lower_dashboard_frame.place_forget()
            trip_info_frame.place_forget()
            bar_frame.place_forget()
            trip_history_frame_all.place_forget()

            try:
                menu_frame.place_forget()
            except:
                pass

            try:
                profile_frame.place_forget()
            except:
                pass

            window_width = 1000
            window_height = 800

            # ----WINDOW APPEAR IN THE MIDDLE OF THE SCREEN----
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            window.geometry(f'{window_width}x{window_height}+{x}+{y}')
            window.configure(fg_color='#0a2135')

            welcome_label.place(relx=0.5, rely=0.03, anchor='center')
            logo_label.place(relx=0.5, rely=0.13, anchor='center')
            tabview.place(relx=0.5, rely=0.6, anchor='center')

    menu_open_image = ctk.CTkImage(Image.open(r'Resources/open.png'), size=(40, 30))
    menu_open = ctk.CTkButton(bar_frame, image=menu_open_image, text='', command=menu_toggle, width=20, height=10,
                              fg_color='#19181A', hover_color='#19181A', bg_color='#19181A')
    menu_open.place(relx=0.025, rely=0.5, anchor='center')

    profile_open_image = ctk.CTkImage(Image.open(r'Resources/profile.png'), size=(40, 30))
    profile_open = ctk.CTkButton(bar_frame, image=profile_open_image, text='', command=profile_toggle, width=20,
                                 height=10, fg_color='#19181A', hover_color='#19181A')
    profile_open.place(relx=0.975, rely=0.5, anchor='center')

    # --- Right Dashboard Frame ---

    pickup_address_frame = ctk.CTkFrame(right_dashboard_frame, border_width=1, border_color='gray', width=300,
                                        height=55,
                                        fg_color='#19181A')
    pickup_address_frame.place(relx=0.31, rely=0.3, anchor='center')

    pickup_address_txt = ctk.CTkLabel(pickup_address_frame, text='Pickup Address: ', text_color='gray',
                                      font=('Ariel', 12), height=10)
    pickup_address_txt.place(relx=0.2, rely=0.2, anchor='center')

    pickup_address_label = ctk.CTkLabel(pickup_address_frame, text="", font=('Ariel', 14), height=30, width=250)
    pickup_address_label.place(relx=0.1, rely=0.6, anchor='w')

    dropoff_address_frame = ctk.CTkFrame(right_dashboard_frame, border_width=1, border_color='gray', width=300,
                                         height=55, fg_color='#19181A')
    dropoff_address_frame.place(relx=0.31, rely=0.5, anchor='center')

    dropoff_address_txt = ctk.CTkLabel(dropoff_address_frame, text='Drop-off Address: ', text_color='gray', height=10,
                                       font=('Ariel', 12))
    dropoff_address_txt.place(relx=0.2, rely=0.2, anchor='center')

    dropoff_address_label = ctk.CTkLabel(dropoff_address_frame, text="", height=30, font=('Ariel', 14), width=250)
    dropoff_address_label.place(relx=0.1, rely=0.6, anchor='w')

    distance_frame = ctk.CTkFrame(right_dashboard_frame, width=200, height=55, border_width=1,
                                  border_color='gray', fg_color='#19181A')
    distance_frame.place(relx=0.78, rely=0.3, anchor='center')

    distance_txt_label = ctk.CTkLabel(distance_frame, text='Distance: ', text_color='gray', height=10,
                                      font=('Ariel', 12))
    distance_txt_label.place(relx=0.2, rely=0.2, anchor='center')

    distance_label = ctk.CTkLabel(distance_frame, text='', height=30, font=('Ariel', 14), width=150)
    distance_label.place(relx=0.1, rely=0.6, anchor='w')

    price_frame = ctk.CTkFrame(right_dashboard_frame, width=200, height=55, border_width=1,
                               border_color='gray', fg_color='#19181A')
    price_frame.place(relx=0.78, rely=0.5, anchor='center')

    price_txt_label = ctk.CTkLabel(price_frame, text='Fare: ', text_color='gray', height=10, font=('Ariel', 12))
    price_txt_label.place(relx=0.2, rely=0.2, anchor='center')

    price_label = ctk.CTkLabel(price_frame, text='', height=30, font=('Ariel', 14), width=150)
    price_label.place(relx=0.1, rely=0.6, anchor='w')

    date_frame = ctk.CTkFrame(right_dashboard_frame, width=300, height=55, border_width=1,
                              border_color='gray', fg_color='#19181A')
    date_frame.place(relx=0.31, rely=0.7, anchor='center')

    date_txt_label = ctk.CTkLabel(date_frame, text='Pickup Date: ', text_color='gray', height=10, font=('Ariel', 12))
    date_txt_label.place(relx=0.2, rely=0.2, anchor='center')

    date_label = ctk.CTkLabel(date_frame, text='', height=30, font=('Ariel', 14), width=250)
    date_label.place(relx=0.1, rely=0.6, anchor='w')

    time_frame = ctk.CTkFrame(right_dashboard_frame, width=200, height=55, border_width=1,
                              border_color='gray', fg_color='#19181A')
    time_frame.place(relx=0.78, rely=0.7, anchor='center')

    time_txt_label = ctk.CTkLabel(time_frame, text='Pickup Time: ', text_color='gray', height=10, font=('Ariel', 12))
    time_txt_label.place(relx=0.25, rely=0.2, anchor='center')

    time_label = ctk.CTkLabel(time_frame, text='', height=30, font=('Ariel', 13), width=150)
    time_label.place(relx=0.1, rely=0.6, anchor='w')

    complete_btn = ctk.CTkButton(right_dashboard_frame, width=300, height=45, corner_radius=10,
                                 text='C O M P L E T E   T R I P', command=complete_trip_fun)
    complete_btn.place(relx=0.31, rely=0.9, anchor='center')

    refresh_btn = ctk.CTkButton(right_dashboard_frame, width=200, height=45, corner_radius=10, text='R E F R E S H',
                                command=trip_info)
    refresh_btn.place(relx=0.78, rely=0.9, anchor='center')

    # --- Left Dashboard Frame ---

    firstname_frame = ctk.CTkFrame(left_dashboard_frame, border_width=1, border_color='gray', width=260,
                                   height=55, fg_color='#19181A')
    firstname_frame.place(relx=0.265, rely=0.3, anchor='center')

    firstname_txt = ctk.CTkLabel(firstname_frame, text='First Name', text_color='gray',
                                 font=('Ariel', 12), height=10)
    firstname_txt.place(relx=0.15, rely=0.2, anchor='center')

    firstname_label = ctk.CTkLabel(firstname_frame, text="", font=('Ariel', 14), height=30, width=210)
    firstname_label.place(relx=0.1, rely=0.6, anchor='w')

    lastname_frame = ctk.CTkFrame(left_dashboard_frame, width=260, height=55, border_width=1,
                                  border_color='gray', fg_color='#19181A')
    lastname_frame.place(relx=0.74, rely=0.3, anchor='center')

    lastname_txt = ctk.CTkLabel(lastname_frame, text='Last Name ', text_color='gray', height=10,
                                font=('Ariel', 12))
    lastname_txt.place(relx=0.15, rely=0.2, anchor='center')

    lastname_label = ctk.CTkLabel(lastname_frame, text='', height=30, font=('Ariel', 14), width=210)
    lastname_label.place(relx=0.1, rely=0.6, anchor='w')

    email_frame = ctk.CTkFrame(left_dashboard_frame, border_width=1, border_color='gray', width=526,
                               height=55, fg_color='#19181A')
    email_frame.place(relx=0.5, rely=0.5, anchor='center')

    email_txt = ctk.CTkLabel(email_frame, text='Email:', text_color='gray',
                             font=('Ariel', 12), height=10)
    email_txt.place(relx=0.05, rely=0.2, anchor='center')

    email_label = ctk.CTkLabel(email_frame, text="", font=('Ariel', 14), height=30, width=480)
    email_label.place(relx=0.05, rely=0.6, anchor='w')

    phone_number_frame = ctk.CTkFrame(left_dashboard_frame, border_width=1, border_color='gray', width=260,
                                      height=55, fg_color='#19181A')
    phone_number_frame.place(relx=0.265, rely=0.7, anchor='center')

    phone_number_txt = ctk.CTkLabel(phone_number_frame, text='Phone number', text_color='gray',
                                    font=('Ariel', 12), height=10)
    phone_number_txt.place(relx=0.2, rely=0.2, anchor='center')

    phone_number_label = ctk.CTkLabel(phone_number_frame, text="", font=('Ariel', 14), height=30, width=210)
    phone_number_label.place(relx=0.1, rely=0.6, anchor='w')

    gender_frame = ctk.CTkFrame(left_dashboard_frame, width=260, height=55, border_width=1,
                                border_color='gray', fg_color='#19181A')
    gender_frame.place(relx=0.74, rely=0.7, anchor='center')

    gender_txt = ctk.CTkLabel(gender_frame, text='Gender', text_color='gray', height=10,
                              font=('Ariel', 12))
    gender_txt.place(relx=0.1, rely=0.2, anchor='center')

    gender_label = ctk.CTkLabel(gender_frame, text='', height=30, font=('Ariel', 14), width=210)
    gender_label.place(relx=0.1, rely=0.6, anchor='w')

    age_frame = ctk.CTkFrame(left_dashboard_frame, border_width=1, border_color='gray', width=260,
                             height=55, fg_color='#19181A')
    age_frame.place(relx=0.265, rely=0.9, anchor='center')

    age_txt = ctk.CTkLabel(age_frame, text='Age', text_color='gray',
                           font=('Ariel', 12), height=10)
    age_txt.place(relx=0.07, rely=0.2, anchor='center')

    age_label = ctk.CTkLabel(age_frame, text="", font=('Ariel', 14), height=30, width=210)
    age_label.place(relx=0.1, rely=0.6, anchor='w')

    payment_method_frame = ctk.CTkFrame(left_dashboard_frame, width=260, height=55, border_width=1,
                                        border_color='gray', fg_color='#19181A')
    payment_method_frame.place(relx=0.74, rely=0.9, anchor='center')

    payment_method_txt = ctk.CTkLabel(payment_method_frame, text='Payment Method', text_color='gray', height=10,
                                      font=('Ariel', 12))
    payment_method_txt.place(relx=0.2, rely=0.2, anchor='center')

    payment_method_label = ctk.CTkLabel(payment_method_frame, text='', height=30, font=('Ariel', 14), width=210)
    payment_method_label.place(relx=0.1, rely=0.6, anchor='w')

    trip_info()
    trip_history_fun()
