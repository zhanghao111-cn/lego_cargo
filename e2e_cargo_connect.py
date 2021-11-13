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
right_motor = Motor("D")
left_motor = Motor("C")
arm_motor = Motor("E")
col_sensor = ColorSensor("B")
dis_sensor = DistanceSensor("F")
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

def reset_turn():
    mm_motor.set_default_speed(normal_speed)
   # hub.motion_sensor.reset_yaw_angle()
    while(hub.motion_sensor.get_yaw_angle()>0):
        mm_motor.start(-100)
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

def gyro_straight(target_yawn, distance, power):
    hub.motion_sensor.reset_yaw_angle()
    right_motor.run_to_position(0)
    while(right_motor.get_degrees_counted < (distance / 17.5 * 360)):
        #print(distance / 17.5 * 360)
        print(right_motor.get_degrees_counted())
        correction = target_yawn - hub.motion_sensor.get_yaw_angle()
        #mm_motor.start_at_power((power + correction), (power - correction))
        #mm_motor.start_at_power((power - correction), (power + correction))
        #mm_motor.move_tank(10,"degrees",int(power + correction), int(power - correction ))
    
 #       print(power + correction)

    mm_motor.stop()

def pid_turn(target_angle, p_constant, min_power):
    hub.motion_sensor.reset_yaw_angle()
    mm_motor.set_stop_action('hold')
    error = target_angle - hub.motion_sensor.get_yaw_angle()
    max_power = 100
    while(error != 0):
        error = target_angle - hub.motion_sensor.get_yaw_angle()
        control_output = error - p_constant
        if(abs(control_output) > max_power):
            control_output = max_power * target_angle / abs(target_angle)
        if(abs(control_output) < min_power):
            control_output = min_power * target_angle / abs(target_angle)
        mm_motor.start_at_power(control_output, -control_output)
    mm_motor.stop()

def pid_line_follow(kp,ki,kd,distance):
    last_err = 0
    integral = 0
    motor_power = 27
    target_light = 80
    right_motor.run_to_position(0)
    while(right_motor.get_position() > distance / 17.5 * 360):
        error = target_light - col_sensor.get_reflected_light()
        integral = error + integral
        derivative = error - last_err
        correction = (error * kp) + (integral * ki) + (derivative * kd)
        mm_motor.start_at_power((motor_power + correction), (motor_power - correction))
        last_err = error
    mm_motor.stop()


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
"""
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

hub.motion_sensor.reset_yaw_angle()
right_turn(50,30,0)
mm_motor.move(600,"degrees",0)
mm_motor.move(-150,"degrees",0)
right_turn(90,30,0)
mm_motor.move(-200,"degrees",0)
hub.motion_sensor.reset_yaw_angle()
while True:
    if(dis_sensor.get_distance_cm() > 30):
        mm_motor.start(0,10)
 #   if(dis_sensor.get_distance_cm() < 31):
 #       mm_motor.start(0,-10)
    if(dis_sensor.get_distance_cm() <= 30):
        mm_motor.stop()
        break
wait_for_seconds(1)
#right_turn_motor(180,30)
right_turn(90,30,0)
mm_motor.move(1000,"degrees",0)

hub.motion_sensor.reset_yaw_angle()
right_turn(30,20,0)
print(hub.motion_sensor.get_yaw_angle())
mm_motor.move(600,"degrees",0)
mm_motor.move(-300,"degrees",0)
reset_turn()
print(hub.motion_sensor.get_yaw_angle())
wait_for_seconds(1)
right_turn(166,50,0)
print(hub.motion_sensor.get_yaw_angle())
mm_motor.move(1000,"degrees",0)
"""
gyro_straight(0,10,70)
















