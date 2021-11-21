#Import
#----------------------------------------------------------------------------------------------------------------------------------------------------
from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Object
#----------------------------------------------------------------------------------------------------------------------------------------------------
hub = PrimeHub()
mm_motor = MotorPair("A","B")
#rmm_motor = MotorPair("B","A")
right_motor = Motor("B")
left_motor = Motor("A")
arm_motor = Motor("C")
col_sensor = ColorSensor("F")
dis_sensor = DistanceSensor("D")
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
    mm_motor.move_tank(degrees,'degrees',speed,0)
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
    mm_motor.move_tank(degrees,'degrees',0,speed)
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
    arm_motor.run_for_degrees(-360,100)

def gyro_straight_forward(target_yawn, distance, power):
    right_motor.set_degrees_counted(0)
    while(abs(right_motor.get_degrees_counted()) <= (distance / 17.5 * 360)):
        correction = target_yawn - hub.motion_sensor.get_yaw_angle()
        mm_motor.start_tank_at_power((power + correction), (power - correction))
    mm_motor.stop()

def gyro_straight_backward(target_yawn, distance, power):
    right_motor.set_degrees_counted(0)
    while(abs(right_motor.get_degrees_counted()) <= (distance / 17.5 * 360)):
        correction = target_yawn - hub.motion_sensor.get_yaw_angle()
        rmm_motor.start_tank_at_power((power + correction), (power - correction))
    rmm_motor.stop()

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
    right_motor.set_degrees_counted(0)
    while(right_motor.get_degrees_counted() < distance / 17.5 * 360):
        error = target_light - col_sensor.get_reflected_light()
        integral = error + integral
        derivative = error - last_err
        correction = (error * kp) + (integral * ki) + (derivative * kd)
        mm_motor.start_tank_at_power((power + correction), (power - correction))
        last_err = error
    mm_motor.stop()


#----------------------------------------------------------------------------------------------------------------------------------------------------
#Variable definition
#----------------------------------------------------------------------------------------------------------------------------------------------------
switch_flag = 1 # use as a local variable to switch between round1 and round3
fast_speed = 70 # maximum speed
normal_speed = 50 # normal speed for routine.
slow_speed = 35 #slow speed to control the accuracy
middle_reflection = 80 # used for the line follower or accurate positioning.
#----------------------------------------------------------------------------------------------------------------------------------------------------

#Execution
hub.light_matrix.show_image('HAPPY')


while True:
    hub.left_button.wait_until_pressed()
    if(switch_flag == 1):
        hub.light_matrix.write('3')
        print("Round3")
