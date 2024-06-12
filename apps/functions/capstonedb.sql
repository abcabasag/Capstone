-- Create the sequence for the request number
CREATE SEQUENCE Request_Number_seq;
SELECT setval('Request_Number_seq', 100000);

-- Function to generate random 8-digit number with NCTS prefix
CREATE OR REPLACE FUNCTION generate_request_number()
RETURNS text AS $$
DECLARE
    random_number text;
BEGIN
    random_number := lpad(floor(random() * 100000000)::text, 8, '0');
    RETURN 'NCTS' || random_number;
END;
$$ LANGUAGE plpgsql;

-- Trigger function to set request_number before insert
CREATE OR REPLACE FUNCTION generate_request_number_trigger()
RETURNS trigger AS $$
BEGIN
    NEW.Request_number := generate_request_number();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the Request_Class table
CREATE TABLE Request_Class(
    Request_Class_ID SERIAL PRIMARY KEY,
    RC_First_name varchar (512) NOT NULL, 
    RC_Middle_I varchar(5),
    RC_Last_name varchar (512) NOT NULL,
    Email varchar (512),
    Contact_Number varchar(512),
    Organization varchar (512) NOT NULL,
    Request_number text NOT NULL UNIQUE DEFAULT generate_request_number(),
    Date_requested timestamp default now(),
    Date_needed date,
    Request_Class_Delete bool
);

-- Trigger to call the trigger function before insert
CREATE TRIGGER set_request_number
BEFORE INSERT ON Request_Class
FOR EACH ROW
EXECUTE FUNCTION generate_request_number_trigger();
CREATE TABLE Group_Citizen_Charter (
	Group_ID serial PRIMARY KEY,
	Group_name varchar(512),
	Group_Citizen_Charter_Delete bool
);


CREATE TABLE Request_type (
	Request_type_ID serial PRIMARY KEY,
	Request_type varchar(512),
	Group_ID integer,
	Request_type_Delete bool,
	CONSTRAINT Request_type_Group_ID_fkey FOREIGN KEY (Group_ID) 
		REFERENCES Group_Citizen_Charter(Group_ID)
);

CREATE SEQUENCE CC_Request_ID_seq;
CREATE TABLE Citizen_Charter_Request (
	CC_Request_ID text DEFAULT 'CC' || nextval('CC_Request_ID_seq')NOT NULL PRIMARY KEY,
	Additional_remarks_CC varchar(1220),
	Request_type_ID integer,
	Citizen_Charter_Request_Delete bool,
	Request_Class_ID integer,
	CONSTRAINT Citizen_Charter_Request_Request_type_ID_fkey FOREIGN KEY (Request_type_ID) 
		REFERENCES Request_type(Request_type_ID),
	CONSTRAINT Citizen_Charter_Request_Request_Class_ID_fkey FOREIGN KEY (Request_Class_ID) 
		REFERENCES Request_Class(Request_Class_ID)
);

CREATE SEQUENCE Procurement_ID_seq;
CREATE TABLE Procurement_Request (
	Procurement_ID text DEFAULT 'PR' || nextval('Procurement_ID_seq')NOT NULL PRIMARY KEY,	
	Item varchar (512),
	Quantity integer,
	Additional_remarks_procu varchar (1220),
	Procurement_Request_Delete bool,
	Request_Class_ID integer,
	CONSTRAINT Procurement_Request_Request_Class_ID_fkey FOREIGN KEY (Request_Class_ID) 
		REFERENCES Request_Class(Request_Class_ID)
);

CREATE TABLE Vehicle (
	Vehicle_ID serial PRIMARY KEY,
	vehicle_type varchar(1220),
	Vehicle_Delete bool
);

Insert into Vehicle ( vehicle_type)
VALUES
	('Mitsubishi Pajero'),
	('Nissan Urvan'),
	('Dyna Truck'),
	('Bajaj Tricycle')
;
	
CREATE TABLE Purpose (
	Purpose_ID serial PRIMARY KEY,
	Purpose_type varchar(1220),
	Purpose_Delete bool
);

Insert into Purpose ( Purpose_type)
VALUES
	('Official'),
	('Project'),
	('Others')
;

