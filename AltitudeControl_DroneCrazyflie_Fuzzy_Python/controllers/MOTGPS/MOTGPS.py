from controller import Robot, Gyro

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
motor1.setVelocity(-54.36808)
motor2.setPosition(float('inf'))
motor2.setVelocity(55.36808)
motor3.setPosition(float('inf'))
motor3.setVelocity(-54.36808)
motor4.setPosition(float('inf'))
motor4.setVelocity(55.36808)

# Set torsi motor
motor1.setTorque(5.0)
motor2.setTorque(5.0)
motor3.setTorque(5.0)
motor4.setTorque(5.0)

# Set Power
motor_power = 5.0

# Inisialisasi sensor GPS
gps = robot.getDevice("gps")
gps.enable(10)
gyro = robot.getDevice("gyro")
gyro.enable(TIME_STEP)

# Loop siklus
while robot.step(TIME_STEP) != -1:
    # Baca nilai GPS
    x, y, z = gps.getValues()
    print("Altitude:", z)

    # Baca kecepatan motor
    speed1 = motor1.getVelocity()
    speed2 = motor2.getVelocity()
    speed3 = motor3.getVelocity()
    speed4 = motor4.getVelocity()
    print("Speeds:", speed1, speed2, speed3, speed4)
    
    # Baca nilai yaw dari gyro
    yaw = gyro.getValues()[1]
    print("Yaw:", yaw)
