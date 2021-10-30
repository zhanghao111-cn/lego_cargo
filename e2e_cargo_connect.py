#Import
#----------------------------------------------------------------------------------------------------------------------------------------------------
from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Object
#----------------------------------------------------------------------------------------------------------------------------------------------------
hub = PrimeHub() 
mm_motor = MotorPair("C","D")
arm_motor = Motor("E")
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Function definition
#----------------------------------------------------------------------------------------------------------------------------------------------------
def right_turn(degrees,speed,reset):
    if(reset == 1):
        mm_motor.set_default_speed(speed)
    hub.motion_sensor.reset_yaw_angle()
    while(hub.motion_sensor.get_yaw_angle()<degrees):
        mm_motor.start(100)
    mm_motor.stop()

def left_turn(degrees,speed,reset):
    if(reset == 1):
        mm_motor.set_default_speed(speed)
    hub.motion_sensor.reset_yaw_angle()
    while((-hub.motion_sensor.get_yaw_angle())<degrees):
        print(hub.motion_sensor.get_yaw_angle())
        mm_motor.start(-100)
    mm_motor.stop()

def line_follow(speed,m_reflect):
    print("line follow")
    movement_motor.set_default_speed(speed)
    while True:
        movement_motor.start((m_reflect-col_sensor.get_reflected_light())*2)
        if(col_sensor.get_color() == 'red'):
            movement_motor.stop()

def move_arm_up(degree,speed):
    print("Move arm up")
    arm_motor.run_for_degrees(degree,speed)


def move_arm_down(degree,speed):
    print("Move arm down")
    arm_motor.run_for_degrees(-degree,speed)

def move_arm_down_turbo():
    print("Move up down with maximum power and speed")
    arm_motor.start_at_power(100)
    arm_motor.run_for_degrees(180,100)

#----------------------------------------------------------------------------------------------------------------------------------------------------

#Variable definition
#----------------------------------------------------------------------------------------------------------------------------------------------------
switch_flag = 0
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Execution
hub.light_matrix.show_image('HAPPY')
while True:
    hub.left_button.wait_until_pressed()
    if(switch_flag == 1):
        hub.light_matrix.write('3')
        print("Round3")
#Round 3 start
        right_turn(90,20,1)
        left_turn(90,20,1)
#Round 3 end
    if(switch_flag == 0):
        hub.light_matrix.write('1')
        print(switch_flag)
        print("Round1")
#Round 1 start
        right_turn(90,20,1)
#Round 1 end
    switch_flag = 1
    hub.right_button.wait_until_pressed()
    hub.light_matrix.write('2')
    print("Round2")
#Round 2 start
    left_turn(90,20,1)
#Round 2 end