# Untitled - By: chenna - Tue Apr 2 2024

#import sensor, image, time

#sensor.reset()
#sensor.set_pixformat(sensor.RGB565)
#sensor.set_framesize(sensor.QVGA)
#sensor.skip_frames(time = 2000)

#clock = time.clock()

#while(True):
#    clock.tick()
#    img = sensor.snapshot()
#    print(clock.fps())


#import pyb # Import module for board related functions
#import sensor # Import the module for sensor related functions
#import image # Import module containing machine vision algorithms
#import time # Import module for tracking elapsed time

#sensor.reset() # Resets the sensor
#sensor.set_pixformat(sensor.RGB565) # Sets the sensor to RGB
#sensor.set_framesize(sensor.QVGA) # Sets the resolution to 320x240 px
#sensor.set_vflip(True) # Flips the image vertically
#sensor.set_hmirror(True) # Mirrors the image horizontally
#sensor.skip_frames(time = 2000) # Skip some frames to let the image stabilize
## Define the min/max LAB values we're looking for
#thresholdsGreenBall = (0, 70, -128, -14, -99, 127)
#thresholdsYellowBall = (35, 100, -128, -2, 21, 127)
#img = sensor.snapshot() # Takes a snapshot and saves it in memory

## Find blobs with a minimal area of 50x50 = 2500 px
## Overlapping blobs will be merged
#blobs = img.find_blobs([thresholdsGreenBall, thresholdsYellowBall], area_threshold=2500, merge=True)
## Draw blobs
#for blob in blobs:
#    # Draw a rectangle where the blob was found
#    img.draw_rectangle(blob.rect(), color=(0,255,0))
#    # Draw a cross in the middle of the blob
#    img.draw_cross(blob.cx(), blob.cy(), color=(0,255,0))




import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import time # Import module for tracking elapsed time
import math
#import numpy as np

sensor.reset() # Resets the sensor
sensor.set_pixformat(sensor.RGB565) # Sets the sensor to RGB
sensor.set_framesize(sensor.QVGA) # Sets the resolution to 320x240 px
sensor.set_vflip(True) # Flips the image vertically
sensor.set_hmirror(True) # Mirrors the image horizontally
sensor.skip_frames(time = 2000) # Skip some frames to let the image stabilize

# Define the min/max LAB values we're looking for
thresholdsGreenBall = (0, 70, -128, -14, -99, 127)
thresholdsYellowBall = (35, 100, -128, -2, 21, 127)

ledRed = pyb.LED(1) # Initiates the red led
ledGreen = pyb.LED(2) # Initiates the green led

clock = time.clock() # Instantiates a clock object
def calculate_duck_position(u, s_b):
#    u = np.array([274, 214, 119, 43, 87, 77, 263, 181, 82, 137])
#    sb = np.array([9600, 10712, 20306, 12642, 11340, 28390, 8370, 5476, 6399, 30267])
#    theta = np.array([10.19032591, 4.681632549, 13.89504536, -20.41457778, -5.495110344, -21.49293433, 16.53224858, 8.913518786, -10.59562425, 0])
#    d = np.array([30.3, 28, 20, 22, 26.5, 17, 31, 37.5, 36.5, 16])

     # Linear approximation for u vs. theta
#    m_u, c_u = np.polyfit(u, theta, 1)  # Returns slope (m_u) and intercept (c_u)

#    # Linear approximation for 1/sb vs. d
#    inv_sb = 1 / sb  # Calculate 1/sb
#    m_sb, c_sb = np.polyfit(inv_sb, d, 1)  # Returns slope (m_sb) and intercept (c_sb)


    m_u = 0.136
    c_u = -20.4

    m_sb = 150880
    c_sb = 12.3

    # Calculate theta and d using the linear approximations
    theta = m_u * u + c_u  # Theta in degrees
    d = m_sb * (1/s_b) + c_sb

    # Convert theta from degrees to radians
    theta_rad = math.radians(theta)

    # Calculate the relative x and y positions
    x = d * math.cos(theta_rad)
    y = d * math.sin(theta_rad)

    return x, y
while(True):
    clock.tick() # Advances the clock
    img = sensor.snapshot() # Takes a snapshot and saves it in memory

    # Find blobs with a minimal area of 50x50 = 2500 px
    # Overlapping blobs will be merged
    blobs = img.find_blobs([thresholdsGreenBall, thresholdsYellowBall], area_threshold=2500, merge=True)

    # Draw blobs
    for blob in blobs:
        # Draw a rectangle where the blob was found
        img.draw_rectangle(blob.rect(), color=(0,255,0))
        # Draw a cross in the middle of the blob
        img.draw_cross(blob.cx(), blob.cy(), color=(0,255,0))
        print("Center (x, y): ({}, {})  Size: {}".format(blob.cx(), blob.cy(), blob.area()))
        x, y = calculate_duck_position(blob.cx(), blob.area())
        print("Center respect with camera: (x, y): ({}, {}) ".format(x, y))
    # Turn on green LED if a blob was found
    if len(blobs) > 0:
        ledGreen.on()
        ledRed.off()
    else:
    # Turn the red LED on if no blob was found
        ledGreen.off()
        ledRed.on()

    pyb.delay(50) # Pauses the execution for 50ms
    print(clock.fps()) # Prints the framerate to the serial console