#Round 3 start
        wait_for_seconds(1)
        mm_motor = MotorPair("A","B")
        hub.motion_sensor.reset_yaw_angle()
        gyro_straight_forward(0,43,normal_speed)# moving straight North from launching aera
        right_turn_motor(80,slow_speed)#step2    trun right robot heading east
        #move_arm_up(25,slow_speed) #lift arm up to pass platooning truck

        gyro_straight_forward(90,60,normal_speed) # complete to move the platooning truck
        move_arm_up(44,slow_speed) #lift arm up to pass platooning truck
        gyro_straight_forward(90,30,normal_speed) # hit west bridge down
        move_arm_up(50,slow_speed) # lift arm up to pass the east bridge piece
        gyro_straight_forward(90,15,normal_speed) #pass east bridge
        move_arm_down(100,slow_speed) # lower arm to hit east bridge
        mm_motor = MotorPair("B","A")
        gyro_straight_forward(90,20,fast_speed) #backward to hit east bridge
        arm_motor.set_stall_detection(True)
        """
        arm_motor.run_for_rotations(-2)
        if arm_motor.was_stalled():
            arm_motor.stop()
            """
        #move_arm_down(80,slow_speed) # lower arm to hold the cargo
        mm_motor = MotorPair("A","B")
        gyro_straight_forward(90,40,fast_speed) #moving toward east
        right_turn_motor(180,slow_speed) #right turn to enter Cargo Connect circle
        gyro_straight_forward(180,2,slow_speed) #adjust robot heading south
        move_arm_up(80,slow_speed) # lift up arm to release cargos
        mm_motor = MotorPair("B","A")
        gyro_straight_forward(170,50,slow_speed) # backing up to unload cargo ship
        right_turn_motor(80,slow_speed) # robot heading west
        mm_motor = MotorPair("A","B")
        gyro_straight_forward(-90,20,slow_speed) #adjust robot heading west
        move_arm_down(50,slow_speed)
        mm_motor = MotorPair("B","A")
        gyro_straight_forward(-90,70,normal_speed) #moving the cargo ship - backing up to east
        mm_motor = MotorPair("A","B")
        gyro_straight_forward(-90,70,normal_speed) #moving forward to west
        left_turn_motor(180,slow_speed) #facing south
        mm_motor = MotorPair("B","A")
        move_arm_up(150,slow_speed)
        #backing up to parking location
        while True:
                if(dis_sensor.get_distance_cm() > 1):
                    gyro_straight_forward(-180,dis_sensor.get_distance_cm(),normal_speed)
                if(dis_sensor.get_distance_cm() <= 1):
                    mm_motor.stop()
                    break
        wait_for_seconds(1)
        mm_motor = MotorPair("A","B")
        right_turn_motor(90,slow_speed) #facing west
        move_arm_up(40,slow_speed) # need to confirm the lifting arm height
        gyro_straight_forward(-90,8,normal_speed)    #moveing forward to parking spot ??? using disctance sensor?
#Round 3 end
    if(switch_flag == 0):
        hub.light_matrix.write('1')
        print(switch_flag)
        print("Round1")
#Round 1 start
        wait_for_seconds(1)
        hub.motion_sensor.reset_yaw_angle()
        mm_motor = MotorPair("B","A")
        gyro_straight_forward(0,115,normal_speed)
        left_turn_motor(88,slow_speed)
        gyro_straight_forward(-49,89,normal_speed)
        mm_motor = MotorPair("A","B")
        mm_motor.move(130,"degrees",0)
        right_turn(0,30,0)
        mm_motor.move(200,"degrees",0)
        wait_for_seconds(1)
        while True:
            if(dis_sensor.get_distance_cm() > 20):
                mm_motor.start(0,-10)
            if(dis_sensor.get_distance_cm() <= 20):
                mm_motor.stop()
                break
        wait_for_seconds(1)
        left_turn_motor(145,slow_speed)
        arm_motor.run_for_rotations(-1)
        mm_motor = MotorPair("A","B")
        gyro_straight_forward(-86,32,slow_speed+10)
        wait_for_seconds(1)
        arm_motor.set_default_speed(slow_speed)
        arm_motor.run_for_rotations(1.25)
        mm_motor.move(-22,"cm",0)
        right_turn_motor(75,slow_speed)
        gyro_straight_forward(1,185,fast_speed)
#Round 1 end
    switch_flag = 1
    hub.right_button.wait_until_pressed()
    hub.light_matrix.write('2')
    print("Round2")
#Round 2 start
    wait_for_seconds(1)
    hub.motion_sensor.reset_yaw_angle()
    gyro_straight_forward(0,51,normal_speed)#step1
    right_turn_motor(80,slow_speed)#step2
    gyro_straight_forward(44,55,fast_speed)
    mm_motor = MotorPair("B","A")
    gyro_straight_forward(40,3,normal_speed)
    move_arm_up(360,slow_speed)
    gyro_straight_forward(40,22,normal_speed)
    left_turn_motor(55,normal_speed)
    mm_motor.move(-3,"cm",normal_speed)
    move_arm_down_turbo()
    gyro_straight_forward(90,80,fast_speed)
#Round 2 end

    switch_flag = 1
    hub.right_button.wait_until_pressed()
    hub.light_matrix.write('3')
    print("Round3")
#Round 3 start