CREATE SEQUENCE Vehicle_Dispatch_ID_seq;
CREATE TABLE Vehicle_Dispatch_Request (
	Vehicle_Dispatch_ID text DEFAULT 'VD' || nextval('Vehicle_Dispatch_ID_seq')NOT NULL PRIMARY KEY,
	Passengers varchar (1220),
	Driver_name varchar (1220),
	Destination varchar(1220),
	Borrow_time_from time,
	Borrow_time_to time,
	Borrow_date_from date,
	Borrow_date_to date,
	length_of_trip varchar(50),
	mode_of_claiming varchar(20),
	pickup_time time,
	Remarks_vehicledisp varchar(1220),
	Vehicle_ID integer,
	Purpose_ID integer,
	Vehicle_Dispatch_Request_Delete bool,
	Request_Class_ID integer,
	Purpose_others varchar(1220),
	Terms varchar (10),
	CONSTRAINT Vehicle_Dispatch_Request_Vehicle_ID_fkey FOREIGN KEY (Vehicle_ID) 
		REFERENCES Vehicle(Vehicle_ID),
	CONSTRAINT Vehicle_Dispatch_Request_Purpose_ID_fkey FOREIGN KEY (Purpose_ID) 
		REFERENCES Purpose(Purpose_ID),
	CONSTRAINT Vehicle_Dispatch_Request_Request_Class_ID_fkey FOREIGN KEY (Request_Class_ID) 
		REFERENCES Request_Class(Request_Class_ID)
);

CREATE TABLE users (
	user_id serial PRIMARY KEY,
	First_Name varchar(512),
	Middle_Initial varchar(200),
	Last_name varchar (200),
	user_name varchar(32) unique,
	user_password varchar(64) not null,
	user_modified_on timestamp without time zone default now(),
	user_role varchar(10),
	user_delete_ind boolean default false

);

INSERT INTO users (First_Name, Last_name, user_name, user_password, user_role)
VALUES
	('Admin', 'Admin', 'Admin_UPNCTS', 'adminupcts', 'Admin')
;

CREATE TABLE Status (
	Status_ID serial PRIMARY KEY,
	Status_Name varchar(1220),
	Status_Delete bool
);

INSERT into status (status_name)
VALUES
	('Pending'),
	('Ongoing'),
	('Completed'),
	('Rejected')
;

CREATE TABLE Status_Change (
	Status_Change_ID serial PRIMARY KEY,
	Current_Status varchar (100),
	Date_updated date,
	Remarks_statchange varchar(1220),
	Request_Class_ID integer,
	Status_ID integer,
	user_id integer,
	Status_Change_Delete bool,
	current_ind bool,
	delete_ind bool,
	Date_started date,
	update_finish_time timestamp,
	inserted_on timestamp,
	CONSTRAINT Status_Change_Request_Class_ID_fkey FOREIGN KEY (Request_Class_ID) 
		REFERENCES Request_Class(Request_Class_ID),
	CONSTRAINT Status_Change_Status_ID_fkey FOREIGN KEY (Status_ID) 
		REFERENCES Status(Status_ID),
	CONSTRAINT Status_Change_user_id_fkey FOREIGN KEY (user_id) 
		REFERENCES users(user_id)	
);

Insert into Group_Citizen_Charter (group_id, group_name)
VALUES
	('1', 'TE&E, TEM, INTRA'),
	('2', 'TEM, TE&E, Training, INTRA, Library'),
	('3', 'INTRA'),
	('4', 'Training'),
	('5', 'Data and Information Unit'),
	('6', 'Library'),
	('7', 'Media Committee'),
	('8', 'Admin');

Insert into Request_type (request_type, group_id)
VALUES
	('Technical Service', '1'),
	('Academic Research', '1'),
	('Technical Expertise', '2'),
	('Transport Software', '1'),
	('Student Affairs Coordinator', '3'),
	('Host students, researches, and projects', '1'),
	('Training Programs', '4'),
	('Customized Training Programs', '4'),
	('Training Webinars', '4'),
	('Certificate Request', '4'),
	('Transport Data Request', '5'),
	('Library Access Request', '6'),
	('Library Materials Borrowing', '6'),
	('Library Materials Returning', '6'),
	('Library Donations', '6'),
	('Resource Person Request', '7'),
	('Extension Services', '2'),
	('Equipment and Facilities Use', '8');

INSERT into status (status_name)
VALUES
	('Approved');

