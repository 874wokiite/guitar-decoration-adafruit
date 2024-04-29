## Setup Block ##
import board
import time
import adafruit_apds9960.apds9960
import neopixel
import adafruit_lis3dh
import math
import adafruit_fancyled.adafruit_fancyled as fancy
from digitalio import DigitalInOut, Pull


WHITE = (255, 255, 255, 0)
# create an I2C() object
i2c = board.I2C()
pixel_strip = neopixel.NeoPixel(board.D13, 30, bpp=3)
pixel_ring = neopixel.NeoPixel(board.D12, 12, bpp=4)
brightness = 0.1
# create an object for the APDS9960
apds = adafruit_apds9960.apds9960.APDS9960(i2c)
# cretae an object for the lis3dh
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

sw1 = DigitalInOut(board.D5)
sw1.switch_to_input()
# variable to track the previous value of the switch
sw1_pre = sw1.value
light1 = False
# enable gesture input (gesture requries proximity also)
apds.enable_gesture = True
apds.enable_proximity = True

# a variable to store the previous gesture
pre_gesture = 0
palette1 = [fancy.CRGB(255, 255, 255),  # White
           fancy.CRGB(255, 255, 0),    # Yellow
           fancy.CRGB(130, 255, 86),      # Green
           fancy.CRGB(86, 154, 255),      # Blue
           fancy.CRGB(0,0,0)]          # Black
palette2 = [fancy.CRGB(255, 0, 229),      # Red
           fancy.CRGB(0,0,0),              #black
           fancy.CRGB(51,0,255)]          # purple
palette3 = [fancy.CRGB(86, 255, 204),      # light green
           fancy.CRGB(0,0,0)]          # Black
palette4 = [fancy.CRGB(255, 0, 0,),
            fancy.CRGB(192, 60,0) ]
# loop forever
offset = 0  # Position offset into palette to make it "spin"

mode = 0

i = 0

while True:

    print(time.monotonic())
    ## Input Block ##
    # poll the sensor for a gesture
    this_gesture = apds.gesture()

    # capture all three x y and z values at once
    x, y, z = lis3dh.acceleration

    ## calculation block ##
    #x_angle = math.atan2(y, z) * 57.3
    y_angle = math.atan2(-x, math.sqrt(y ** 2 + z ** 2)) * 57.3
    x_angle = math.atan2(-z, math.sqrt(x ** 2 + y ** 2)) * 57.3
    z_angle = math.atan2(-y, math.sqrt(z ** 2 + x ** 2)) * 57.3
    # gather input values as an integer
    sw1_read = int(sw1.value)
    print((y_angle))
    print((x_angle))
    print((z_angle))


    # compare the previous sw1 state to the current state with if
    if sw1_read != sw1_pre:
        # sw1_read is not equal to sw1_pre so the switch state has changed
        # since it changed, lets save the new value to sw1_pre
        sw1_pre = sw1_read
        # if the state of the switch is False, it has been pushed down
        if sw1_read == False:
            # toggle the light variable
            light1 = not light1

    if this_gesture != pre_gesture:
        if this_gesture != 0:
            mode = this_gesture
        pre_gesture = this_gesture

    print(mode)

    if light1 == True:
        if mode == 1:
            for i in range(30):
                color = fancy.palette_lookup(palette2, offset + i )
                pixel_strip[i] = color.pack()
            for i in range(12):
                color = fancy.palette_lookup(palette1, offset + i/11 )
                pixel_ring[i] = color.pack()
            if z_angle >= 40:
                offset += 0.25  # Bigger number = faster spin
            else:
                offset += 0.05  # Bigger number = faster spin
        elif mode == 2:
            for i in range(30):
                color = fancy.palette_lookup(palette1, offset + i/29 )
                pixel_strip[i] = color.pack()
            for i in range(12):
                color = fancy.palette_lookup(palette2, offset + i/11 )
                pixel_ring[i] = color.pack()
            if z_angle >= 40:
                offset += 0.25  # Bigger number = faster spin
            else:
                offset += 0.05  # Bigger number = faster spin
        elif mode == 3:
            for i in range(30):
                color = fancy.palette_lookup(palette3, offset + i/29 )
                pixel_strip[i] = color.pack()
            for i in range(12):
                color = fancy.palette_lookup(palette4, offset + i/11 )
                pixel_ring[i] = color.pack()
            if z_angle >= 40:
                offset += 0.25  # Bigger number = faster spin
            else:
                offset += 0.05  # Bigger number = faster spin
        elif mode == 4:
            for i in range(30):
                color = fancy.palette_lookup(palette4, offset + i/29 )
                pixel_strip[i] = color.pack()
            for i in range(12):
                color = fancy.palette_lookup(palette3, offset + i/11 )
                pixel_ring[i] = color.pack()
            if z_angle >= 40:
                offset += 0.25  # Bigger number = faster spin
            else:
                offset += 0.05  # Bigger number = faster spin
        else:
            pixel_strip.fill(WHITE)
            pixel_ring.fill(WHITE)

        pixel_strip.show()
        pixel_ring.show()

    else:
        pixel_strip.fill(0)
        pixel_ring.fill(0)
        mode = 0

    time.sleep(0.05)
