import network
import veml7700
import utime
import math
from ledvals import LEDVALS
from machine import Pin, I2C, Timer
from neopixel import NeoPixel
from ds3231_port import DS3231


# Setup the hardware pins for the LED strip
pin = Pin(13, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
LEDs = NeoPixel(pin, 30)   # create NeoPixel driver on GPIO0 for 8 pixels


# Setup the hardware pins for the I2C comms bus
scl_pin = Pin(22, pull=Pin.PULL_UP, mode=Pin.OPEN_DRAIN)
sda_pin = Pin(23, pull=Pin.PULL_UP, mode=Pin.OPEN_DRAIN)
i2c = I2C(1, scl=scl_pin, sda=sda_pin)

# The VEML light sensor object
DS3231 = DS3231(i2c)
VEML = veml7700.VEML7700(address=0x10, i2c=i2c, it=100, gain=1/8)

# Network setup
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('SSID', 'PASSWORD')
    while not sta_if.isconnected():	
        print(".", end="")
      		
print('network config:', sta_if.ifconfig())

# The LEDs values object
ledvals = LEDVALS(LEDVALS.FUCHSIA, 255)



def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(int(n * multiplier) / multiplier)



def updateLED(index, digit):
    #Data dictionary for the digit byte array
    global ledvals
    
    digits = ledvals.DIGITS
    
    #Get the led array values from the led object
    r_val = ledvals.get_rColorval()
    g_val = ledvals.get_gColorval()
    b_val = ledvals.get_bColorval()   
    
    for j in range(7):
        if (digits[digit][j] == "1"):
            LEDs[j+index] = (r_val, g_val, b_val)
        else:
            LEDs[j+index] = (0,0,0)
            
            
            
def updateClock():
    # Variable to adjust local time
    
    utc_shift = 10
    #Get the time from the system
    clockTime = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
 
    #Offsets for individual numbers
    DIG_1 = 0
    DIG_2 = 7
    DIG_3 = 16
    DIG_4 = 23

    fMdig = truncate(clockTime[4] /10)
    sMdig = clockTime[4]  % 10
    
    fHdig = truncate(clockTime[3]  /10)
    sHdig = clockTime[3]  % 10
    
    updateLED(DIG_1, sMdig)
    updateLED(DIG_2, round(fMdig))
    updateLED(DIG_3, sHdig)
    updateLED(DIG_4, round(fHdig))



def updateDots():
    global ledvalues
    
    dotsOn = ledvals.getDots()

    if dotsOn != True: ledvals.setDots(True) 
    else: ledvals.setDots(False)
    
    #Get the led array values from the led object
    r_val = int(ledvals.get_rColorval()*0.3)
    g_val = int(ledvals.get_gColorval()*0.3)
    b_val = int(ledvals.get_bColorval()*0.3)
    
  
    if dotsOn:
        LEDs[14] = (r_val, g_val, b_val)
        LEDs[15] = (r_val, g_val, b_val)
    else:
        LEDs[14] = (0,0,0)
        LEDs[15] = (0,0,0)
      


def updateBrightness():
    print(VEML.read_lux())
    
    if VEML.read_lux() < 8:
        lux = 8
    if VEML.read_lux() > 120:
        lux = 120
    else:
        lux = VEML.read_lux()
        
    #print((lux / 120)* ledvals.get_Brightval())
    ledvals.updateBrightness(lux)
    
    
    
def updateColor(newval):
    global ledvals
    val = round((DS3231.get_temperature())-3)
    
    print(val)
    print (ledvals.get_gColorval())
    
    if val != newval:
        if val == 23: ledvals.setColor(ledvals.BLUE)
        if val == 24: ledvals.setColor(ledvals.VIOLET)
        if val == 25: ledvals.setColor(ledvals.CYAN)
        if val == 26: ledvals.setColor(ledvals.GREEN)
        if val == 27: ledvals.setColor(ledvals.FUCHSIA)
        if val == 28: ledvals.setColor(ledvals.RED)
        return val
    
    return newval




def updateRTC():
    # Synchronise time and the DS3231 RTC
    import ntptime
    utc_shift = 10

    print("Local time before synchronization：%s" %str(utime.localtime()))
    ntptime.settime()
    print("Local time after synchronization：%s" %str(utime.localtime()))

    #localTime = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
    DS3231.save_time()

    print('Initial values')
    print('DS3231 time:', DS3231.get_time())
    #print('Board time: ', localTime)



# Global integer for the millisecond timer loop
oneSec = 0

# On start sync RTC and time
updateRTC()

#ledvals.set_rColorval(255)
#ledvals.set_bColorval(255)
#ledvals.setBrightness(1)
temp=0

while True:
    # 1000 millisecond or second function
    current = int(utime.ticks_ms())
    LEDs.write()
    
    
    # 1 second loop
    if current - oneSec >= 1000:
        oneSec = current
        updateDots()        
        updateClock()
        updateBrightness()
        temp = updateColor(temp)
