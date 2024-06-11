import sys

from .dbconnection import Connect


# passenger login operation
def login_passenger(email, password):
    conn = None
    sql = """SELECT * FROM Passenger_Accounts WHERE email=%s AND password=%s"""
    values = (email, password)
    account_info = None

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        account_info = cursor.fetchone()
        cursor.close()
        conn.close()

    except:
        print('Error', sys.exc_info())

    finally:
        del values, sql, conn
        return account_info


# register passenger operation
def register_passenger(first_name, last_name, email, gender, age, address, phone_number, payment_method, password):
    conn = None
    sql = """ INSERT INTO Passenger_Accounts (Firstname, LastName, Email, Gender, Age, Address, PhoneNumber,
              PaymentMethod, Password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """
    values = (first_name, last_name, email, gender, age, address, phone_number, payment_method, password)

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True  # Return True if registration is successful

    except Exception as e:
        print('Error:', e)
        return False  # Return False if an error occurred during registration

    finally:
        del values, sql, conn


# send booking request operation
def send_booking_request(passenger_id, pickup_address, dropoff_address, pickup_date,
                         pickup_time, distance, fare):
    conn = None
    sql = """ INSERT INTO Booking_Requests (Passenger_ID, Pickup_Address, Dropoff_Address, Pickup_Date,
                                            Pickup_Time, Distance, Amount, Approval)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pending') """
    values = (passenger_id, pickup_address, dropoff_address, pickup_date, pickup_time, distance, fare)

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True  # Return True if registration is successful

    except Exception as e:
        print('Error:', e)
        return False  # Return False if an error occurred during registration

    finally:
        del values, sql, conn


# get booking information operation
def fetch_booking_info(id):
    conn = Connect()
    cursor = conn.cursor()

    query = """
            SELECT 
                BR.Booking_ID, 
                BR.Pickup_Address, 
                BR.Dropoff_Address, 
                BR.Pickup_Date, 
                BR.Pickup_Time,
                BR.Distance, 
                BR.Amount, 
                BR.Approval, 
                CONCAT(DA.FirstName, ' ', DA.LastName) AS DriverName,
                BR.Trip_Status
            FROM 
                Booking_Requests BR
            LEFT JOIN 
                Driver_Accounts DA ON BR.Assigned_DriverID = DA.ID
            WHERE 
                BR.Passenger_ID = %s
            ORDER BY 
                BR.Booking_ID DESC 
            LIMIT 8
        """

    cursor.execute(query, (id,))
    records = cursor.fetchall()

    conn.close()
    columns = [col[0] for col in cursor.description]
    return columns, records


# get all the booking information
def fetch_booking_info_all(id):
    conn = Connect()
    cursor = conn.cursor()

    query = """
            SELECT 
                BR.Booking_ID, 
                BR.Pickup_Address, 
                BR.Dropoff_Address, 
                BR.Pickup_Date, 
                BR.Pickup_Time,
                BR.Distance, 
                BR.Amount, 
                BR.Approval, 
                CONCAT(DA.FirstName, ' ', DA.LastName) AS DriverName,
                BR.Trip_Status
            FROM 
                Booking_Requests BR
            LEFT JOIN 
                Driver_Accounts DA ON BR.Assigned_DriverID = DA.ID
            WHERE 
                BR.Passenger_ID = %s
            ORDER BY 
                BR.Booking_ID DESC 
            LIMIT 16
        """

    cursor.execute(query, (id,))
    records = cursor.fetchall()

    conn.close()
    columns = [col[0] for col in cursor.description]
    return columns, records


# update current booking function
def send_update_request(pickup_date, pickup_time, booking_id, passenger_id):
    conn = None

    sql = """UPDATE Booking_Requests SET Pickup_Date = %s, Pickup_Time = %s 
                WHERE Booking_ID = %s AND Passenger_ID = %s"""
    values = (pickup_date, pickup_time, booking_id, passenger_id,)

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True  # Return True if update is successful

    except Exception as e:
        print('Error:', e)
        return False  # Return False if an error occurred during updating

    finally:
        del values, sql, conn


# cancel a booking function
def send_delete_request(booking_id, passenger_id):
    conn = None

    sql = """DELETE FROM Booking_Requests WHERE Booking_ID = %s AND Passenger_ID = %s"""
    values = (booking_id, passenger_id,)

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True  # Return True if update is successful

    except Exception as e:
        print('Error:', e)
        return False  # Return False if an error occurred during updating

    finally:
        del values, sql, conn


