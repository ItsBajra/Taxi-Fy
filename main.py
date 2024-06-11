# ---- IMPORTING LIBRARIES ----
import customtkinter as ctk
from PIL import Image

from Backend.admin import admin_class
from Backend.passenger import passenger_class
from Backend.driver import driver_class

# main class
class mainGUI():
    def __init__(self):
        # ----CREATING WINDOW----
        self.window = window
        self.window.title('Taxi-Fy')
        self.window.resizable(True, True)
        window_width = 800
        window_height = 800

        # ----WINDOW APPEAR IN THE MIDDLE OF THE SCREEN----
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.window.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # ----BUTTON HOVER FUNCTIONS ----

        def on_enter(event, widget):
            widget.configure(text_color='#fffc04', border_color='#fffc04')

        def on_leave(event, widget):
            widget.configure(text_color='WHITE', border_color='WHITE')

        # ----BUTTON FUNCTIONS----

        def on_click_get_started():
            first_frame.place_forget()
            second_frame.place(relx=0.5, rely=0.75, anchor='center')

        def frame_close_passenger(window):
            bg_label.place_forget()
            first_frame.place_forget()
            second_frame.place_forget()
            passenger_class(window, bg_label, second_frame)

        def frame_close_driver(window):
            bg_label.place_forget()
            first_frame.place_forget()
            second_frame.place_forget()
            driver_class(window, bg_label, second_frame)

        def frame_close_admin(window):
            bg_label.place_forget()
            first_frame.place_forget()
            second_frame.place_forget()
            admin_class(window, bg_label, second_frame)

        # ----ADDING THE BACKGROUND PICTURE----
        bg_picture = ctk.CTkImage(Image.open('Resources/main-bg.png'), size=(800, 800))
        bg_label = ctk.CTkLabel(self.window, width=800, height=600, image=bg_picture, text='')
        bg_label.place(relx=0.5, rely=0.45, anchor='center')

        # ----FIRST FRAME----
        first_frame = ctk.CTkFrame(self.window, width=800, height=200, fg_color='#0a2135', )
        first_frame.place(relx=0.5, rely=0.75, anchor='center')

        # --GET STARTED BUTTON--
        get_started_button = ctk.CTkButton(first_frame, command=on_click_get_started, text='Get Started',
                                           text_color='WHITE', width=100, height=40, border_width=2,
                                           fg_color='#0a2135', border_color='WHITE')
        get_started_button.bind('<Enter>', lambda event: on_enter(event, get_started_button))
        get_started_button.bind('<Leave>', lambda event: on_leave(event, get_started_button))
        get_started_button.place(x=400, y=100, anchor='center')

        # ----SECOND FRAME----
        second_frame = ctk.CTkFrame(self.window, width=800, height=200, fg_color='#0a2135')

        # --PASSENGER BUTTON--
        passenger_button = ctk.CTkButton(second_frame, command=lambda: frame_close_passenger(window),
                                         text='Passenger', text_color='WHITE', width=100, height=40, border_width=2,
                                         fg_color='#0a2135', border_color='WHITE')
        passenger_button.bind('<Enter>', lambda event: on_enter(event, passenger_button))
        passenger_button.bind('<Leave>', lambda event: on_leave(event, passenger_button))
        passenger_button.place(x=290, y=100, anchor='center')

        # --DRIVER BUTTON--
        driver_button = ctk.CTkButton(second_frame, command=lambda: frame_close_driver(window), text='Driver',
                                      text_color='WHITE', width=100, height=40, border_width=2, fg_color='#0a2135',
                                      border_color='WHITE')
        driver_button.bind('<Enter>', lambda event: on_enter(event, driver_button))
        driver_button.bind('<Leave>', lambda event: on_leave(event, driver_button))
        driver_button.place(x=400, y=100, anchor='center')

        # --ADMIN BUTTON--
        admin_button = ctk.CTkButton(second_frame, command=lambda: frame_close_admin(window), text='Admin',
                                     text_color='WHITE', width=100, height=40,
                                     border_width=2, fg_color='#0a2135', border_color='WHITE')
        admin_button.bind('<Enter>', lambda event: on_enter(event, admin_button))
        admin_button.bind('<Leave>', lambda event: on_leave(event, admin_button))
        admin_button.place(x=510, y=100, anchor='center')

# ---MAIN LOOP---
if __name__ == '__main__':
    window = ctk.CTk(fg_color='#0a2135')
    mainGUI()
    window.mainloop()
