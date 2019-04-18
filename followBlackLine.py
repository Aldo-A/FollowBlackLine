#!/usr/bin/env python3
import picar
from picar.line_sensor import *
from picar.front_wheels import *
from picar.back_wheels import *
import time

steering = Front_Wheels()  # create a Front_Wheels object for steering the car
motors = Back_Wheels()    # create a Back_Wheels object to move the car
lineSensor = Line_Sensor()  # creates a line sensor object to get readings
motor.speed=30
picar.setup()
steering.ready()
motors.ready()

# Returns line sensor readings; (speed, angle to turn)
def getLineControls():
    SA=(motors.speed,steering.angle)
    reading=lineSensor.read_digital()
    randomReadings=[[1,1,1,1,1], [0,1,1,1,0], [0,0,1,1,0], [0,1,1,0,0], [1,1,0,1,1], [1,1,0,0,1], [1,0,0,1,1], [1,0,1,1,1]]

    if reading == [0,0,0,0,0]:
             SA=(29,120)
    elif reading in randomReadings:
             SA=(30,130)
    else:
        if reading==[1,0,0,0,0]:
            SA=(30,90)
        elif reading==[1,1,0,0,0]:
                SA=(30,110)
        elif reading==[1,1,1,0,0]:
            SA=(30,120)
        elif reading==[1,1,1,1,0]:
                SA=(30,125)
        elif reading==[0,0,0,0,1]:
                SA=(30,90)
        elif reading==[0,0,0,1,1]:
                SA=(30,80)
        elif reading==[0,0,1,1,1]:
                SA=(30,70)
         elif reading==[0,1,1,1,1]:
                SA=(30,50)

    return SA

# Makes pi-car go backward to avoid collision/ getting off course
def hitWall(Speed,Angle):
    motors.speed=Speed
    steering.turn(Angle)
    motors.backward()
    time.sleep(2)
    motors.stop()
    steering.turn(80)
    motors.forward()
    time.sleep(.5)

# Gets reading and makes decision on what direction to turn
def followLine():
    speed=motors.speed
    motors.forward()
    while speed!=0:
        speed,angle=getLineControls()
        if (speed,angle)==(30,130):
            hitWall(speed,angle)
        else:
            motors.speed=speed
            steering.turn(angle)
    motors.stop()

# Makes pi-car follow black line 
def goBot():
    try:
        followLine()
    except Exception as e:
        traceback.print_exc()
    finally:
        motors.stop()
        steering.ready()
        
print("Following line...")
goBot()