# passenger edit profile function
def edit_profile(first_name, last_name, email, gender, age, address, phone_number, payment_method, password,
                 account_info):
    conn = None
    passenger_id = account_info[0]

    sql = "UPDATE Passenger_Accounts SET FirstName = %s, LastName = %s, Email = %s, Gender = %s, Age = %s, Address = %s, PhoneNumber = %s,  PaymentMethod = %s, Password = %s WHERE ID = %s "

    values = (first_name, last_name, email, gender, age, address, phone_number, payment_method, password, passenger_id)

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True  # Return True if update is successful

    except Exception as e:
        print('Error:', e)
        return False  # Return False if an error occurred during updating

    finally:
        del conn


# register driver function
def register_driver(first_name, last_name, email, gender, age, address, phone_number, licensenumber, vehiclemodel,
                    vehicleregistration, password):
    conn = None
    sql = """ INSERT INTO Driver_Accounts (Firstname, LastName, Email, Gender, Age, Address, PhoneNumber,
              LicenseNumber, VehicleModel, VehicleRegistrationNumber, Password, Verification, Status) VALUES 
              (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    values = (
        first_name, last_name, email, gender, age, address, phone_number, licensenumber, vehiclemodel,
        vehicleregistration,
        password, 'Pending', 'Pending')

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True  # Return True if registration is successful

    except Exception as e:
        print('Error:', e)
        return False  # Return False if an error occurred during registration

    finally:
        del values, sql, conn


# login driver function
def login_driver(email, password):
    conn = None
    sql = """SELECT * FROM Driver_Accounts WHERE email=%s AND password=%s"""
    values = (email, password)
    account_info = None

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        account_info = cursor.fetchone()
        cursor.close()
        conn.close()

    except:
        print('Error', sys.exc_info())

    finally:
        del values, sql, conn
        return account_info


# trip information for driver operation
def trip_information(DriverID):
    conn = None
    sql = """SELECT Booking_Requests.*, Passenger_Accounts.* FROM Booking_Requests 
            JOIN Passenger_Accounts ON Booking_Requests.Passenger_ID = Passenger_Accounts.ID 
            WHERE Booking_Requests.Assigned_DriverID = %s  AND Booking_Requests.Trip_Status = 'Upcoming' LIMIT 1"""
    values = (DriverID,)
    trip_info = None

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        trip_info = cursor.fetchone()
        cursor.close()
        conn.close()

    except:
        print('Error', sys.exc_info())

    finally:
        del values, sql, conn
        return trip_info


# complete the trip operation
def complete_trip(bookingid, driverid):
    conn = None
    sql = "UPDATE Booking_Requests SET Trip_Status = 'Completed' WHERE Booking_ID = %s AND Assigned_DriverID = %s AND Trip_Status = 'Upcoming' "
    values = (bookingid, driverid,)

    sql2 = """UPDATE Driver_Accounts SET Status = 'Idle' WHERE ID = %s"""
    values2 = (driverid,)

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor2 = conn.cursor()
        cursor.execute(sql, values, )
        cursor2.execute(sql2, values2, )
        conn.commit()
        cursor.close()
        cursor2.close()
        conn.close()
        return True  # Return True if update is successful

    except Exception as e:
        print('Error:', e)
        return False  # Return False if an error occurred during updating

    finally:
        del conn


# get the trip history of the driver operation
def fetch_trip_info_all(id):
    conn = Connect()
    cursor = conn.cursor()

    columns_to_fetch = ['Booking_ID', 'Pickup_Address', 'Dropoff_Address', 'Pickup_Date', 'Pickup_Time', 'Distance',
                        'Amount', 'Approval', 'Trip_Status', 'FirstName', 'PhoneNumber', 'PaymentMethod']
    sql = f"""
        SELECT {', '.join(columns_to_fetch)}
        FROM Booking_Requests
        JOIN Passenger_Accounts ON Booking_Requests.Passenger_ID = Passenger_Accounts.ID
        WHERE Booking_Requests.Assigned_DriverID = %s
        AND Booking_Requests.Trip_Status = 'Completed'
        ORDER BY Booking_ID DESC LIMIT 22
    """
    values = (id,)

    cursor.execute(sql, values)
    records = cursor.fetchall()

    conn.close()
    return columns_to_fetch, records


# admin login operation
def login_admin(email, password):
    conn = None
    sql = """SELECT * FROM Admin_Accounts WHERE email=%s AND password=%s"""
    values = (email, password)
    account_info = None

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        account_info = cursor.fetchone()
        cursor.close()
        conn.close()

    except:
        print('Error', sys.exc_info())

    finally:
        del values, sql, conn
        return account_info


# count the total new booking requests operation
def new_booking_requests():
    conn = None
    sql = """SELECT COUNT(*) FROM Booking_requests WHERE Approval = 'Pending'"""
    count = None

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()
        cursor.close()
        conn.close()

    except:
        print('Error', sys.exc_info())

    finally:
        del sql, conn
        return count


# count the total available driver operation
def available_drivers():
    conn = None
    sql = """SELECT COUNT(*) FROM Driver_Accounts WHERE Status = 'Idle'"""
    count = None

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()
        cursor.close()
        conn.close()

    except:
        print('Error', sys.exc_info())

    finally:
        del sql, conn
        return count


# count the total completed trip operation
def completed_trips():
    conn = None
    sql = """SELECT COUNT(*) FROM Booking_Requests WHERE Trip_Status = 'Completed'"""
    count = None

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()
        cursor.close()
        conn.close()

    except:
        print('Error', sys.exc_info())

    finally:
        del sql, conn
        return count


# count the total number of passenger operation
def total_passengers():
    conn = None
    sql = """SELECT COUNT(*) FROM Passenger_Accounts"""
    count = None

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()
        cursor.close()
        conn.close()

    except:
        print('Error', sys.exc_info())

    finally:
        del sql, conn
        return count


# count the total number of new driver request function
def new_drivers_requests():
    conn = None
    sql = """SELECT COUNT(*) FROM Driver_Accounts WHERE Verification = 'Pending'"""
    count = None

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        count = cursor.fetchone()
        cursor.close()
        conn.close()

    except:
        print('Error', sys.exc_info())

    finally:
        del sql, conn
        return count


# get new bookings information
def fetch_new_booking_main_info():
    conn = Connect()
    cursor = conn.cursor()

    columns_to_fetch = ['Booking_ID', 'Pickup_Address', 'Dropoff_Address', 'Pickup_Date', 'Pickup_Time', 'Distance',
                        'Amount']
    sql = (f"SELECT {', '.join(columns_to_fetch)} FROM Booking_Requests WHERE Approval = 'Pending' "
           f"ORDER BY Booking_ID LIMIT 14")

    cursor.execute(sql)
    records = cursor.fetchall()

    conn.close()
    return columns_to_fetch, records


# get available drivers info operation
def fetch_available_drivers_main_info():
    conn = Connect()
    cursor = conn.cursor()

    columns_to_fetch = ['ID', 'FirstName', 'LastName', 'PhoneNumber', 'VehicleModel']
    sql = (f"SELECT {', '.join(columns_to_fetch)} FROM Driver_Accounts "
           f"WHERE Verification = 'Verified' AND Status = 'Idle' ORDER BY ID LIMIT 14")

    cursor.execute(sql)
    records = cursor.fetchall()

    conn.close()
    return columns_to_fetch, records


# get trip information
def trip_information_passenger(id):
    conn = None
    sql = """SELECT Booking_Requests.*, Driver_Accounts.* FROM Booking_Requests 
            JOIN Driver_Accounts ON Booking_Requests.Assigned_DriverID = Driver_Accounts.ID 
            WHERE Booking_Requests.Passenger_ID = %s AND Booking_Requests.Trip_Status = 'Upcoming' 
            ORDER BY Booking_Requests.Booking_ID DESC LIMIT 1;"""
    values = (id,)
    trip_info = None

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        trip_info = cursor.fetchone()
        cursor.close()
        conn.close()

    except:
        print('Error', sys.exc_info())

    finally:
        del values, sql, conn
        return trip_info


# get new booking request with limitation
def fetch_new_bookings():
    conn = Connect()
    cursor = conn.cursor()

    columns_to_fetch = ['Booking_ID', 'Pickup_Address', 'Dropoff_Address', 'Pickup_Date', 'Pickup_Time', 'Distance',
                        'Amount', 'Passenger_ID', 'FirstName', 'Age', 'PaymentMethod', 'Assigned_DriverID', 'Approval']
    sql = """SELECT Booking_Requests.Booking_ID, 
            Booking_Requests.Pickup_Address, 
            Booking_Requests.Dropoff_Address, 
            Booking_Requests.Pickup_Date, 
            Booking_Requests.Pickup_Time, 
            Booking_Requests.Distance, 
            Booking_Requests.Amount, 
            Booking_Requests.Passenger_ID, 
            Passenger_Accounts.FirstName, 
            Passenger_Accounts.Age, 
            passenger_Accounts.PaymentMethod, 
            Booking_Requests.Assigned_DriverID, 
            Booking_Requests.Approval
            FROM Booking_Requests 
            JOIN Passenger_Accounts ON Booking_Requests.Passenger_ID = Passenger_Accounts.ID 
            WHERE Booking_Requests.Approval = 'Pending'
            ORDER BY Booking_Requests.Booking_ID DESC 
            LIMIT 5"""

    cursor.execute(sql)
    records = cursor.fetchall()

    conn.close()
    return columns_to_fetch, records


# approve booking request and assign driver operation
def approve_booking_request(bookingID, driverID):
    conn = None

    sql = """UPDATE Booking_Requests SET Assigned_DriverID = %s, Approval = 'Approved', Trip_Status = 'Upcoming' 
            WHERE Booking_ID = %s"""
    values = (driverID, bookingID,)

    sql2 = """UPDATE Driver_Accounts SET STATUS = 'Assigned' WHERE ID = %s"""
    values2 = (driverID,)

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor2 = conn.cursor()
        cursor.execute(sql, values, )
        cursor2.execute(sql2, values2, )
        conn.commit()
        cursor.close()
        cursor2.close()
        conn.close()
        return True  # Return True if update is successful

    except Exception as e:
        print('Error:', e)
        return False  # Return False if an error occurred during updating

    finally:
        del values, sql, conn


# reject booking request
def reject_booking_request(bookingID):
    conn = None

    sql = """UPDATE Booking_Requests SET Approval = 'Rejected'
            WHERE Booking_ID = %s"""
    values = (bookingID,)

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor2 = conn.cursor()
        cursor.execute(sql, values, )
        conn.commit()
        cursor.close()
        cursor2.close()
        conn.close()
        return True  # Return True if update is successful

    except Exception as e:
        print('Error:', e)
        return False  # Return False if an error occurred during updating

    finally:
        del values, sql, conn


# approve new driver registration operation
def approve_driver_request(driverID):
    conn = None

    sql = """UPDATE Driver_Accounts SET Verification = 'Verified', Status = 'Idle'
                WHERE ID = %s"""
    values = (driverID,)

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values, )
        conn.commit()
        cursor.close()
        conn.close()
        return True  # Return True if update is successful

    except Exception as e:
        print('Error:', e)
        return False  # Return False if an error occurred during updating

    finally:
        del values, sql, conn


# reject driver request
def reject_driver_request(driverID):
    conn = None

    sql = """UPDATE Driver_Accounts SET Verification = 'Rejected'
                WHERE ID = %s"""
    values = (driverID,)

    try:
        conn = Connect()
        cursor = conn.cursor()
        cursor.execute(sql, values, )
        conn.commit()
        cursor.close()
        conn.close()
        return True  # Return True if update is successful

    except Exception as e:
        print('Error:', e)
        return False  # Return False if an error occurred during updating

    finally:
        del values, sql, conn


# get new drivers request operation
def fetch_new_drivers():
    conn = Connect()
    cursor = conn.cursor()

    columns_to_fetch = ['ID', 'FirstName', 'LastName', 'Email', 'Gender', 'Age',
                        'Address', 'PhoneNumber', 'LicenseNumber', 'VehicleModel', 'Vehicle Reg No.', 'Password',
                        'Verification', 'Status']
    sql = """SELECT * FROM Driver_Accounts WHERE Verification = 'Pending'"""

    cursor.execute(sql)
    records = cursor.fetchall()

    conn.close()
    return columns_to_fetch, records


# view all the bookings operation
def fetch_all_bookings():
    conn = Connect()
    cursor = conn.cursor()

    columns_to_fetch = ['BookingID', 'PassengerID', 'Pickup_Address', 'Dropoff_Address', 'Pickup_Date', 'Pickup_Time',
                        'Distance', 'Amount', 'Approval', 'Assigned_DriverID', 'Trip_Status']
    sql = """SELECT * FROM Booking_Requests"""

    cursor.execute(sql)
    records = cursor.fetchall()

    conn.close()
    return columns_to_fetch, records


# view all the drivers operation
def fetch_all_drivers():
    conn = Connect()
    cursor = conn.cursor()

    columns_to_fetch = ['ID', 'FirstName', 'LastName', 'Email', 'Gender', 'Age',
                        'Address', 'PhoneNumber', 'LicenseNumber', 'VehicleModel', 'Vehicle Reg. No.', 'Password',
                        'Verification', 'Status']
    sql = """SELECT * FROM Driver_Accounts"""

    cursor.execute(sql)
    records = cursor.fetchall()

    conn.close()
    return columns_to_fetch, records


# view all the passengers operation
def fetch_all_passengers():
    conn = Connect()
    cursor = conn.cursor()

    columns_to_fetch = ['ID', 'FirstName', 'LastName', 'Email', 'Gender', 'Age',
                        'Address', 'PhoneNumber', 'PaymentMethod', 'Password']
    sql = """SELECT * FROM Passenger_Accounts"""

    cursor.execute(sql)
    records = cursor.fetchall()

    conn.close()
    return columns_to_fetch, records
