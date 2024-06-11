from tkinter import messagebox

import customtkinter as ctk
from CTkTable import CTkTable
from PIL import Image

from .backend import approve_driver_request, fetch_all_drivers, approve_booking_request, fetch_new_drivers, \
    reject_driver_request, reject_booking_request
from .backend import fetch_all_bookings, fetch_all_passengers
from .backend import fetch_new_booking_main_info, fetch_available_drivers_main_info, fetch_new_bookings
from .backend import new_booking_requests, available_drivers, completed_trips, total_passengers, new_drivers_requests


# show admin dashboard
def show_dashboard(account_info, window, welcome_label, logo_label, login_frame):
    # define variables
    bookings_table = None
    available_drivers_table = None
    drivers_request_table = None
    bookings_main_table = None
    all_bookings_table = None
    all_drivers_table = None
    all_passengers_table = None

    # bar frame that shows the menu icon
    bar_frame = ctk.CTkFrame(window, width=1200, height=40, corner_radius=10, fg_color='#19181A')
    bar_frame.place(relx=0.5, rely=0.025, anchor='center')

    bar_text = ctk.CTkLabel(bar_frame, text='A D M I N   D A S H B O A R D')
    bar_text.place(relx=0.5, rely=0.5, anchor='center')

    total_info_frame = ctk.CTkFrame(window, width=1150, height=210, corner_radius=20, fg_color='#19181A')
    total_info_frame.place(relx=0.5, rely=0.197, anchor='center')

    new_booking_table_frame = ctk.CTkFrame(window, width=650, height=500, corner_radius=20, fg_color='#19181A')
    new_booking_table_frame.place(relx=0.295, rely=0.35, anchor='n')

    new_bookings_label = ctk.CTkLabel(new_booking_table_frame, text='N E W   B O O K I N G S')
    new_bookings_label.place(relx=0.5, rely=0.05, anchor='center')

    available_drivers_frame = ctk.CTkFrame(window, width=475, height=500, corner_radius=20, fg_color='#19181A')
    available_drivers_frame.place(relx=0.78, rely=0.35, anchor='n')

    available_drivers_label = ctk.CTkLabel(available_drivers_frame, text='A V A I L A B L E   D R I V E R S')
    available_drivers_label.place(relx=0.5, rely=0.02, anchor='n')

    # ----- Approve bookings ------
    def approve_bookings():
        global pending_bookings_frame, approve_booking_table_frame
        nonlocal bookings_table

        pending_bookings_frame = ctk.CTkFrame(window, width=1150, height=210, corner_radius=20, fg_color='#19181A')

        pending_bookings_txt = ctk.CTkLabel(pending_bookings_frame, text='N E W   B O O K I N G S')
        pending_bookings_txt.place(relx=0.5, rely=0.05, anchor='center')

        approve_booking_table_frame = ctk.CTkFrame(window, width=650, height=500, corner_radius=20, fg_color='#19181A')

        approve_bookings_txt = ctk.CTkLabel(approve_booking_table_frame, text='A P P R O V E   B O O K I N G S')
        approve_bookings_txt.place(relx=0.5, rely=0.05, anchor='center')

        enter_id_label = ctk.CTkLabel(approve_booking_table_frame, text='Enter the Booking ID: ', font=('Verdana', 14))
        enter_id_label.place(relx=0.35, rely=0.2, anchor='center')

        enter_id_entry = ctk.CTkEntry(approve_booking_table_frame, width=200)
        enter_id_entry.place(relx=0.65, rely=0.2, anchor='center')

        enter_driver_label = ctk.CTkLabel(approve_booking_table_frame, text='Assign the Driver (ID): ',
                                          font=('Verdana', 14))
        enter_driver_label.place(relx=0.35, rely=0.3, anchor='center')

        enter_driver_entry = ctk.CTkEntry(approve_booking_table_frame, width=200)
        enter_driver_entry.place(relx=0.65, rely=0.3, anchor='center')

        # approve booking button function
        def approve_bookings_btn_fun():
            booking_id = enter_id_entry.get()
            driver_id = enter_driver_entry.get()

            if not all([booking_id, driver_id]):
                messagebox.showwarning('Invalid!', 'Please fill out all the information!')
                return

            approve_booking = approve_booking_request(booking_id, driver_id)

            if approve_booking:
                messagebox.showinfo('Taxi-Fy says', 'Booking approved and Driver assigned successfully!')
                enter_id_entry.delete(0, ctk.END)
                enter_driver_entry.delete(0, ctk.END)
                update_approve_bookings()
                update_available_drivers_table()

        # reject booking button function
        def reject_bookings_btn_fun():
            booking_id = enter_id_entry.get()

            if not all([booking_id]):
                messagebox.showwarning('Invalid!', 'Please fill out all the information!')
                return

            approve_booking = reject_booking_request(booking_id)

            if approve_booking:
                messagebox.showinfo('Taxi-Fy says', 'Booking rejected!')
                enter_id_entry.delete(0, ctk.END)
                enter_driver_entry.delete(0, ctk.END)
                update_approve_bookings()
                update_available_drivers_table()

        approve_button = ctk.CTkButton(approve_booking_table_frame, width=200, height=40, text='A P P R O V E',
                                       command=approve_bookings_btn_fun)
        approve_button.place(relx=0.3, rely=0.5, anchor='center')

        reject_button = ctk.CTkButton(approve_booking_table_frame, width=200, height=40, text='R E J E C T',
                                      command=reject_bookings_btn_fun)
        reject_button.place(relx=0.7, rely=0.5, anchor='center')

        columns, records = fetch_new_bookings()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:15] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        bookings_table = CTkTable(master=pending_bookings_frame, row=6, column=len(values[0]), values=values,
                                  header_color="#406080", wraplength=70, justify='left', width=85)
        bookings_table.place(relx=0.5, rely=0.53, anchor='center')

        return bookings_table

    approve_bookings()

    # approve bookings button in the menu function
    def approve_bookings_fun():
        total_info_frame.place_forget()
        new_booking_table_frame.place_forget()
        approve_drivers_frame.place_forget()
        approve_drivers_table_frame.place_forget()
        all_bookings_frame.place_forget()
        all_drivers_frame.place_forget()
        all_passengers_frame.place_forget()
        update_approve_bookings()
        update_available_drivers_table()
        pending_bookings_frame.place(relx=0.5, rely=0.197, anchor='center')
        approve_booking_table_frame.place(relx=0.295, rely=0.35, anchor='n')
        available_drivers_frame.place(relx=0.78, rely=0.35, anchor='n')

    # ---- Update Table ---
    def update_approve_bookings():
        nonlocal bookings_table

        if bookings_table:
            bookings_table.place_forget()
            bookings_table.destroy()
            bookings_table = None

        columns, records = fetch_new_bookings()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:15] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        bookings_table = CTkTable(master=pending_bookings_frame, row=6, column=len(values[0]), values=values,
                                  header_color="#406080", wraplength=70, justify='left', width=85)
        bookings_table.place(relx=0.5, rely=0.53, anchor='center')

        return bookings_table

    # ---- Home function ----
    def home_fun():
        pending_bookings_frame.place_forget()
        approve_booking_table_frame.place_forget()
        approve_drivers_frame.place_forget()
        approve_drivers_table_frame.place_forget()
        all_bookings_frame.place_forget()
        all_drivers_frame.place_forget()
        all_passengers_frame.place_forget()
        update_new_bookings_table_main()
        update_available_drivers_table()
        total_info_frame.place(relx=0.5, rely=0.197, anchor='center')
        new_booking_table_frame.place(relx=0.295, rely=0.35, anchor='n')
        available_drivers_frame.place(relx=0.78, rely=0.35, anchor='n')

    # ---- Approve Driver -----
    def approve_driver():
        global approve_drivers_frame, approve_drivers_table_frame
        nonlocal drivers_request_table

        approve_drivers_frame = ctk.CTkFrame(window, width=1150, height=500, corner_radius=20, fg_color='#19181A')

        approve_drivers_txt = ctk.CTkLabel(approve_drivers_frame, text='N E W   D R I V E R    R E Q U E S T S')
        approve_drivers_txt.place(relx=0.5, rely=0.05, anchor='center')

        approve_drivers_table_frame = ctk.CTkFrame(window, width=1150, height=200, corner_radius=20, fg_color='#19181A')

        approve_bookings_txt = ctk.CTkLabel(approve_drivers_table_frame, text='A P P R O V E   D R I V E R')
        approve_bookings_txt.place(relx=0.5, rely=0.1, anchor='center')

        enter_id_label = ctk.CTkLabel(approve_drivers_table_frame, text='Enter the Driver ID: ', font=('Verdana', 14))
        enter_id_label.place(relx=0.4, rely=0.4, anchor='center')

        enter_id_entry = ctk.CTkEntry(approve_drivers_table_frame, width=200)
        enter_id_entry.place(relx=0.6, rely=0.4, anchor='center')

        def approve_bookings_btn_fun():
            driver_id = enter_id_entry.get()

            if not all([driver_id]):
                messagebox.showwarning('Invalid!', 'Please fill out all the information!')
                return

            approve_drivers = approve_driver_request(driver_id)

            if approve_drivers:
                messagebox.showinfo('Taxi-Fy says', 'Driver verified successfully!')
                enter_id_entry.delete(0, ctk.END)
                update_approve_bookings()
                update_available_drivers_table()
                update_driver_request_table()

        def reject_bookings_btn_fun():
            driver_id = enter_id_entry.get()

            if not all([driver_id]):
                messagebox.showwarning('Invalid!', 'Please fill out all the information!')
                return

            approve_drivers = reject_driver_request(driver_id)

            if approve_drivers:
                messagebox.showinfo('Taxi-Fy says', 'Driver rejected!')
                enter_id_entry.delete(0, ctk.END)
                update_approve_bookings()
                update_available_drivers_table()
                update_driver_request_table()

        approve_button = ctk.CTkButton(approve_drivers_table_frame, width=200, height=40, text='A P P R O V E',
                                       command=approve_bookings_btn_fun)
        approve_button.place(relx=0.3, rely=0.8, anchor='center')

        reject_button = ctk.CTkButton(approve_drivers_table_frame, width=200, height=40, text='R E J E C T',
                                      command=reject_bookings_btn_fun)
        reject_button.place(relx=0.7, rely=0.8, anchor='center')

        columns, records = fetch_new_drivers()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:20] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        drivers_request_table = CTkTable(master=approve_drivers_frame, row=15, column=len(values[0]), values=values,
                                         header_color="#406080", wraplength=70, justify='left', width=80)
        drivers_request_table.place(relx=0.5, rely=0.53, anchor='center')

        return drivers_request_table

    approve_driver()

    # updates the table showing all the driver requests
    def update_driver_request_table():
        nonlocal drivers_request_table

        if drivers_request_table:
            drivers_request_table.place_forget()
            drivers_request_table.destroy()
            drivers_request_table = None

        columns, records = fetch_new_drivers()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:20] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        drivers_request_table = CTkTable(master=approve_drivers_frame, row=15, column=len(values[0]), values=values,
                                         header_color="#406080", wraplength=70, justify='left', width=80)
        drivers_request_table.place(relx=0.5, rely=0.53, anchor='center')

        return drivers_request_table

    # approve drivers button in the menu function
    def approve_drivers_fun():
        pending_bookings_frame.place_forget()
        approve_booking_table_frame.place_forget()
        total_info_frame.place_forget()
        new_booking_table_frame.place_forget()
        available_drivers_frame.place_forget()
        all_bookings_frame.place_forget()
        all_drivers_frame.place_forget()
        update_driver_request_table()
        approve_drivers_frame.place(relx=0.5, rely=0.39, anchor='center')
        approve_drivers_table_frame.place(relx=0.5, rely=0.85, anchor='center')

    # log out button function
    def log_out_function():
        logout = messagebox.askyesno('Taxi-Fy says', 'Do you really want to log out?')
        if logout:
            pending_bookings_frame.place_forget()
            approve_booking_table_frame.place_forget()
            total_info_frame.place_forget()
            new_booking_table_frame.place_forget()
            available_drivers_frame.place_forget()
            bar_frame.place_forget()
            approve_drivers_frame.place_forget()
            approve_drivers_table_frame.place_forget()
            all_bookings_frame.place_forget()
            all_drivers_frame.place_forget()
            all_passengers_frame.place_forget()

            try:
                menu_frame.place_forget()
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
            login_frame.place(relx=0.5, rely=0.6, anchor='center')

    # ---- All bookings ----
    def all_bookings():
        global all_bookings_frame
        nonlocal all_bookings_table

        all_bookings_frame = ctk.CTkFrame(window, width=1150, height=700, fg_color='#171617')

        all_bookings_text = ctk.CTkLabel(all_bookings_frame, text='A L L   B O O K I N G S')
        all_bookings_text.place(relx=0.5, rely=0.05, anchor='center')

        columns, records = fetch_all_bookings()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:20] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        all_bookings_table = CTkTable(master=all_bookings_frame, row=18, column=len(values[0]), values=values,
                                      header_color="#406080", wraplength=70, justify='left', width=100)
        all_bookings_table.place(relx=0.5, rely=0.53, anchor='center')

        return all_bookings_table

    all_bookings()

    # updates the all bookings table
    def update_all_bookings():
        nonlocal all_bookings_table

        if all_bookings_table:
            all_bookings_table.place_forget()
            all_bookings_table.destroy()
            all_bookings_table = None

        columns, records = fetch_all_bookings()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:20] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        all_bookings_table = CTkTable(master=all_bookings_frame, row=18, column=len(values[0]), values=values,
                                      header_color="#406080", wraplength=70, justify='left', width=100)
        all_bookings_table.place(relx=0.5, rely=0.53, anchor='center')

        return all_bookings_table

    # all bookings button in the menu function
    def all_bookings_fun():
        pending_bookings_frame.place_forget()
        approve_booking_table_frame.place_forget()
        total_info_frame.place_forget()
        new_booking_table_frame.place_forget()
        available_drivers_frame.place_forget()
        approve_drivers_frame.place_forget()
        approve_drivers_table_frame.place_forget()
        all_drivers_frame.place_forget()
        all_passengers_frame.place_forget()
        update_all_bookings()
        all_bookings_frame.place(relx=0.5, rely=0.5, anchor='center')

    # ---- all drivers ----
    def all_drivers():
        global all_drivers_frame
        nonlocal all_drivers_table

        all_drivers_frame = ctk.CTkFrame(window, width=1150, height=700, fg_color='#171617')

        all_drivers_text = ctk.CTkLabel(all_drivers_frame, text='A L L   D R I V E R S')
        all_drivers_text.place(relx=0.5, rely=0.05, anchor='center')

        columns, records = fetch_all_drivers()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:20] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        all_drivers_table = CTkTable(master=all_drivers_frame, row=15, column=len(values[0]), values=values,
                                     header_color="#406080", wraplength=70, justify='left', width=80)
        all_drivers_table.place(relx=0.5, rely=0.53, anchor='center')

        return all_drivers_table

    all_drivers()

    # updates the all drivers table
    def update_all_drivers():
        nonlocal all_drivers_table

        if all_drivers_table:
            all_drivers_table.place_forget()
            all_drivers_table.destroy()
            all_drivers_table = None

        columns, records = fetch_all_drivers()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:20] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        all_drivers_table = CTkTable(master=all_drivers_frame, row=20, column=len(values[0]), values=values,
                                     header_color="#406080", wraplength=70, justify='left', width=80)
        all_drivers_table.place(relx=0.5, rely=0.53, anchor='center')

        return all_drivers_table

    # all drivers button function in the menu
    def all_drivers_fun():
        pending_bookings_frame.place_forget()
        approve_booking_table_frame.place_forget()
        total_info_frame.place_forget()
        new_booking_table_frame.place_forget()
        available_drivers_frame.place_forget()
        approve_drivers_frame.place_forget()
        approve_drivers_table_frame.place_forget()
        all_bookings_frame.place_forget()
        all_passengers_frame.place_forget()
        update_all_drivers()
        all_drivers_frame.place(relx=0.5, rely=0.5, anchor='center')

    # --- all passengers ----
    def all_passengers():
        global all_passengers_frame
        nonlocal all_passengers_table

        all_passengers_frame = ctk.CTkFrame(window, width=1150, height=700, fg_color='#171617')

        all_passengers_text = ctk.CTkLabel(all_passengers_frame, text='A L L   P A S S E N G E R S')
        all_passengers_text.place(relx=0.5, rely=0.05, anchor='center')

        columns, records = fetch_all_passengers()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:20] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        all_passengers_table = CTkTable(master=all_passengers_frame, row=15, column=len(values[0]), values=values,
                                        header_color="#406080", wraplength=70, justify='left', width=110)
        all_passengers_table.place(relx=0.5, rely=0.53, anchor='center')

        return all_passengers_table

    all_passengers()

    # updates the table showing all the passenger
    def update_all_passengers():
        nonlocal all_passengers_table

        if all_passengers_table:
            all_passengers_table.place_forget()
            all_passengers_table.destroy()
            all_passengers_table = None

        columns, records = fetch_all_passengers()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:20] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        all_passengers_table = CTkTable(master=all_passengers_frame, row=20, column=len(values[0]), values=values,
                                        header_color="#406080", wraplength=70, justify='left', width=110)
        all_passengers_table.place(relx=0.5, rely=0.53, anchor='center')

        return all_passengers_table

    # all passenger button in the menu function
    def all_passengers_fun():
        pending_bookings_frame.place_forget()
        approve_booking_table_frame.place_forget()
        total_info_frame.place_forget()
        new_booking_table_frame.place_forget()
        available_drivers_frame.place_forget()
        approve_drivers_frame.place_forget()
        approve_drivers_table_frame.place_forget()
        all_bookings_frame.place_forget()
        all_drivers_frame.place_forget()
        update_all_passengers()
        all_passengers_frame.place(relx=0.5, rely=0.5, anchor='center')

    # ---- menu toggle -----

    def menu_toggle():
        global menu_frame

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
        add_button(0.5, 0.185, 'A P P R O V E   B O O K I N G S', '#171617', '#25dae9', approve_bookings_fun)
        add_button(0.5, 0.245, 'A P P R O V E   D R I V E R S', '#171617', '#e74c3c', approve_drivers_fun)
        add_button(0.5, 0.305, 'A L L   B O O K I N G S', '#171617', '#e9896a', all_bookings_fun)
        add_button(0.5, 0.365, 'D R I V E R S', '#171617', '#142de3', all_drivers_fun)
        add_button(0.5, 0.425, 'P A S S E N G E R S', '#171617', '#6b5b95', all_passengers_fun)
        add_button(0.5, 0.485, 'L O G   O U T', '#171617', '#2ecc71', log_out_function)
        return menu_frame

    # ----new bookings table ----
    def new_bookings_table_main():
        nonlocal bookings_main_table

        columns, records = fetch_new_booking_main_info()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:15] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        bookings_main_table = CTkTable(master=new_booking_table_frame, row=14, column=len(values[0]), values=values,
                                       header_color="#406080", wraplength=70, justify='left', width=85)
        bookings_main_table.place(relx=0.5, rely=0.53, anchor='center')

        return bookings_main_table

    new_bookings_table_main()

    # updates the new bookings table
    def update_new_bookings_table_main():
        nonlocal bookings_main_table

        if bookings_main_table:
            bookings_main_table.place_forget()
            bookings_main_table.destroy()
            bookings_main_table = None

        columns, records = fetch_new_booking_main_info()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:15] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        bookings_main_table = CTkTable(master=new_booking_table_frame, row=14, column=len(values[0]), values=values,
                                       header_color="#406080", wraplength=70, justify='left', width=85)
        bookings_main_table.place(relx=0.5, rely=0.53, anchor='center')

        return bookings_main_table

    # ----Available Drivers Table----
    def available_drivers_table_main():
        nonlocal available_drivers_table

        columns, records = fetch_available_drivers_main_info()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:15] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        available_drivers_table = CTkTable(master=available_drivers_frame, row=14, column=len(values[0]), values=values,
                                           header_color="#406080", wraplength=70, justify='left', width=85)
        available_drivers_table.place(relx=0.5, rely=0.53, anchor='center')

        return available_drivers_table

    available_drivers_table_main()

    # updates the table showing available drivers
    def update_available_drivers_table():
        nonlocal available_drivers_table

        if available_drivers_table:
            available_drivers_table.place_forget()
            available_drivers_table.destroy()
            available_drivers_table = None

        columns, records = fetch_available_drivers_main_info()

        num_empty_rows = 5 - len(records)
        empty_rows = [[''] * len(columns) for _ in range(num_empty_rows)]
        records += empty_rows if num_empty_rows > 0 else []

        compressed_records = []
        for row in records:
            compressed_row = []
            for value in row:
                compressed_value = str(value)[:15] if isinstance(value, str) else str(value)
                compressed_row.append(compressed_value)
            compressed_records.append(compressed_row)

        values = [columns] + compressed_records

        available_drivers_table = CTkTable(master=available_drivers_frame, row=14, column=len(values[0]), values=values,
                                           header_color="#406080", wraplength=70, justify='left', width=85)
        available_drivers_table.place(relx=0.5, rely=0.53, anchor='center')

        return available_drivers_table

    # ---- menu icon ----

    menu_open_image = ctk.CTkImage(Image.open(r'Resources/open.png'), size=(40, 30))
    menu_open = ctk.CTkButton(bar_frame, image=menu_open_image, text='', command=menu_toggle, width=20, height=10,
                              fg_color='#19181A', hover_color='#19181A', bg_color='#19181A')
    menu_open.place(relx=0.025, rely=0.5, anchor='center')

    # ----- total info -----

    new_bookings_frame = ctk.CTkFrame(total_info_frame, width=200, height=170, corner_radius=20)
    new_bookings_frame.place(relx=0.105, rely=0.1, anchor='n')

    new_bookings_txt = ctk.CTkLabel(new_bookings_frame, text='N E W   T R I P   R E Q U E S T S', font=('', 11),
                                    text_color='#25dae9')
    new_bookings_txt.place(relx=0.5, rely=0.1, anchor='n')

    new_bookings_label = ctk.CTkLabel(new_bookings_frame, text='', font=('', 16))
    new_bookings_label.place(relx=0.5, rely=0.6, anchor='center')

    # counts the number of new bookings
    def new_bookings_count_fun():
        count = new_booking_requests()
        new_bookings_label.configure(text=count)

    new_bookings_count_fun()

    available_drivers_count_frame = ctk.CTkFrame(total_info_frame, width=200, height=170, corner_radius=20)
    available_drivers_count_frame.place(relx=0.3, rely=0.1, anchor='n')

    available_drivers_txt = ctk.CTkLabel(available_drivers_count_frame, text='A V A I L A B L E   D R I V E R S',
                                         font=('', 11), text_color='#e9896a')
    available_drivers_txt.place(relx=0.5, rely=0.1, anchor='n')

    available_drivers_label = ctk.CTkLabel(available_drivers_count_frame, text='', font=('', 16))
    available_drivers_label.place(relx=0.5, rely=0.6, anchor='center')

    # counts the total number of available drivers
    def available_drivers_fun():
        count = available_drivers()
        available_drivers_label.configure(text=count)

    available_drivers_fun()

    completed_trips_frame = ctk.CTkFrame(total_info_frame, width=200, height=170, corner_radius=20)
    completed_trips_frame.place(relx=0.495, rely=0.1, anchor='n')

    completed_trips_txt = ctk.CTkLabel(completed_trips_frame, text='C O M P L E T E D   T R I P S', font=('', 11),
                                       text_color='#6b5b95')
    completed_trips_txt.place(relx=0.5, rely=0.1, anchor='n')

    completed_trips_label = ctk.CTkLabel(completed_trips_frame, text='', font=('', 16))
    completed_trips_label.place(relx=0.5, rely=0.6, anchor='center')

    # counts the total number of completed trips
    def completed_trips_fun():
        count = completed_trips()
        completed_trips_label.configure(text=count)

    completed_trips_fun()

    total_passengers_frame = ctk.CTkFrame(total_info_frame, width=200, height=170, corner_radius=20)
    total_passengers_frame.place(relx=0.690, rely=0.1, anchor='n')

    total_passengers_txt = ctk.CTkLabel(total_passengers_frame, text='P A S S E N G E R S', font=('', 11),
                                        text_color='#ffcc66')
    total_passengers_txt.place(relx=0.5, rely=0.1, anchor='n')

    total_passengers_label = ctk.CTkLabel(total_passengers_frame, text='', font=('', 16))
    total_passengers_label.place(relx=0.5, rely=0.6, anchor='center')

    # counts the total number of passengers
    def total_passengers_fun():
        count = total_passengers()
        total_passengers_label.configure(text=count)

    total_passengers_fun()

    new_driver_frame = ctk.CTkFrame(total_info_frame, width=200, height=170, corner_radius=20)
    new_driver_frame.place(relx=0.885, rely=0.1, anchor='n')

    new_driver_txt = ctk.CTkLabel(new_driver_frame, text='N E W   D R I V E R   R E Q U E S T S', font=('', 11),
                                  text_color='#2ecc71')
    new_driver_txt.place(relx=0.5, rely=0.1, anchor='n')

    new_driver_label = ctk.CTkLabel(new_driver_frame, text='', font=('', 16))
    new_driver_label.place(relx=0.5, rely=0.6, anchor='center')

    # counts the total number of new driver request
    def new_drivers_fun():
        count = new_drivers_requests()
        new_driver_label.configure(text=count)

    new_drivers_fun()

    # ----
