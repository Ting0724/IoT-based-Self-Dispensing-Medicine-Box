#Import library
import RPi.GPIO as GPIO #-->Pin control
from time import sleep #-->For time delay
import threading #-->For multitasking
from lcd import drivers #-->For lcd control 
import mysql.connector as mysql #-->For remote access to mysql database
import smtplib #--> For sending email
from mfrc522 import SimpleMFRC522
import sys
import datetime

#GPIO set mode
GPIO.setmode(GPIO.BCM)

#Disable warnings 
GPIO.setwarnings(False)

#Define GPIO for component
but_reset = 17
but_help = 27
# but_spare = 22
buzzer = 4
led_red = 16
led_yellow = 20
led_green = 21
led_white = 12
ir_1 = 5
ir_2 = 6
ir_3 = 13
motor_1 = 14
motor_2 = 15
motor_3 = 18
ir_cup = 23

#Define GPIO pin used
# --Define output pins
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(led_red, GPIO.OUT)
GPIO.setup(led_yellow, GPIO.OUT)
GPIO.setup(led_green, GPIO.OUT)
GPIO.setup(led_white, GPIO.OUT)
GPIO.setup(motor_1, GPIO.OUT)
GPIO.setup(motor_2, GPIO.OUT)
GPIO.setup(motor_3, GPIO.OUT)
# --Define input pins
GPIO.setup(but_reset, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(but_help, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(ir_1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(ir_2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(ir_3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(ir_cup, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#global variable in main thread
global start_fetch
global error
global motor_run

#status of medicine box
alarm = 0
ready = 0
dispensing = 0



"""
#Initialization
GPIO.output(buzzer, alarm)
GPIO.output(led_red, error)
GPIO.output(led_yellow, dispensing)
GPIO.output(led_green, ready)
"""

#Declaration for each pwm channel (Giving a name)
mtr_1 = GPIO.PWM(motor_1,50)
mtr_2 = GPIO.PWM(motor_2,50)
mtr_3 = GPIO.PWM(motor_3,50)

#Position of servo motor
posn0 = 2.5 #<-- 0 degree position
posnC = 7.5 #<-- neutral position
stop = 0

#Errors
error = 0
error_state = "N"

#Declaration of LCD display (Giving a name)
display = drivers.Lcd()

#Declaration of RFID reader (Giving a name)
reader = SimpleMFRC522()

#Variable to stop looping
stop_loop1 = 0
stop_fetch = 0
stop_loop2 = 0
stop_loop3 = 0

#Variable to start fetch data
start_fetch = 1

#Variable for pill detection
detect_1 = 0
detect_2 = 0
detect_3 = 0
chk1 = 0
chk2 = 0
chk3 = 0

#Variable for completing dispensing
done1 = 0
done2 = 0
done3 = 0

#Variable for pill number
panadol_num = 0
painkiller_num = 0
antibiotic_num = 0

#Variable for patient ID
patient_id = 0

#Variable to start servo motor
motor_run = 0

#Variable for displaying on LCD
patient_firstname = ""
patient_lastname = ""
disease_name = ""
age = ""
gender = ""
#patient_info = 0

#Variable for inserting data into database
room_location = 0
bed_location = ""

#Variable for database connection
connection_successful = 0

#Variable for displaying error
dis_error1 = 0
dis_error2 = 0
dis_error3 = 0


def container_1(antibiotic):
    global detect_1, error, chk1, dispensing, done1

    while antibiotic != 0:
        
        if antibiotic != 0:
            dispensing = 1
        if error == 1:
            antibiotic = 0
            
        while antibiotic != 0 and error == 0:
            
            mtr_1.start(posn0)
            print("position motor 1 0")
            sleep(1)
            mtr_1.ChangeDutyCycle(posnC)
            print("position motor 1 Center")

            sleep(3)

            mtr_1.ChangeDutyCycle(posn0)
            antibiotic = antibiotic - 1
            
            if antibiotic == 0:
                done1 = 1
                
            sleep(1)
            mtr_1.ChangeDutyCycle(stop)
            
        else:
            pass
    else:
        #pass
        done1 = 1     

def error_occurred_c1():
    global detect_1, alarm, error, chk1, done1, dis_error1 
    #detect_1
    #sleep(2)
    print(detect_1)
    while done1 != 1 and error == 0:
        while detect_1 == 1:
            print("Checking pill detection for 1")
            time_delay1 = 10 #<--
            
            while chk1 == 1 and time_delay1 != 0:
                sleep(1)
                time_delay1 = time_delay1 - 1
                
            if detect_1 == 1 and time_delay1 == 0:
                print("Error Occurred")
                #GPIO.output(buzzer, 1)
                #GPIO.output(led_red, 1)
                error = 1
                dis_error1 = 1
                detect_1 = 0
                print(detect_1)
            else:
                pass


def container_2(panadol):
    global detect_2, error, chk2, dispensing, done2

    while panadol != 0:

        if panadol != 0:
            dispensing = 1
        if error == 1:
            panadol = 0
            
        while panadol != 0 and error == 0:
            
            mtr_2.start(posn0)
            print("position motor 2 0")
            sleep(1)
            mtr_2.ChangeDutyCycle(posnC)
            print("position motor 2 Center")

            sleep(3)

            mtr_2.ChangeDutyCycle(posn0)
            panadol = panadol - 1
            
            if panadol == 0:
                done2 = 1
                
            sleep(1)
            mtr_2.ChangeDutyCycle(stop)
            
        else:
            pass
    else:
        #pass
        done2 = 1
                    
def error_occurred_c2():
    global detect_2, alarm, error, chk2, done2, dis_error2
    #detect_2
    #sleep(2)
    print(detect_2)
    while done2 != 1 and error == 0:
        while detect_2 == 1:
            print("Checking pill detection for 1")
            time_delay2 = 10 #<--
            
            while chk2 == 1 and time_delay2 != 0:
                sleep(1)
                time_delay2 = time_delay2 - 1
                
            if detect_2 == 1 and time_delay2 == 0:
                print("Error Occurred")
                #GPIO.output(buzzer, 1)
                #GPIO.output(led_red, 1)
                error = 1
                dis_error2 = 1
                detect_2 = 0
                print(detect_2)
            else:
                pass
            
 
def container_3(painkiller):
    global detect_3, error, chk3, dispensing, done3

    while painkiller != 0:
        
        if painkiller != 0:
            dispensing = 1
        if error == 1:
            painkiller = 0
            
        while painkiller != 0 and error == 0:
            
            mtr_3.start(posn0)
            print("position motor 3 0")
            sleep(1)
            mtr_3.ChangeDutyCycle(posnC)
            print("position motor 3 Center")

            sleep(3)

            mtr_3.ChangeDutyCycle(posn0)
            painkiller = painkiller - 1
            
            if painkiller == 0:
                done3 = 1
            sleep(1)
            
            mtr_3.ChangeDutyCycle(stop)
            
        else:
            pass
    else:
        #pass
        done3 = 1
                    
def error_occurred_c3():
    global detect_3, alarm, error, chk3, done3, dis_error3
    #detect_3
    #sleep(2)
    print(detect_3)
    while done3 != 1 and error == 0:
        while detect_3 == 1:
            print("Checking pill detection for 1")
            time_delay3 = 10 #<--
            
            while chk3 == 1 and time_delay3 != 0:
                sleep(1)
                time_delay3 = time_delay3 - 1
                
            if detect_3 == 1 and time_delay3 == 0:
                print("Error Occurred")
                #GPIO.output(buzzer, 1)
                #GPIO.output(led_red, 1)
                error = 1
                dis_error3 = 1
                detect_3 = 0
                print(detect_3)
            else:
                pass

def error_removecup(check_cup):
    global error, done1, done2, done3
    
    while (done1 != 1 or done2 != 1 or done3 != 1) and error == 0:
        if GPIO.input(ir_cup) == 1 and check_cup == 0:
            error = 1
            display.lcd_clear() 
            display.lcd_display_string("Error: Cup is", 1)  # Write line of text
            display.lcd_display_string("Removed", 2)  # Write line of text
            print("Cup Error Occurred")
        

while True:
    
    while connection_successful != 1 and start_fetch == 1 and error == 0:
        try:
            display.lcd_clear() 
            display.lcd_display_string("Connecting ", 1)  # Write line of text
            display.lcd_display_string("database", 2)  # Write line of text
            # enter your server IP address/domain name
            HOST = "192.168.234.19" # or "domain.com"
            # database name, if you want just to connect to MySQL server, leave it empty
            DATABASE = "medicine_box"
            # this is the user you create
            USER = "staff"
            # user password
            PASSWORD = "000724see"
            # connect to MySQL server
            db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
            print("Connected to:", db_connection.get_server_info())
            # enter your code here!
            # connection_successful = 1
                
            GPIO.output(buzzer, 0)
            GPIO.output(led_red, 0)
            GPIO.output(led_green, 1)
            GPIO.output(led_yellow, 0)
                
            display.lcd_clear() 
            display.lcd_display_string("Connected to ", 1)  # Write line of text
            display.lcd_display_string("database", 2)  # Write line of text
            sleep(1)
            display.lcd_clear() 
            display.lcd_display_string("Pls put your cup", 1)  # Write line of text
            display.lcd_display_string("inside the box", 2)  # Write line of text
            sleep(1)
                
                
                
            if GPIO.input(ir_cup) == 0:
                
                connection_successful = 1                    
                start_fetch = 0
                    
                mycursor = db_connection.cursor()
                #stop_fetch = 1
                print("Hold a tag near the reader")
                display.lcd_clear() 
                display.lcd_display_string("Hold your tag", 1)  # Write line of text
                display.lcd_display_string("near the reader  ", 2)  # Write line of text
                sleep(2)
                id, text = reader.read()
                GPIO.output(buzzer, 1)
                sleep(0.1)
                GPIO.output(buzzer, 0)
                #print("ID: %s\nPatient ID: %s" % (id,patient_id))
                patient_id = text
                print(patient_id)
                        
                mycursor.execute("SELECT * FROM patient Where Patient_ID = %s", (patient_id,))
                #mycursor.execute("SELECT * FROM patient Where Patient_ID = '3'")
                patient_table = mycursor.fetchone()
                print(patient_table)
                patient_firstname = patient_table[1]
                patient_lastname = patient_table[2]
                disease_name = patient_table[3]
                age = patient_table[4]
                gender = patient_table[5]
                prescription_patient = patient_table[6]
                doctor_email = patient_table[7]
                print(patient_firstname)
                print(patient_lastname)
                print(disease_name)
                print(age)
                print(gender)
                print(prescription_patient)

                mycursor.execute("SELECT * FROM prescription Where Prescription_ID = %s", (prescription_patient,))
                prescription_table = mycursor.fetchone()
                print(prescription_table)
                antibiotic_num = prescription_table[1]
                panadol_num = prescription_table[2]
                painkiller_num = prescription_table[3]
                print(antibiotic_num)
                print(panadol_num)
                print(painkiller_num)

                mycursor.execute("SELECT * FROM room Where Patient_ID = %s", (patient_id,))
                room_table = mycursor.fetchone()  

                time = datetime.datetime.now()
                #The date contains year, month, day, hour, minute, second, and microsecond.
                #print(time)
                room_location = room_table[0]
                bed_location = room_table[1]
                '''
                store_data = (time, room_location, bed_location, patient_id, patient_firstname, patient_lastname)
                mycursor.execute("INSERT INTO event (Time, Room_No, Bed_location, Patient_ID, First_name, Last_name) VALUES (%s,%s, %s, %s, %s, %s)", (store_data)) 
                db_connection.commit()
                print(mycursor.rowcount, "record inserted.")
                '''

                display.lcd_clear() 
                display.lcd_display_string(f"Name: {patient_firstname}", 1)  # Write line of text
                display.lcd_display_string(f"{patient_lastname}", 2)  # Write line of text
                sleep(2)
                display.lcd_clear() 
                display.lcd_display_string(f"Disease: {disease_name}", 1)  # Write line of text
                display.lcd_display_string(f"Age: {age}", 2)  # Write line of text
                sleep(2)
                display.lcd_clear() 
                display.lcd_display_string(f"Gender: {gender}", 1)  # Write line of text
                #display.lcd_display_string(f"Age: {age}", 2)  # Write line of text
                sleep(2)
                display.lcd_clear() 
                display.lcd_display_string(f"Medicine: ", 1)  # Write line of text
                display.lcd_display_string(f"Antibiotic: {antibiotic_num}", 2)  # Write line of text
                sleep(2)
                display.lcd_clear()
                display.lcd_display_string(f"Panadol: {panadol_num}", 1)  # Write line of text
                display.lcd_display_string(f"Painkiller: {painkiller_num}", 2)  # Write line of text
                sleep(2)
                display.lcd_clear() 
                display.lcd_display_string("Dispensing....", 1)  # Write line of text
                display.lcd_display_string("Please wait", 2)  # Write line of text
                sleep(2)

                errcup_t = threading.Thread(target = error_removecup, args = (0,))
                errcup_t.start()
                                
                c1_t = threading.Thread(target = container_1, args = (antibiotic_num,))
                c1_t.start()
                c2_t = threading.Thread(target = container_2, args = (panadol_num,))
                c2_t.start()
                c3_t = threading.Thread(target = container_3, args = (painkiller_num,))
                c3_t.start()

        except:
            connection_successful = 0
            display.lcd_clear() 
            display.lcd_display_string("Not connected", 1)  # Write line of text
            display.lcd_display_string("to database", 2)  # Write line of text
            
    if (GPIO.input(but_reset) == 1 and stop_loop1 == 0):
        
        if error == 1:

            time = datetime.datetime.now()
            error_data = "Y"
            store_data = (time, room_location, bed_location, patient_id, patient_firstname, patient_lastname, error_data)
            mycursor.execute("INSERT INTO event (Time, Room_No, Bed_location, Patient_ID, First_name, Last_name, Error) VALUES (%s,%s, %s, %s, %s, %s, %s)", (store_data)) 
            db_connection.commit()
            print(mycursor.rowcount, "record inserted with error occurred.")
            
            print("Button reset is pressed")
            GPIO.output(buzzer, 0)
            GPIO.output(led_red, 0)
            stop_loop1 = 1
            stop_loop3 = 0
            sleep(0.5)
            mtr_1.ChangeDutyCycle(posn0)
            mtr_2.ChangeDutyCycle(posn0)
            mtr_3.ChangeDutyCycle(posn0)
            
            sleep(0.5)
            mtr_1.ChangeDutyCycle(stop)
            mtr_2.ChangeDutyCycle(stop)
            mtr_3.ChangeDutyCycle(stop)
            print(f"error now is: {error}")
            sleep(3)
            # Pls replace button reset
            error = 0
            dispensing = 0
            start_fetch = 1
            stop_loop1 = 0
            connection_successful = 0
            done1 = 0
            done2 = 0
            done3 = 0
            GPIO.output(led_white, 0)
            
        

    if GPIO.input(but_help) == 1 and stop_loop3 == 0:

        GPIO.output(led_white, 1)

        stop_loop3 = 1
            
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('self.dispensing.medicine.box@gmail.com', 'medicinebox')

        subject = 'Patient calls for HELP'
        body = f'{patient_firstname} {patient_lastname} is pressed help button at the location of {room_location}{bed_location}'
        name = f'Patient name: {patient_firstname} {patient_lastname}'
        location = f'Location: {room_location}{bed_location}'
        msg = f'Subject:{subject}\n\n{body}.\n\n{name}\n{location}'

        server.sendmail('self.dispensing.medicine.box@gmail.com', doctor_email, msg)
        print('Mail sent')


    if error == 1:
                
        GPIO.output(buzzer, 1)
        GPIO.output(led_red, 1)
        GPIO.output(led_green, 0)
        GPIO.output(led_yellow, 0)
        
        
    elif dispensing == 1:
        GPIO.output(buzzer, 0)
        GPIO.output(led_red, 0)
        GPIO.output(led_green, 0)
        GPIO.output(led_yellow, 1)

    if dis_error1 == 1 or dis_error2 == 1 or dis_error3 == 1:
        display.lcd_clear() 
        display.lcd_display_string("Error: Pill", 1)  # Write line of text
        display.lcd_display_string("Not Detected", 2)  # Write line of text
        sleep(0.5)
        dis_error1 = 0
        dis_error2 = 0
        dis_error3 = 0
        

    if done1 == 1 and done2 == 1 and done3 == 1 and error != 1:
        
        store_data = (time, room_location, bed_location, patient_id, patient_firstname, patient_lastname)
        mycursor.execute("INSERT INTO event (Time, Room_No, Bed_location, Patient_ID, First_name, Last_name) VALUES (%s,%s, %s, %s, %s, %s)", (store_data)) 
        db_connection.commit()
        print(mycursor.rowcount, "record inserted with no error.")
        
        sleep(3)
        GPIO.output(buzzer, 1)
        GPIO.output(led_green, 1)
        GPIO.output(led_yellow, 0)
        sleep (0.3)
        GPIO.output(buzzer, 0)
        sleep (0.3)
        GPIO.output(buzzer, 1)
        sleep (0.3)
        GPIO.output(buzzer, 0)
        sleep (0.3)
        GPIO.output(buzzer, 1)
        sleep (0.3)
        GPIO.output(buzzer, 0)
        stop_loop2 = 0

        while stop_loop2 == 0:
            print("How many theads?")
            print(threading.active_count())
            display.lcd_clear() 
            display.lcd_display_string("You may take", 1)  # Write line of text
            display.lcd_display_string("your medicine", 2)  # Write line of text
            sleep(0.5)

            if GPIO.input(ir_cup) == 1:
                print("Initializing")
                display.lcd_clear() 
                display.lcd_display_string("Thank you", 1)  # Write line of text
                display.lcd_display_string("Take care", 2)  # Write line of text
                sleep(2)
                dispensing = 0
                start_fetch = 1
                connection_successful = 0
                #error = 0
                done1 = 0
                done2 = 0
                done3 = 0
                stop_loop2 = 1
                stop_loop3 = 0
                GPIO.output(led_white, 0)
        
        

    

