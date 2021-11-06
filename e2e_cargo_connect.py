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
col_sensor = ColorSensor("B")
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Function definition
#----------------------------------------------------------------------------------------------------------------------------------------------------

def right_turn(degrees,speed,reset):
    mm_motor.set_default_speed(speed)
    if(reset == 1):
        hub.motion_sensor.reset_yaw_angle()
    while(hub.motion_sensor.get_yaw_angle()<degrees):
        mm_motor.start(100)
    mm_motor.stop()

def right_turn_motor(degrees,speed):
    mm_motor.set_default_speed(speed)
    mm_motor.move_tank(degrees,'degrees',50,0)
    #mm_motor.move(degrees,'degrees',100)
    mm_motor.stop()

def left_turn(degrees,speed,reset):
    mm_motor.set_default_speed(speed)
    if(reset == 1):
        hub.motion_sensor.reset_yaw_angle()
    while((-hub.motion_sensor.get_yaw_angle())<degrees):
        print(hub.motion_sensor.get_yaw_angle())
        mm_motor.start(-100)
    mm_motor.stop()

def left_turn_motor(degrees,speed):
    mm_motor.set_default_speed(speed)
    #mm_motor.move(degrees,'degrees',-100)
    mm_motor.move_tank(degrees,'degrees',0,50)
    mm_motor.stop()
    
def line_follow(speed,m_reflect):
    print("line follow")
    mm_motor.set_default_speed(speed)
    while True:
        mm_motor.start((m_reflect-col_sensor.get_reflected_light())*2)
        if(col_sensor.get_color() == 'red'):
            mm_motor.stop()

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
switch_flag = 0 # use as a local variable to switch between round1 and round3
normal_speed = 40 # normal speed for routine. 
slow_speed = 20 #slow speed to control the accuracy
middle_reflection = 80 # used for the line follower or accurate positioning. 
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Execution
hub.light_matrix.show_image('HAPPY')
hub.motion_sensor.reset_yaw_angle()

while True:
    hub.left_button.wait_until_pressed()
    if(switch_flag == 1):
        hub.light_matrix.write('3')
        print("Round3")
#Round 3 start
        wait_for_seconds(1)
        mm_motor.move(600,"degrees",0)#step1
        right_turn_motor(90,normal_speed)#step2
        mm_motor.move(600,"degrees",0)
        right_turn_motor(90,normal_speed)#step3
        mm_motor.move(300,"degrees",0)
        move_arm_down(90,normal_speed)#step4
        mm_motor.move(500,"degrees",0)
        move_arm_up(20,normal_speed)#step5
        mm_motor.move(300,"degrees",0)
        move_arm_up(90,normal_speed)
        mm_motor.move(100,"degrees",0)
        right_turn_motor(180,normal_speed)#step6 start
        mm_motor.move(100,"degrees",0)
        mm_motor.move(-100,"degrees",0)
        move_arm_down(30,normal_speed)
        right_turn_motor(100,normal_speed)
        move_arm_up(30,normal_speed)
        left_turn_motor(100,normal_speed)
        mm_motor.move(-400,"degrees",0)#step6 stop
        right_turn_motor(180,normal_speed)#step7 start
        move_arm_down(30,normal_speed)
        mm_motor.move(-300,"degrees",0)#step8
        move_arm_up(100,normal_speed)
        mm_motor.move(700,"degrees",0)#step9
        left_turn_motor(180,normal_speed)
        mm_motor.move(-600,"degrees",0)
        mm_motor.move(50,"degrees",0)#step10
        right_turn_motor(180,normal_speed)
        mm_motor.move(80,"degrees",0)#step11
#Round 3 end
    if(switch_flag == 0):
        hub.light_matrix.write('1')
        print(switch_flag)
        print("Round1")
#Round 1 start
#Yifei coding on this part
        wait_for_seconds(1)
        mm_motor.move(600,"degrees",0)#step1
        right_turn_motor(90,normal_speed)#step2
        #Option1: straight move
        mm_motor.move(600,"degrees",0)
        right_turn_motor(90,normal_speed)#step3
        mm_motor.move(700,"degrees",0)
        left_turn_motor(60,normal_speed)
        mm_motor.move(500,"degrees",0)
        right_turn_motor(240,normal_speed)
        mm_motor.move(130,"degrees",0)
        move_arm_up(90,slow_speed)
        mm_motor.move(-60,"degrees",0)
        right_turn_motor(180,normal_speed)
        mm_motor.move(2000,"degrees",0)
        #Option2: line following
#Round 1 end
    switch_flag = 1
    hub.right_button.wait_until_pressed()
    hub.light_matrix.write('2')
    print("Round2")
#Round 2 start
    wait_for_seconds(1)
    mm_motor.move(600,"degrees",0)#step1    
    right_turn_motor(90,normal_speed)#step2
    mm_motor.move(600,"degrees",0)
    mm_motor.move(-100,"degrees",0)
    move_arm_up(90,slow_speed)
    right_turn_motor(90,normal_speed)
    mm_motor.move(-800,"degrees",0)
#Round 2 end
