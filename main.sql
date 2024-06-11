-- CREATING THE DATABASE --

CREATE DATABASE Assignment2;

USE Assignment2;

-- DROP TABLE Passenger_Accounts;


-- CREATING THE PASSENGER ACCOUNTS TABLE --

CREATE TABLE Passenger_Accounts (
	ID INT PRIMARY KEY AUTO_INCREMENT, 
    FirstName VARCHAR(30) NOT NULL, 
    LastName VARCHAR(30) NOT NULL, 
    Email VARCHAR(50) NOT NULL, 
    Gender VARCHAR(10) NOT NULL,
    Age INT(3) NOT NULL, 
    Address VARCHAR(50) NOT NULL, 
    PhoneNumber VARCHAR(10) NOT NULL, 
    PaymentMethod VARCHAR(30) NOT NULL, 
    Password VARCHAR(50) NOT NULL
);

-- SELECT * FROM Passenger_Accounts;

-- Describe passenger_Accounts;


-- CREATING DRIVER ACCOUNTS TABLE --

CREATE TABLE Driver_Accounts (
	ID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(30) NOT NULL, 
    LastName VARCHAR(30) NOT NULL, 
    Email VARCHAR(50) NOT NULL,
    Gender VARCHAR(10) NOT NULL,
    Age INT(3) NOT NULL,
    Address VARCHAR(50) NOT NULL, 
    PhoneNumber VARCHAR(10) NOT NULL,
    LicenseNumber VARCHAR(30) NOT NULL,
    VehicleModel VARCHAR(50) NOT NULL,
    VehicleRegistrationNumber VARCHAR(30) NOT NULL,
    Password VARCHAR(50) NOT NULL,
    Verification VARCHAR(10) NOT NULL, 
    Status VARCHAR(10) NOT NULL
);

-- Select * from Driver_Accounts;

-- Drop table Driver_Accounts;


-- CREATING BOOKING REQUESTS TABLE --

CREATE TABLE Booking_Requests (
	Booking_ID INT PRIMARY KEY AUTO_INCREMENT,
    Passenger_ID INT(10) NOT NULL,
    Pickup_Address VARCHAR(255) NOT NULL,
    Dropoff_Address VARCHAR(255) NOT NULL,
    Pickup_Date DATE NOT NULL,
    Pickup_Time VARCHAR(5) NOT NULL,
    Distance FLOAT NOT NULL,
    Amount INT(10) NOT NULL,
    Approval VARCHAR(10) NOT NULL,
    Assigned_DriverID INT (10) NULL,
    Trip_Status VARCHAR(10) NULL,
    FOREIGN KEY (Passenger_ID) REFERENCES Passenger_Accounts(ID),
    FOREIGN KEY (Assigned_DriverID) REFERENCES Driver_Accounts(ID)
);

-- DROP table Booking_Requests;
-- SELECT * FROM Booking_Requests;
-- desc Booking_Requests;


-- CREATING ADMIN ACCOUNT TABLE --

CREATE TABLE Admin_Accounts (
	Admin_ID INT PRIMARY KEY AUTO_INCREMENT,
    Email VARCHAR(255) NOT NULL	,
    Password VARCHAR(255) NOT NULL
);

-- INSERTING ADMIN DETAILS IN THE ADMIN TABLE--
INSERT INTO Admin_Accounts (Email, Password) VALUES ('admin@admin.com', 'admin');

-- DROP TABLE Admin_Accounts;
-- SELECT * FROM Admin_Accounts;
-- DROP DATABASE Assignment2;

-- SOME SQL QUERYS I USED IN MY APPLICATION --

-- SELECT Booking_Requests.*, Driver_Accounts.* FROM Booking_Requests JOIN Driver_Accounts ON Booking_Requests.Assigned_DriverID = Driver_Accounts.ID WHERE Booking_Requests.Passenger_ID = 1 AND Booking_Requests.Trip_Status = 'Upcoming' ORDER BY Booking_Requests.Booking_ID DESC LIMIT 1;

-- SELECT Booking_Requests.*, Passenger_Accounts.* FROM Booking_Requests JOIN Passenger_Accounts ON Booking_Requests.Passenger_ID = Passenger_Accounts.ID WHERE Booking_Requests.Assigned_DriverID = 1  AND Booking_Requests.Trip_Status = 'Upcoming' LIMIT 1;

-- SELECT * FROM Booking_Requests WHERE Approval = 'Approved' LIMIT 23;

-- SELECT COUNT(*) FROM Booking_Requests WHERE Trip_Status = 'Completed';

-- SELECT Booking_Requests.*, Passenger_Accounts.* FROM Booking_Requests JOIN Passenger_Accounts ON Booking_Requests.Passenger_ID = Passenger_Accounts.ID WHERE Booking_Requests.Approval = 'Pending'