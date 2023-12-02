# import library Webots dan controller drone Crazyflie
from controller import Robot, Motor

# Inisialisasi robot dan controller drone Crazyflie
robot = Robot()
motor1 = robot.getDevice('m1_motor')
motor2 = robot.getDevice('m2_motor')
motor3 = robot.getDevice('m3_motor')
motor4 = robot.getDevice('m4_motor')

# Set waktu siklus
TIME_STEP = int(robot.getBasicTimeStep())

# Set kecepatan motor
motor1.setPosition(float('inf'))
motor1.setVelocity(-55.368087)
motor2.setPosition(float('inf'))
motor2.setVelocity(55.368087)
motor3.setPosition(float('inf'))
motor3.setVelocity(-55.368087)
motor4.setPosition(float('inf'))
motor4.setVelocity(55.368087)

# Set torsi motor
motor1.setTorque(5.0)
motor2.setTorque(5.0)
motor3.setTorque(5.0)
motor4.setTorque(5.0)

#Set Power
motor_power = 0.0

# Loop siklus
while robot.step(TIME_STEP) != -1:
    # Program akan terus berjalan sampai dihentikan secara manual
    speed1 = motor1.getVelocity()
    speed2 = motor2.getVelocity()
    speed3 = motor3.getVelocity()
    speed4 = motor4.getVelocity()
    print("Speeds: ", speed1, speed2, speed3, speed4)
    # program ini akan terus berjalan selama simulasi berlangsung
    pass
