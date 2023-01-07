import socket
import RPi.GPIO as GPIO
import os
import time
import smbus
from gpiozero import Servo
import math

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)  # sw
GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(16, GPIO.OUT)  #led
GPIO.setup(18, GPIO.OUT)  # led

from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()
servo = Servo(25, pin_factory = factory)  #moter

bus = smbus.SMBus(1)
addr = 0x48
AIN0 = 0x40
bus.read_byte(0x48)

IP = ''
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

def begin():
    global option
    print('main menu')
    print('Login or Register\npress 1 : Login\npress 2 : register\nLow light : Get Login Data')
    while True:
        input_state_1 = GPIO.input(13)
        input_state_2 = GPIO.input(15)
        bus.write_byte(addr, AIN0)
        bus.read_byte(addr)
        CDS = bus.read_byte(addr)
        if input_state_1 == 0:
            option = 'login'
            break
        if input_state_2 == 0:
            option = 'reg'
            break
        if CDS > 200:
            option = 'get'
            break

def login(id_pw):
    s.sendall(id_pw.encode('utf-8'))
    result_recv = s.recv(1024).decode()
    if result_recv == 'True':
        print('login success\nDoor is OPEN!\nGame Start!')
        GPIO.output(16, GPIO.HIGH)
        servo.value = math.sin(math.radians(90))  # 1
        time.sleep(1)
        os.system('python3 snake_project.py')
    else:
        print('login fail')
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        
def register(id_pw):
    s.sendall(id_pw.encode('utf-8'))
    result_recv = s.recv(1024).decode()
    if result_recv == 'True':
        print('register success')
        time.sleep(1)
    

def access(option):
    global name
    if(option == 'login'):
        s.sendall('login'.encode('utf-8'))
        os.system('clear')
        print('Enter your id and password to login')
        id_name = input('Enter your id : ')
        password = input('Enter your password : ')
        id_pw = id_name + ':' + password
        login(id_pw)
    if(option == 'reg'):
        s.sendall('register'.encode('utf-8'))
        os.system('clear')
        print('Enter your id and password to register')
        id_name = input('Enter your id : ')
        password = input('Enter your password : ')
        id_pw = id_name + ':' + password
        register(id_pw)
    if(option == 'get'):
        s.sendall('get'.encode('utf-8'))
        login_data = s.recv(1024).decode()
        print(login_data)
        print(login_data.count(':'))
        time.sleep(1)
        
while True:
    os.system('clear')
    GPIO.output(16, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    servo.value = math.sin(math.radians(-90))  # -1
    begin()
    access(option)
        
p.stop()
s.close()