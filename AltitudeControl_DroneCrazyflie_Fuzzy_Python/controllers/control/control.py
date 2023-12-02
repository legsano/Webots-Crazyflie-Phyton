from controller import Robot

# Inisialisasi robot dan motor
robot = Robot()
motor1 = robot.getDevice('m1_motor')
motor2 = robot.getDevice('m2_motor')
motor3 = robot.getDevice('m3_motor')
motor4 = robot.getDevice('m4_motor')

# Set waktu siklus
TIME_STEP = int(robot.getBasicTimeStep())

# Set kecepatan motor
S = 1.0
H = 55.36808

gps = robot.getDevice("gps")
gps.enable(10)

# Set posisi motor
motor1.setPosition(float('inf'))
motor2.setPosition(float('inf'))
motor3.setPosition(float('inf'))
motor4.setPosition(float('inf'))

# Set torsi motor
motor1.setTorque(5.0)
motor2.setTorque(5.0)
motor3.setTorque(5.0)
motor4.setTorque(5.0)

# Fungsi untuk mendeteksi input keyboard
def check_keyboard_input():
    keyboard = robot.getKeyboard()
    keyboard.enable(10)
    
    while robot.step(TIME_STEP) != -1:
        key = keyboard.getKey()
        x, y, z = gps.getValues()
        print("Altitude:", z)
        
        if key == ord('Q') or key == ord('q'):
            # Tombol Q ditekan, drone naik
            motor1.setVelocity(-H - S)
            motor2.setVelocity(H + S)
            motor3.setVelocity(-H - S)
            motor4.setVelocity(H + S)
        elif key == ord('E') or key == ord('e'):
            # Tombol E ditekan, drone turun
            motor1.setVelocity(H + S)
            motor2.setVelocity(-H - S)
            motor3.setVelocity(H + S)
            motor4.setVelocity(-H - S)
        else:
            # Tidak ada input, drone tetap stabil
            motor1.setVelocity(-H)
            motor2.setVelocity(H)
            motor3.setVelocity(-H)
            motor4.setVelocity(H)

# Panggil fungsi untuk memulai kontrol dengan keyboard
check_keyboard_input()
