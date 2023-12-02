import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from controller import Robot, Gyro
import math
import time

# Inisialisasi robot dan controller drone Crazyflie
robot = Robot()
motor1 = robot.getDevice('m1_motor')
motor2 = robot.getDevice('m2_motor')
motor3 = robot.getDevice('m3_motor')
motor4 = robot.getDevice('m4_motor')

motor1.setPosition(float('inf'))
motor2.setPosition(float('inf'))
motor3.setPosition(float('inf'))
motor4.setPosition(float('inf'))

# Set torsi motor
motor1.setTorque(5.0)
motor2.setTorque(5.0)
motor3.setTorque(5.0)
motor4.setTorque(5.0)

# Set waktu siklus
TIME_STEP = int(robot.getBasicTimeStep())
# Set kecepatan motor
H = 55.36808
# Brake
B = 0.885363
# Mendapatkan referensi ke motor dan sensor
gyro = Gyro("gyro")
# Inisialisasi sensor GPS
gps = robot.getDevice("gps")
gps.enable(10)
# S
S = 0.1

# Deklarasi variabel input dan output
height = ctrl.Antecedent(np.arange(0, 11, 0.01), 'height')
velocity = ctrl.Consequent(np.arange(-4, 4, 0.01), 'velocity')


# Deklarasi fungsi keanggotaan untuk variabel input dan output
height['terlalurendah'] = fuzz.trimf(height.universe, [0, 0, 2.5])
height['rendah'] = fuzz.trimf(height.universe, [0, 2.5, 4.5])
height['normal'] = fuzz.trimf(height.universe, [3.5, 5 ,6.5])
height['tinggi'] = fuzz.trimf(height.universe, [5.5, 7.5, 10])
height['terlalutinggi'] = fuzz.trimf(height.universe, [7.5, 10, 10])

velocity['cepatN'] = fuzz.trimf(velocity.universe, [-3.25, -3.25, -1])
velocity['sedenganN'] = fuzz.trimf(velocity.universe, [-3.25, -1.75, -0.25])
velocity['lambatN'] = fuzz.trimf(velocity.universe, [-3.25, -0.25, -0.25])

velocity['zero'] = fuzz.trimf(velocity.universe, [-3.25, 0, 3.25])

velocity['lambatP'] = fuzz.trimf(velocity.universe, [0.25, 0.25, 3.25])
velocity['sedenganP'] = fuzz.trimf(velocity.universe, [0.25, 1.75, 3.25])
velocity['cepatP'] = fuzz.trimf(velocity.universe, [1, 3.25, 3.25])

# Rule Base
rule1 = ctrl.Rule(height['terlalurendah'], velocity['cepatP'])
rule2 = ctrl.Rule(height['rendah'] & height['terlalurendah'], velocity['sedenganP'])
rule3 = ctrl.Rule(height['rendah'], velocity['lambatP'])
rule4 = ctrl.Rule(height['rendah'] & height['normal'], velocity['zero'])

rule5 = ctrl.Rule(height['normal'], velocity['zero'])

rule6 = ctrl.Rule(height['tinggi'] & height['normal'], velocity['zero'])
rule7 = ctrl.Rule(height['tinggi'], velocity['lambatN'])
rule8 = ctrl.Rule(height['tinggi'] & height['terlalutinggi'], velocity['sedenganN'])
rule9 = ctrl.Rule(height['terlalutinggi'], velocity['cepatN'])


# Pembuatan sistem kontrol
velocity_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
velocity_sim = ctrl.ControlSystemSimulation(velocity_ctrl)


# Timer sebelum drone naik
start_time = time.time()
while time.time() - start_time < 5:
    # Set kecepatan motor awal H
    motor1.setVelocity(-H)
    motor2.setVelocity(H)
    motor3.setVelocity(-H)
    motor4.setVelocity(H)
    robot.step(TIME_STEP)

def check_keyboard_input():
    keyboard = robot.getKeyboard()
    keyboard.enable(10)
    
    while robot.step(TIME_STEP) != -1:
        key = keyboard.getKey()
        
        # Baca nilai GPS
        x, y, z = gps.getValues()
        print("+++++++++++++++++++++++L++++++++++++++++++++++++")
        print("Altitude:", z)
    
        # Baca nilai Yaw Gyro
        yaw = gyro.getValues()[1]
        print("Yaw:", yaw)

        # Baca kecepatan motor
        speed1 = motor1.getVelocity()
        speed2 = motor2.getVelocity()
        speed3 = motor3.getVelocity()
        speed4 = motor4.getVelocity()
        print("Speeds: {:.3f}, {:.3f}, {:.3f}, {:.3f}".format(speed1, speed2, speed3, speed4))

        # Set input variabel
        velocity_sim.input['height'] = z

        # Melakukan perhitungan sistem pengontrol fuzzy
        velocity_sim.compute()

        # Menampilkan hasil defuzzifikasi
        A = 0

        if 4.4 <= z <= 5:
            A = velocity_sim.output['velocity'] / 10 - B
            print("Output Velocity: {:.6f}".format(A))
            print("++++++++++++++++++++++++++++++++++++++++++++++++")
        else:
            A = velocity_sim.output['velocity'] / 10
            print("Output Velocity: {:.6f}".format(A))
            print("++++++++++++++++++++++++++++++++++++++++++++++++")

        # Set kecepatan motor
        motor1.setVelocity(-H - A)
        motor2.setVelocity(H + A)
        motor3.setVelocity(-H - A)
        motor4.setVelocity(H + A)
        
        if key == ord('Q') or key == ord('q'):
            # Tombol Q ditekan, drone naik
            motor1.setVelocity(-H - S)
            motor2.setVelocity(H + S)
            motor3.setVelocity(-H - S)
            motor4.setVelocity(H + S)

        elif key == ord('E') or key == ord('e'):
            # Tombol E ditekan, drone turun
            motor1.setVelocity(-H + S)
            motor2.setVelocity(H - S)
            motor3.setVelocity(-H + S)
            motor4.setVelocity(H - S)

# Panggil fungsi untuk memulai kontrol dengan keyboard
check_keyboard_input()    