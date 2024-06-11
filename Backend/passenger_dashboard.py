from datetime import date
from tkinter import messagebox

import customtkinter as ctk
import geocoder
import certifi
import tkintermapview
from CTkTable import *
from PIL import Image
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from tkcalendar import Calendar
from tktimepicker import SpinTimePickerOld, constants

import ssl

from .backend import send_booking_request, fetch_booking_info, fetch_booking_info_all, send_update_request, \
    send_delete_request, edit_profile, trip_information_passenger


# passenger dashboard
def show_dashboard(account_info, window, welcome_label_1, logo_label, reg_login_frame):
    def dashboard():

        # defining global variables

        global pickup_date, pickup_time, pickup_address, dropoff_address, distance, fare, booking_id

        pickup_date = None
        pickup_time = None
        pickup_address = None
        dropoff_address = None
        distance = None
        fare = None
        bookings_table = None
        bookings_table_all = None
        booking_id = None

        # main frames
        dashboard_frame = ctk.CTkFrame(window, width=800, height=730, corner_radius=20, fg_color='#19181A')
        dashboard_frame.place(relx=0.635, rely=0.525, anchor='center')

        second_dashboard_frame = ctk.CTkFrame(window, width=300, height=730, corner_radius=20, fg_color='#19181A')
        second_dashboard_frame.place(relx=0.155, rely=0.525, anchor='center')

        # ----functional map widget-----
        map_widget = tkintermapview.TkinterMapView(dashboard_frame, width=800, height=580, corner_radius=20)
        map_widget.place(relx=0.5, rely=0.58, anchor='center')
        map_widget.set_position(27.6839, 85.3186)
        map_widget.set_zoom(16)

        pickup_marker = [None]
        dropoff_marker = [None]

        # cancel booking function
        def delete_bookings():
            global delete_bookings_frame

            delete_bookings_frame = ctk.CTkFrame(window, width=750, height=400, corner_radius=20, fg_color='#19181A')
            delete_bookings_label = ctk.CTkLabel(delete_bookings_frame,
                                                 text='C A N C E L   Y O U R   B O O K I N G S !',
                                                 font=('Ariel', 14), text_color='#25dae9')
            delete_bookings_label.place(relx=0.5, rely=0.1, anchor='center')

            def clear_widgets_delete():
                booking_id_delete_entry.delete(0, ctk.END)

            def send_delete_request_fun():
                global booking_id

                booking_id = booking_id_delete_entry.get()
                passenger_id = account_info[0]

                if not all([booking_id, passenger_id]):
                    messagebox.showwarning('Invalid!', 'Please fill out all the information!')
                    return

                booking_request = send_delete_request(booking_id, passenger_id)

                if booking_request:
                    messagebox.showinfo('Taxi-Fy says',
                                        'Booking Cancelled Successfully!')
                    clear_widgets_delete()
                    update_table()

            booking_id_delete_label = ctk.CTkLabel(delete_bookings_frame, text='Enter the Booking ID: ',
                                                   font=('Ariel', 14))
            booking_id_delete_label.place(relx=0.35, rely=0.3, anchor='center')

            booking_id_delete_entry = ctk.CTkEntry(delete_bookings_frame, width=200, height=30)
            booking_id_delete_entry.place(relx=0.6, rely=0.3, anchor='center')

            send_delete_request_btn = ctk.CTkButton(delete_bookings_frame, width=200, height=30,
                                                    text='Cancel booking',
                                                    command=send_delete_request_fun)
            send_delete_request_btn.place(relx=0.5, rely=0.9, anchor='center')

        # short information frame
        def info_fun():
            global info_frame

            info_frame = ctk.CTkFrame(window, width=350, height=400, corner_radius=20, fg_color='#19181A')

            info_image = ctk.CTkImage(Image.open(r'Resources/taxi-fy-trans.png'), size=(250, 125))
            menu_close = ctk.CTkLabel(info_frame, image=info_image, text='', width=250, height=125)
            menu_close.place(relx=0.5, rely=0.155, anchor='center')

            info_textbox = ctk.CTkTextbox(info_frame, width=325, height=250, corner_radius=20, wrap='word',
                                          font=('Ariel', 15), state='normal')
            info_textbox.place(relx=0.5, rely=0.65, anchor='center')
            info_textbox.insert('0.0',
                                '-------------------Taxi-Fy Says-------------------: \n\nPick-Up address and Drop-Off address cannot be updated. \n\nWhat shall I do now? \n\nDont worry! \nJust cancel the booking and create a new booking with the correct Pick-Up and Drop-Off address.')
            info_textbox.configure(state='disabled')

        # shows all the bookings done by the current passenger
        def create_bookings_table_all():
            global bookings_frame_all
            nonlocal bookings_table_all

            id = account_info[0]
            columns, records = fetch_booking_info_all(id)

            bookings_frame_all = ctk.CTkFrame(window, width=1150, height=700, corner_radius=20, fg_color='#19181A')
            bookings_label = ctk.CTkLabel(bookings_frame_all, text='Y O U R   B O O K I N G S !', text_color='#e9896a')
            bookings_label.pack()

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

            bookings_table_all = CTkTable(master=bookings_frame_all, row=5, column=len(values[0]), values=values,
                                          header_color="#406080", wraplength=200, justify='left', width=110)
            bookings_table_all.pack(anchor='nw', padx=20, pady=(0, 20))

            return bookings_table_all

        # updates the booking table
        def update_table_all():
            # Clear the current table content
            nonlocal bookings_table_all
            if bookings_table_all:
                bookings_table_all.place_forget()  # Hide the table widget
                bookings_table_all.destroy()  # Destroy the table instance
                bookings_table_all = None

            # Fetch user data
            id = account_info[0]
            columns, records = fetch_booking_info_all(id)

            # Truncate long cell values and limit text width in cells
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

            # Insert new data into the table
            values = [columns] + compressed_records
            bookings_table_all = CTkTable(master=bookings_frame_all, row=len(values), column=len(values[0]),
                                          values=values,
                                          header_color="#406080", wraplength=200, justify='left', width=110)
            bookings_table_all.pack(anchor='nw', padx=20, pady=(0, 20))

            return bookings_table_all

        # update the booking function
        def update_bookings():
            global update_bookings_frame

            update_bookings_frame = ctk.CTkFrame(window, width=750, height=400, corner_radius=20, fg_color='#19181A')
            update_bookings_label = ctk.CTkLabel(update_bookings_frame,
                                                 text='M O D I F Y   Y O U R   B O O K I N G S !',
                                                 font=('Ariel', 14), text_color='#6b5b95')
            update_bookings_label.place(relx=0.5, rely=0.1, anchor='center')

            # clears the entry widgets
            def clear_widgets_update():
                booking_id_entry.delete(0, ctk.END)
                date_update_label.configure(text='')
                time_update_label.configure(text='')

            # update button function
            def send_update_request_fun():
                global pickup_date, pickup_time, booking_id

                passenger_id = account_info[0]

                if not all([pickup_date, pickup_time, booking_id, passenger_id]):
                    messagebox.showwarning('Invalid!', 'Please fill out all the information!')
                    return

                booking_request = send_update_request(pickup_date, pickup_time, booking_id, passenger_id)

                if booking_request:
                    messagebox.showinfo('Taxi-Fy says',
                                        'Booking Updated Successfully!, Please wait for Approval!')
                    clear_widgets_update()
                    update_table()

            # date and time selector in update bookings page
            def date_time_selector_update():

                def get_date_update(time):
                    global pickup_date, pickup_time, booking_id
                    pickup_date = date_picker.get_date()
                    pickup_time = "{}:{}".format(*time)
                    booking_id = booking_id_entry.get()
                    date_update_label.configure(text=pickup_date)
                    time_update_label.configure(text=pickup_time)
                    date_time_update_frame.place_forget()

                date_time_update_frame = ctk.CTkFrame(update_bookings_frame, width=300, height=400, corner_radius=20,
                                                      fg_color='#19181A')
                date_time_update_frame.place(relx=0.5, rely=0.5, anchor='center')

                todays_date = date.today()

                date_picker_label = ctk.CTkLabel(date_time_update_frame, text='Select Pickup Date: ')
                date_picker_label.place(relx=0.5, rely=0.1, anchor='center')

                date_picker = Calendar(date_time_update_frame, mindate=todays_date, date_pattern='yyyy-mm-dd')
                date_picker.place(relx=0.5, rely=0.4, anchor='center')

                time_picker_label = ctk.CTkLabel(date_time_update_frame, text='Select Pickup Time: ')
                time_picker_label.place(relx=0.5, rely=0.78, anchor='center')

                pickup_time_picker = SpinTimePickerOld(date_time_update_frame)
                pickup_time_picker.addAll(constants.HOURS24)
                pickup_time_picker.configureAll(bg='#4d4d4d', width=3, font=('Ariel', 12))
                pickup_time_picker.configure_separator(bg='#4d4d4d', fg='white')
                pickup_time_picker.place(relx=0.5, rely=0.84, anchor='center')

                date_picker_button = ctk.CTkButton(date_time_update_frame, text='Confirm',
                                                   command=lambda: get_date_update(pickup_time_picker.time()))
                date_picker_button.place(relx=0.5, rely=0.95, anchor='center')

            booking_id_label = ctk.CTkLabel(update_bookings_frame, text='Enter the Booking ID: ', font=('Ariel', 14))
            booking_id_label.place(relx=0.35, rely=0.3, anchor='center')

            booking_id_entry = ctk.CTkEntry(update_bookings_frame, width=200, height=30)
            booking_id_entry.place(relx=0.6, rely=0.3, anchor='center')

            select_date_time_btn_update = ctk.CTkButton(update_bookings_frame, text='Select New Date and Time',
                                                        command=date_time_selector_update, corner_radius=20)
            select_date_time_btn_update.place(relx=0.5, rely=0.45, anchor='center')

            date_udpate_frame = ctk.CTkFrame(update_bookings_frame, width=200, height=35, border_width=1,
                                             border_color='azure', fg_color='#19181A')
            date_udpate_frame.place(relx=0.6, rely=0.6, anchor='center')

            date_txt_update_label = ctk.CTkLabel(update_bookings_frame, text='New Pickup Date: ')
            date_txt_update_label.place(relx=0.35, rely=0.6, anchor='center')

            date_update_label = ctk.CTkLabel(date_udpate_frame, text='')
            date_update_label.place(relx=0.5, rely=0.5, anchor='center')

            time_update_frame = ctk.CTkFrame(update_bookings_frame, width=200, height=35, border_width=1,
                                             border_color='azure', fg_color='#19181A')
            time_update_frame.place(relx=0.6, rely=0.7, anchor='center')

            time_txt_update_label = ctk.CTkLabel(update_bookings_frame, text='New Pickup Time: ')
            time_txt_update_label.place(relx=0.35, rely=0.7, anchor='center')

            time_update_label = ctk.CTkLabel(time_update_frame, text='')
            time_update_label.place(relx=0.5, rely=0.5, anchor='center')

            send_update_request_btn = ctk.CTkButton(update_bookings_frame, width=200, height=30,
                                                    text='Update your booking',
                                                    command=send_update_request_fun)
            send_update_request_btn.place(relx=0.5, rely=0.9, anchor='center')

        # bookings table main
        def create_bookings_table():
            global bookings_frame
            nonlocal bookings_table

            id = account_info[0]
            columns, records = fetch_booking_info(id)

            bookings_frame = ctk.CTkFrame(window, width=1150, height=400, corner_radius=20, fg_color='#19181A')
            bookings_label = ctk.CTkLabel(bookings_frame, text='Y O U R   B O O K I N G S !', text_color='#e9896a')
            bookings_label.pack()

            num_empty_rows = 5 - len(records)
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

            bookings_table = CTkTable(master=bookings_frame, row=5, column=len(values[0]), values=values,
                                      header_color="#406080", wraplength=200, justify='left', width=110)
            bookings_table.pack(anchor='nw', padx=20, pady=(0, 20))

            return bookings_table

        # updates the booking table main
        def update_table():
            nonlocal bookings_table
            if bookings_table:
                bookings_table.place_forget()
                bookings_table.destroy()
                bookings_table = None

            id = account_info[0]
            columns, records = fetch_booking_info(id)

            num_empty_rows = 8 - len(records)
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
            bookings_table = CTkTable(master=bookings_frame, row=len(values), column=len(values[0]), values=values,
                                      header_color="#406080", wraplength=200, justify='left', width=110)
            bookings_table.pack(anchor='nw', padx=20, pady=(0, 20))

            return bookings_table

        # displays if there are any approved bookings of the current passenger
        def upcoming_trip_fun():
            global trip_info_frame, right_dashboard_frame, left_dashboard_frame, lower_dashboard_frame

            trip_info_frame = ctk.CTkFrame(window, width=1150, height=50, corner_radius=10, fg_color='#19181A')
            trip_info_label = ctk.CTkLabel(trip_info_frame, width=1100, height=45, text='', text_color='#ffcc66')
            trip_info_label.place(relx=0.5, rely=0.5, anchor='center')

            welcome_text = ctk.CTkLabel(bar_frame, text=f"Welcome to Taxi-Fy, {account_info[1]}!",
                                        font=('Harry Plain', 14))
            welcome_text.place(relx=0.5, rely=0.5, anchor='center')

            right_dashboard_frame = ctk.CTkFrame(window, width=565, height=300, corner_radius=20, fg_color='#19181A')
            right_dashboard_label = ctk.CTkLabel(right_dashboard_frame, text='T R I P   D E T A I L S',
                                                 text_color='#e74c3c')
            right_dashboard_label.place(relx=0.5, rely=0.1, anchor='center')

            left_dashboard_frame = ctk.CTkFrame(window, width=565, height=300, corner_radius=20, fg_color='#19181A')
            left_dashboard_label = ctk.CTkLabel(left_dashboard_frame, text='D R I V E R   D E T A I L S',
                                                text_color='#2ecc71')
            left_dashboard_label.place(relx=0.5, rely=0.1, anchor='center')

            lower_dashboard_frame = ctk.CTkFrame(window, width=1150, height=355, corner_radius=20, fg_color='#19181A')

            map_widget = tkintermapview.TkinterMapView(lower_dashboard_frame, width=1150, height=355, corner_radius=20)
            map_widget.place(relx=0.5, rely=0.5, anchor='center')
            map_widget.set_position(27.6839, 85.3186)
            map_widget.set_zoom(12)

            # --- Right Dashboard Frame ---

            pickup_address_frame = ctk.CTkFrame(right_dashboard_frame, border_width=1, border_color='gray', width=300,
                                                height=55,
                                                fg_color='#19181A')
            pickup_address_frame.place(relx=0.31, rely=0.3, anchor='center')

            pickup_address_txt = ctk.CTkLabel(pickup_address_frame, text='Pickup Address: ', text_color='gray',
                                              font=('Ariel', 12), height=10)
            pickup_address_txt.place(relx=0.2, rely=0.2, anchor='center')

            pickup_address_label = ctk.CTkLabel(pickup_address_frame, text="", font=('Ariel', 14), height=30, width=250)
            pickup_address_label.place(relx=0.07, rely=0.6, anchor='w')

            dropoff_address_frame = ctk.CTkFrame(right_dashboard_frame, border_width=1, border_color='gray', width=300,
                                                 height=55, fg_color='#19181A')
            dropoff_address_frame.place(relx=0.31, rely=0.5, anchor='center')

            dropoff_address_txt = ctk.CTkLabel(dropoff_address_frame, text='Drop-off Address: ', text_color='gray',
                                               height=10, font=('Ariel', 12))
            dropoff_address_txt.place(relx=0.2, rely=0.2, anchor='center')

            dropoff_address_label = ctk.CTkLabel(dropoff_address_frame, text="", height=30, font=('Ariel', 14),
                                                 width=250)
            dropoff_address_label.place(relx=0.07, rely=0.6, anchor='w')

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

            date_txt_label = ctk.CTkLabel(date_frame, text='Pickup Date: ', text_color='gray', height=10,
                                          font=('Ariel', 12))
            date_txt_label.place(relx=0.15, rely=0.2, anchor='center')

            date_label = ctk.CTkLabel(date_frame, text='', height=30, font=('Ariel', 14), width=150)
            date_label.place(relx=0.1, rely=0.6, anchor='w')

            time_frame = ctk.CTkFrame(right_dashboard_frame, width=200, height=55, border_width=1,
                                      border_color='gray', fg_color='#19181A')
            time_frame.place(relx=0.78, rely=0.7, anchor='center')

            time_txt_label = ctk.CTkLabel(time_frame, text='Pickup Time: ', text_color='gray', height=10,
                                          font=('Ariel', 12))
            time_txt_label.place(relx=0.25, rely=0.2, anchor='center')

            time_label = ctk.CTkLabel(time_frame, text='', height=30, font=('Ariel', 13), width=150)
            time_label.place(relx=0.1, rely=0.6, anchor='w')

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

            email_label = ctk.CTkLabel(email_frame, text="", font=('Ariel', 14), height=30, width=470)
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

            VehicleModel_frame = ctk.CTkFrame(left_dashboard_frame, border_width=1, border_color='gray', width=260,
                                              height=55, fg_color='#19181A')
            VehicleModel_frame.place(relx=0.265, rely=0.9, anchor='center')

            VehicleModel_txt = ctk.CTkLabel(VehicleModel_frame, text='VehicleModel', text_color='gray',
                                            font=('Ariel', 12), height=10)
            VehicleModel_txt.place(relx=0.2, rely=0.2, anchor='center')

            VehicleModel_label = ctk.CTkLabel(VehicleModel_frame, text="", font=('Ariel', 14), height=30, width=210)
            VehicleModel_label.place(relx=0.1, rely=0.6, anchor='w')

            Vehicle_Registration_frame = ctk.CTkFrame(left_dashboard_frame, width=260, height=55, border_width=1,
                                                      border_color='gray', fg_color='#19181A')
            Vehicle_Registration_frame.place(relx=0.74, rely=0.9, anchor='center')

            Vehicle_Registration_txt = ctk.CTkLabel(Vehicle_Registration_frame, text='Vehicle Reg. No.',
                                                    text_color='gray', height=10,
                                                    font=('Ariel', 12))
            Vehicle_Registration_txt.place(relx=0.2, rely=0.2, anchor='center')

            Vehicle_Registration_label = ctk.CTkLabel(Vehicle_Registration_frame, text='', height=30,
                                                      font=('Ariel', 14), width=210)
            Vehicle_Registration_label.place(relx=0.1, rely=0.6, anchor='w')

            # shows the trip information along with driver details in the labels and the map widget if the booking is approved
            def trip_info():
                global trip_details, pickup_marker, dropoff_marker

                trip_details = trip_information_passenger(account_info[0])

                if (trip_details != None):
                    pickup_location = geocoder.osm(trip_details[2])
                    dropoff_location = geocoder.osm(trip_details[3])

                    pickup_coordinates = pickup_location.latlng
                    dropoff_coordinates = dropoff_location.latlng

                    pickup_marker = map_widget.set_marker(pickup_coordinates[0], pickup_coordinates[1],
                                                          text='Pickup Location')
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
                    VehicleModel_label.configure(text=trip_details[20], anchor='w')
                    phone_number_label.configure(text=trip_details[18], anchor='w')
                    Vehicle_Registration_label.configure(text=trip_details[21], anchor='w')

                    trip_info_label.configure(
                        text='Y O U   T R I P   H A S   B E E N   C O N F I R M E D!  C H E C K   D E T A I L S   B E L O W !')

                else:
                    trip_info_label.configure(
                        text='N O   T R I P S   C O N F I R M E D! ! !')

            trip_info()

        # menu button toggle function
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
            add_button(0.5, 0.185, 'Y O U R     U P C O M I N G     T R I P', '#171617', '#25dae9', upcoming_trip)
            add_button(0.5, 0.245, 'Y O U R     B O O K I N G S', '#171617', '#e9896a', bookings_fun)
            add_button(0.5, 0.305, 'U P D A T E     B O O K I N G S', '#171617', '#6b5b95'
                       , update_bookings_fun)
            add_button(0.5, 0.365, 'C A N C E L     B O O K I N G S', '#171617', '#2ecc71'
                       , delete_bookings_fun)
            add_button(0.5, 0.425, 'P R O F I L E', '#171617', '#9b59b6', profile_toggle)
            add_button(0.5, 0.485, 'L O G   O U T', '#171617', '#e74c3c'
                       , log_out_function)

            return menu_frame

        # profile button toggle function
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

            add_button(0.5, 0.33, 'E D I T   P R O F I L E', '#171617', '#ffcc66', edit_profile_fun)
            # add_button(0.5, 0.39, 'A C T I V I T Y', '#19181A', '#25dae9', home_fun)
            add_button(0.5, 0.39, 'L O G   O U T', '#19181A', '#e74c3c', log_out_function)

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

        # edit profile button function in the profile
        def edit_profile_fun():
            global edit_profile_frame

            edit_profile_frame = ctk.CTkFrame(window, width=500, height=600, fg_color='#19181A')
            edit_profile_frame.place(relx=0.745, rely=0.5, anchor='e')

            edit_profile_label = ctk.CTkLabel(edit_profile_frame, text='E D I T    P R O F I L E')
            edit_profile_label.place(relx=0.5, rely=0.045, anchor='center')

            def show_password_fun():
                if show_password_var.get():
                    password_entry.configure(show='')
                    repeat_password_entry.configure(show='')

                else:
                    password_entry.configure(show='*')
                    repeat_password_entry.configure(show='*')

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

            def edit_profile_off_toggle():
                edit_profile_frame.place_forget()

            def edit_profile_function():
                first_name = edit_firstname_entry.get()
                last_name = lastname_entry.get()
                email_ = email_entry.get()
                gender_ = gender_value.get()
                age_value = int(age_slider_display.get())
                address_ = address_entry.get()
                phone_number = number_entry.get()
                payment_method_ = payment_method_cmbbox.get()
                password_ = password_entry.get()
                repeat_password_ = repeat_password_entry.get()

                if not all([first_name, last_name, email_, gender_, age_value, address_, phone_number, payment_method_,
                            password_]):
                    messagebox.showwarning('Invalid!', 'Please fill out all the information!')
                    return
                # validation rules.
                if '@' in email_ and '.com' in email_:
                    if age_value > 16 and age_value < 100:
                        if phone_number.isdigit() and len(phone_number) == 10:
                            if password_ == repeat_password_:
                                profile_edit = edit_profile(first_name, last_name, email_, gender_, age_value,
                                                            address_, phone_number,
                                                            payment_method_,
                                                            password_, account_info)

                                if profile_edit:
                                    messagebox.showinfo('Taxi-Fy says',
                                                        'Profile Updated Successfully! Please Login again!')
                                    bookings_frame.place_forget()
                                    bookings_frame_all.place_forget()
                                    update_bookings_frame.place_forget()
                                    delete_bookings_frame.place_forget()
                                    info_frame.place_forget()
                                    bar_frame.place_forget()
                                    profile_frame.place_forget()
                                    dashboard_frame.place_forget()
                                    second_dashboard_frame.place_forget()
                                    edit_profile_frame.place_forget()

                                    window_width = 1000
                                    window_height = 800

                                    # ----WINDOW APPEAR IN THE MIDDLE OF THE SCREEN----
                                    screen_width = window.winfo_screenwidth()
                                    screen_height = window.winfo_screenheight()
                                    x = (screen_width // 2) - (window_width // 2)
                                    y = (screen_height // 2) - (window_height // 2)
                                    window.geometry(f'{window_width}x{window_height}+{x}+{y}')
                                    window.configure(fg_color='#0a2135')

                                    welcome_label_1.place(relx=0.5, rely=0.03, anchor='center')
                                    logo_label.place(relx=0.5, rely=0.13, anchor='center')
                                    reg_login_frame.place(relx=0.5, rely=0.6, anchor='center')




                            else:
                                messagebox.showwarning('Invalid!', 'The passwords do not match!')

                        else:
                            messagebox.showwarning('Invalid!', 'Phone number is invalid!')

                    else:
                        messagebox.showwarning('Invalid!', 'Please enter an appropriate age!')

                else:
                    messagebox.showwarning('Invalid!', 'The email is not valid!')

            edit_profile_close_image = ctk.CTkImage(Image.open(r'Resources/close.png'), size=(40, 40))
            edit_profile_close = ctk.CTkButton(edit_profile_frame, image=edit_profile_close_image, text='',
                                               command=edit_profile_off_toggle,
                                               width=20, height=10, fg_color='#19181A', hover_color='#19181A')
            edit_profile_close.place(relx=0.9, rely=0.035, anchor='center')

            sign_up_frame = ctk.CTkScrollableFrame(edit_profile_frame, width=350, height=500, fg_color='#19181A')
            sign_up_frame.place(relx=0.56, rely=0.55, anchor='center')

            # edit_firstname
            edit_firstname_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2,
                                                border_color='gray',
                                                corner_radius=10)
            edit_firstname_frame.grid(row=1, column=1, stick='n', pady=5)

            edit_firstname = ctk.CTkLabel(edit_firstname_frame, text='First Name', text_color='gray',
                                          font=('Ariel', 12),
                                          height=10)
            edit_firstname.place(relx=0.035, rely=0.2, anchor='w')

            edit_firstname_entry_var = ctk.StringVar()

            edit_firstname_entry = ctk.CTkEntry(edit_firstname_frame, border_width=0, width=290, height=30,
                                                fg_color='#2b2b2b',
                                                font=('Verdana', 14), textvariable=edit_firstname_entry_var)
            edit_firstname_entry.place(relx=0.5, rely=0.6, anchor='center')

            # lastname
            lastname_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                          corner_radius=10)
            lastname_frame.grid(row=2, column=1, stick='n', pady=5)

            lastname_entry_var = ctk.StringVar()

            lastname = ctk.CTkLabel(lastname_frame, text='Last Name', text_color='gray', font=('Ariel', 12), height=10)
            lastname.place(relx=0.035, rely=0.2, anchor='w')

            lastname_entry = ctk.CTkEntry(lastname_frame, border_width=0, width=290, height=30, fg_color='#2b2b2b',
                                          font=('Verdana', 14), textvariable=lastname_entry_var)
            lastname_entry.place(relx=0.5, rely=0.6, anchor='center')

            # email
            email_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                       corner_radius=10)
            email_frame.grid(row=3, column=1, stick='n', pady=5)

            email_entry_var = ctk.StringVar()

            email = ctk.CTkLabel(email_frame, text='Email', text_color='gray', font=('Ariel', 12), height=10)
            email.place(relx=0.035, rely=0.2, anchor='w')

            email_entry = ctk.CTkEntry(email_frame, border_width=0, width=290, height=30, fg_color='#2b2b2b',
                                       font=('Verdana', 14), textvariable=email_entry_var)
            email_entry.place(relx=0.5, rely=0.6, anchor='center')

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
            address_entry_var = ctk.StringVar()

            address_entry = ctk.CTkEntry(address_frame, border_width=0, width=290, height=30, fg_color='#2b2b2b',
                                         font=('Verdana', 14), textvariable=address_entry_var)
            address_entry.place(relx=0.5, rely=0.6, anchor='center')

            # number
            number_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                        corner_radius=10)
            number_frame.grid(row=7, column=1, stick='n', pady=5)
            number = ctk.CTkLabel(number_frame, text='Phone number', text_color='gray', font=('Ariel', 12), height=10)
            number.place(relx=0.035, rely=0.2, anchor='w')

            # number entry
            number_entry_var = ctk.StringVar()
            number_entry = ctk.CTkEntry(number_frame, border_width=0, width=290, height=30, fg_color='#2b2b2b',
                                        font=('Verdana', 14), textvariable=number_entry_var)
            number_entry.place(relx=0.5, rely=0.6, anchor='center')

            # payment_method
            payment_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                         corner_radius=10)
            payment_frame.grid(row=8, column=1, stick='n', pady=5)

            # payment_method combobox
            payment_value = ctk.StringVar()
            payment_method_cmbbox = ctk.CTkComboBox(payment_frame, state='readonly', width=290, fg_color='#2b2b2b',
                                                    values=['Credit Card', 'E-Wallet', 'Cash'], border_width=1,
                                                    height=40, variable=payment_value,
                                                    dropdown_hover_color='#0a2135')
            payment_method_cmbbox.set('Select Payment Method:')
            payment_method_cmbbox.place(relx=0.5, rely=0.5, anchor='center')

            # password
            password_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2, border_color='gray',
                                          corner_radius=10)
            password_frame.grid(row=9, column=1, stick='n', pady=5)
            password = ctk.CTkLabel(password_frame, text='New Password', text_color='gray', font=('Ariel', 12),
                                    height=10)
            password.place(relx=0.035, rely=0.2, anchor='w')

            # password entry
            password_entry_var = ctk.StringVar()
            password_entry = ctk.CTkEntry(password_frame, border_width=0, width=290, height=30, fg_color='#2b2b2b',
                                          font=('Verdana', 14), textvariable=password_entry_var, show='*')
            password_entry.place(relx=0.5, rely=0.6, anchor='center')

            # repeat password
            repeat_password_frame = ctk.CTkFrame(sign_up_frame, width=300, height=55, border_width=2,
                                                 border_color='gray',
                                                 corner_radius=10)
            repeat_password_frame.grid(row=10, column=1, stick='n', pady=5)
            repeat_password = ctk.CTkLabel(repeat_password_frame, text='Re-enter Password', text_color='gray',
                                           font=('Ariel', 12), height=10)
            repeat_password.place(relx=0.035, rely=0.2, anchor='w')

            # repeat password entry
            repeat_password_entry_var = ctk.StringVar()
            repeat_password_entry = ctk.CTkEntry(repeat_password_frame, border_width=0, width=290, height=30,
                                                 fg_color='#2b2b2b',
                                                 font=('Verdana', 14), textvariable=repeat_password_entry_var, show='*')
            repeat_password_entry.place(relx=0.5, rely=0.6, anchor='center')

            # show password
            show_password_var = ctk.BooleanVar(value=False)
            show_password = ctk.CTkCheckBox(sign_up_frame, text='Show password', variable=show_password_var,
                                            command=show_password_fun, font=('Ariel', 12), border_color='gray',
                                            hover_color='#fffc04', corner_radius=20)
            show_password.grid(row=11, column=1, stick='e', pady=5)

            # submit button
            submit_btn = ctk.CTkButton(sign_up_frame, text='Submit', text_color='WHITE', width=120, fg_color='#0a2135',
                                       corner_radius=20, height=30, command=edit_profile_function)
            submit_btn.grid(row=13, column=1, stick='w', pady=5)

            edit_firstname_entry_var.set(account_info[1])
            lastname_entry_var.set(account_info[2])
            email_entry_var.set(account_info[3])
            gender_value.set(value=account_info[4])
            entry_var.set(account_info[5])
            address_entry_var.set(account_info[6])
            number_entry_var.set(account_info[7])
            payment_value.set(value=account_info[8])
            password_entry_var.set(account_info[9])
            repeat_password_entry_var.set(account_info[9])

            return edit_profile_frame

        # home button function
        def home_fun():
            bookings_frame.place_forget()
            bookings_frame_all.place_forget()
            update_bookings_frame.place_forget()
            delete_bookings_frame.place_forget()
            info_frame.place_forget()
            trip_info_frame.place_forget()
            right_dashboard_frame.place_forget()
            left_dashboard_frame.place_forget()
            lower_dashboard_frame.place_forget()
            dashboard_frame.place(relx=0.635, rely=0.525, anchor='center')
            second_dashboard_frame.place(relx=0.155, rely=0.525, anchor='center')

        # upcoming trip button function
        def upcoming_trip():
            bookings_frame.place_forget()
            bookings_frame_all.place_forget()
            update_bookings_frame.place_forget()
            delete_bookings_frame.place_forget()
            info_frame.place_forget()
            dashboard_frame.place_forget()
            second_dashboard_frame.place_forget()
            trip_info_frame.place(relx=0.5, rely=0.09, anchor='center')
            right_dashboard_frame.place(relx=0.74, rely=0.32, anchor='center')
            left_dashboard_frame.place(relx=0.26, rely=0.32, anchor='center')
            lower_dashboard_frame.place(relx=0.5, rely=0.75, anchor='center')

        # bookings button function
        def bookings_fun():
            dashboard_frame.place_forget()
            second_dashboard_frame.place_forget()
            update_bookings_frame.place_forget()
            delete_bookings_frame.place_forget()
            info_frame.place_forget()
            trip_info_frame.place_forget()
            right_dashboard_frame.place_forget()
            left_dashboard_frame.place_forget()
            lower_dashboard_frame.place_forget()
            update_table_all()
            bookings_frame_all.place(relx=0.5, rely=0.07, anchor='n')

        # update bookings button function
        def update_bookings_fun():
            bookings_frame_all.place_forget()
            dashboard_frame.place_forget()
            second_dashboard_frame.place_forget()
            delete_bookings_frame.place_forget()
            trip_info_frame.place_forget()
            right_dashboard_frame.place_forget()
            left_dashboard_frame.place_forget()
            lower_dashboard_frame.place_forget()
            update_table()
            bookings_frame.place(relx=0.5, rely=0.07, anchor='n')
            update_bookings_frame.place(relx=0.335, rely=0.475, anchor='n')
            info_frame.place(relx=0.82, rely=0.475, anchor='n')

        # cancel bookings button function
        def delete_bookings_fun():
            dashboard_frame.place_forget()
            bookings_frame_all.place_forget()
            second_dashboard_frame.place_forget()
            update_bookings_frame.place_forget()
            trip_info_frame.place_forget()
            right_dashboard_frame.place_forget()
            left_dashboard_frame.place_forget()
            lower_dashboard_frame.place_forget()
            info_frame.place(relx=0.82, rely=0.475, anchor='n')
            update_table()
            bookings_frame.place(relx=0.5, rely=0.07, anchor='n')
            delete_bookings_frame.place(relx=0.335, rely=0.475, anchor='n')

        # log out button function
        def log_out_function():
            logout = messagebox.askyesno('Taxi-Fy says', 'Do you really want to log out?')
            if logout:
                bookings_frame.place_forget()
                bookings_frame_all.place_forget()
                update_bookings_frame.place_forget()
                delete_bookings_frame.place_forget()
                info_frame.place_forget()
                dashboard_frame.place_forget()
                second_dashboard_frame.place_forget()
                bar_frame.place_forget()
                trip_info_frame.place_forget()
                right_dashboard_frame.place_forget()
                left_dashboard_frame.place_forget()
                lower_dashboard_frame.place_forget()

                try:
                    menu_frame.place_forget()
                except:
                    pass

                try:
                    profile_frame.place_forget()
                except:
                    pass

                try:
                    edit_profile_frame.place_forget()
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

                welcome_label_1.place(relx=0.5, rely=0.03, anchor='center')
                logo_label.place(relx=0.5, rely=0.13, anchor='center')
                reg_login_frame.place(relx=0.5, rely=0.6, anchor='center')

        # clears the label and widgets
        def clear_widgets():
            pickup_address_label.configure(text='')
            dropoff_address_label.configure(text='')
            distance_label.configure(text='')
            price_label.configure(text='')
            date_label.configure(text='')
            time_label.configure(text='')
            searchbar_entry.delete(0, ctk.END)
            searchbar_entry.insert(0, searchbar_text)
            map_widget.delete(pickup_marker[0])
            map_widget.delete(dropoff_marker[0])

        # date and time selector for booking a cab
        def date_time_selector():

            def get_date(time):
                global pickup_date, pickup_time
                pickup_date = date_picker.get_date()
                pickup_time = "{}:{}".format(*time)
                date_label.configure(text=pickup_date)
                time_label.configure(text=pickup_time)
                date_time_frame.place_forget()

            date_time_frame = ctk.CTkFrame(second_dashboard_frame, width=300, height=400, corner_radius=20,
                                           fg_color='#19181A')
            date_time_frame.place(relx=0.5, rely=0.5, anchor='center')

            todays_date = date.today()

            date_picker_label = ctk.CTkLabel(date_time_frame, text='Select Pickup Date: ')
            date_picker_label.place(relx=0.5, rely=0.1, anchor='center')

            date_picker = Calendar(date_time_frame, mindate=todays_date, date_pattern='yyyy-mm-dd')
            date_picker.place(relx=0.5, rely=0.4, anchor='center')

            time_picker_label = ctk.CTkLabel(date_time_frame, text='Select Pickup Time: ')
            time_picker_label.place(relx=0.5, rely=0.78, anchor='center')

            pickup_time_picker = SpinTimePickerOld(date_time_frame)
            pickup_time_picker.addAll(constants.HOURS24)
            pickup_time_picker.configureAll(bg='#4d4d4d', width=3, font=('Ariel', 12))
            pickup_time_picker.configure_separator(bg='#4d4d4d', fg='white')
            pickup_time_picker.place(relx=0.5, rely=0.84, anchor='center')

            date_picker_button = ctk.CTkButton(date_time_frame, text='Confirm',
                                               command=lambda: get_date(pickup_time_picker.time()))
            date_picker_button.place(relx=0.5, rely=0.95, anchor='center')

        # clear the search bar of the map
        def clear_searchbar_text(event):
            if searchbar_entry.get() == 'Search location......':
                searchbar_entry.delete(0, ctk.END)

        # search location function of the map
        def search_location():
            location = searchbar_entry.get()
            map_widget.set_address(location)
            map_widget.set_zoom(17)

        # get the pickup address
        def get_address_name(marker):
            if marker[0]:
                lat, lon = marker[0].position
                location = geocoder.osm([lat, lon], method='reverse')
                return location.address
            return None

        # adding a pickup marker function
        def add_pickup_marker(coordinates_tuple):
            global pickup_address
            lat, lon = coordinates_tuple
            if pickup_marker[0] is not None:
                map_widget.delete(pickup_marker[0])  # Remove the previous pickup marker
            pickup_marker[0] = map_widget.set_marker(lat, lon, text="Pickup Location")
            pickup_address = get_address_name(pickup_marker)
            pickup_address_limited = pickup_address[:55]
            if pickup_address_limited:
                pickup_address_label.configure(text=f"{pickup_address_limited}")
            else:
                pickup_address_label.configure(text="No drop-off location selected!")

        # adding a drop off marker function
        def add_dropoff_marker(coordinates_tuple):
            global dropoff_address
            lat, lon = coordinates_tuple
            if dropoff_marker[0] is not None:
                map_widget.delete(dropoff_marker[0])  # Remove the previous drop-off marker
            dropoff_marker[0] = map_widget.set_marker(lat, lon, text="Drop-off Location")
            dropoff_address = get_address_name(dropoff_marker)
            dropoff_address_limited = dropoff_address[:55]
            if dropoff_address_limited:
                dropoff_address_label.configure(text=f"{dropoff_address_limited}")
            else:
                dropoff_address_label.configure(text="No drop-off location selected!")

        # calculating the distance and fare
        def calculate_distance_and_fare():
            global distance, fare
            
            # Create SSL context with the CA certificates bundle from certifi
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            
            geolocator = Nominatim(user_agent="taxi_app", ssl_context=ssl_context)

            # Get coordinates (latitude and longitude) for pickup and drop-off locations
            pickup_location = get_address_name(pickup_marker)
            dropoff_location = get_address_name(dropoff_marker)

            try:
                pickup = geolocator.geocode(pickup_location)
                dropoff = geolocator.geocode(dropoff_location)

                # Check if both locations were successfully geocoded
                if pickup and dropoff:
                    # Calculate distance between pickup and drop-off locations
                    distance = geodesic((pickup.latitude, pickup.longitude),
                                        (dropoff.latitude, dropoff.longitude)).kilometers

                    fare = distance * 140
                    fare = int(fare)
                    distance = f"{distance:.2f}"

                    # Display the calculated distance and fare
                    distance_label.configure(text=f"{distance} km")
                    price_label.configure(text=f"Rs.{fare:.2f}")
                else:
                    distance_label.configure(text="Invalid location")
            except AttributeError as e:
                # Handle any attribute error or invalid input
                print("Error:", e)
                distance_label.configure(text="Invalid input")



        # send booking request button function
        def send_booking_request_fun():
            global pickup_date, pickup_time, pickup_address, dropoff_address, distance, fare

            passenger_id = account_info[0]

            if not all([passenger_id, pickup_address, dropoff_address, pickup_date, pickup_time, distance, fare]):
                messagebox.showwarning('Invalid!', 'Please fill out all the information!')
                return

            booking_request = send_booking_request(passenger_id, pickup_address, dropoff_address, pickup_date,
                                                   pickup_time, distance, fare)

            if booking_request:
                messagebox.showinfo('Taxi-Fy says',
                                    'Booking Request sent successfully!, Please check Your request history!')
                clear_widgets()

        map_widget.add_left_click_map_command(add_pickup_marker)
        map_widget.add_left_click_map_command(add_dropoff_marker)

        # widget for booking a cab
        pickup_button = ctk.CTkButton(dashboard_frame, text="Select Pickup Location",
                                      command=lambda: map_widget.add_left_click_map_command(add_pickup_marker))
        pickup_button.place(relx=0.25, rely=0.03, anchor='center')

        dropoff_button = ctk.CTkButton(dashboard_frame, text="Select Drop-off Location",
                                       command=lambda: map_widget.add_left_click_map_command(add_dropoff_marker))
        dropoff_button.place(relx=0.75, rely=0.03, anchor='center')

        pickup_address_frame = ctk.CTkFrame(dashboard_frame, border_width=1, border_color='azure', width=350, height=35,
                                            fg_color='#19181A')
        pickup_address_frame.place(relx=0.25, rely=0.08, anchor='center')

        pickup_address_label = ctk.CTkLabel(pickup_address_frame, text="")
        pickup_address_label.place(relx=0.5, rely=0.5, anchor='center')

        dropoff_address_frame = ctk.CTkFrame(dashboard_frame, border_width=1, border_color='azure', width=350,
                                             height=35, fg_color='#19181A')
        dropoff_address_frame.place(relx=0.75, rely=0.08, anchor='center')

        dropoff_address_label = ctk.CTkLabel(dropoff_address_frame, text="")
        dropoff_address_label.place(relx=0.5, rely=0.5, anchor='center')

        searchbar_text = 'Search location......'
        searchbar_entry = ctk.CTkEntry(dashboard_frame, width=600, height=30, border_width=1, border_color='azure')
        searchbar_entry.insert(0, searchbar_text)
        searchbar_entry.bind('<Button-1>', clear_searchbar_text)
        searchbar_entry.place(relx=0.42, rely=0.15, anchor='center')

        searchbar_button = ctk.CTkButton(dashboard_frame, text='Search', command=search_location)
        searchbar_button.place(relx=0.9, rely=0.15, anchor='center')

        welcome_picture = ctk.CTkImage(Image.open(r'Resources/taxi-fy-trans.png'), size=(200, 110))
        welcome_label = ctk.CTkLabel(second_dashboard_frame, width=150, height=20, image=welcome_picture, text='')
        welcome_label.place(relx=0.5, rely=0.1, anchor='center')

        calculate_button = ctk.CTkButton(second_dashboard_frame, text="Calculate Fare",
                                         command=calculate_distance_and_fare)
        calculate_button.place(relx=0.5, rely=0.25, anchor='center')

        distance_frame = ctk.CTkFrame(second_dashboard_frame, width=200, height=35, border_width=1,
                                      border_color='azure', fg_color='#19181A')
        distance_frame.place(relx=0.5, rely=0.31, anchor='center')

        distance_txt_label = ctk.CTkLabel(distance_frame, text='Distance: ')
        distance_txt_label.place(relx=0.25, rely=0.5, anchor='center')

        distance_label = ctk.CTkLabel(distance_frame, text='')
        distance_label.place(relx=0.75, rely=0.5, anchor='center')

        price_frame = ctk.CTkFrame(second_dashboard_frame, width=200, height=35, border_width=1,
                                   border_color='azure', fg_color='#19181A')
        price_frame.place(relx=0.5, rely=0.37, anchor='center')

        price_txt_label = ctk.CTkLabel(price_frame, text='Fare: ')
        price_txt_label.place(relx=0.25, rely=0.5, anchor='center')

        price_label = ctk.CTkLabel(price_frame, text='')
        price_label.place(relx=0.75, rely=0.5, anchor='center')

        select_date_time_btn = ctk.CTkButton(second_dashboard_frame, text='Select Date and Time',
                                             command=date_time_selector)
        select_date_time_btn.place(relx=0.5, rely=0.5, anchor='center')

        date_frame = ctk.CTkFrame(second_dashboard_frame, width=200, height=35, border_width=1,
                                  border_color='azure', fg_color='#19181A')
        date_frame.place(relx=0.5, rely=0.56, anchor='center')

        date_txt_label = ctk.CTkLabel(date_frame, text='Pickup Date: ')
        date_txt_label.place(relx=0.25, rely=0.5, anchor='center')

        date_label = ctk.CTkLabel(date_frame, text='')
        date_label.place(relx=0.75, rely=0.5, anchor='center')

        time_frame = ctk.CTkFrame(second_dashboard_frame, width=200, height=35, border_width=1,
                                  border_color='azure', fg_color='#19181A')
        time_frame.place(relx=0.5, rely=0.62, anchor='center')

        time_txt_label = ctk.CTkLabel(time_frame, text='Pickup Time: ')
        time_txt_label.place(relx=0.25, rely=0.5, anchor='center')

        time_label = ctk.CTkLabel(time_frame, text='')
        time_label.place(relx=0.75, rely=0.5, anchor='center')

        send_booking_request_btn = ctk.CTkButton(second_dashboard_frame, width=200, height=30,
                                                 text='Send Booking Request', command=send_booking_request_fun)
        send_booking_request_btn.place(relx=0.5, rely=0.9, anchor='center')

        menu_open_image = ctk.CTkImage(Image.open(r'Resources/open.png'), size=(40, 30))
        menu_open = ctk.CTkButton(bar_frame, image=menu_open_image, text='', command=menu_toggle, width=20, height=10,
                                  fg_color='#19181A', hover_color='#19181A')
        menu_open.place(relx=0.025, rely=0.5, anchor='center')

        profile_open_image = ctk.CTkImage(Image.open(r'Resources/profile.png'), size=(40, 30))
        profile_open = ctk.CTkButton(bar_frame, image=profile_open_image, text='', command=profile_toggle, width=20,
                                     height=10, fg_color='#19181A', hover_color='#19181A')
        profile_open.place(relx=0.975, rely=0.5, anchor='center')

        # functions to be working on the background
        create_bookings_table()
        create_bookings_table_all()
        info_fun()
        update_bookings()
        delete_bookings()
        upcoming_trip_fun()

    # bar frame consisting the menu icon and profile icon
    bar_frame = ctk.CTkFrame(window, width=1200, height=40, corner_radius=10, fg_color='#19181A')
    bar_frame.place(relx=0.5, rely=0.025, anchor='center')

    welcome_text = ctk.CTkLabel(bar_frame,
                                text=f"Welcome to Taxi-Fy, {account_info[1]}!")  # Assuming name is at index 1
    welcome_text.place(relx=0.5, rely=0.5, anchor='center')

    dashboard()
