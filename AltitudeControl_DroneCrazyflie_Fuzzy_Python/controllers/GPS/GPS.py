from controller import Robot

#inisialisasi robot dan gps
robot = Robot()
gps = robot.getDevice("gps")

#active gps
gps.enable(10)

while robot.step(64) != -1:
    #read gps
    x,y,z = gps.getValues()
    print("Altitude",z)