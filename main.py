import network
import veml7700
import utime
import math
from credentials import CREDENTIALS
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

# The LEDs values object
# Wifi credentials
ledvals = LEDVALS(LEDVALS.FUCHSIA, 255)
creds = CREDENTIALS

# Network setup
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(creds.SSID, creds.PSWD)
    while not sta_if.isconnected():	
        print(".", end="")
      		
print('network config:', sta_if.ifconfig())



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
    #Get the time from the RTC, get_time(True) updates system time
    DS3231.get_time(True)
    clockTime = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)

    
    #Offsets for individual numbers
    DIG_1 = 0
    DIG_2 = 7
    DIG_3 = 16
    DIG_4 = 23
    
    fMdig = truncate(clockTime[4] /10)
    sMdig = clockTime[4]  % 10
    
    fHdig = truncate((clockTime[3])  /10)
    sHdig = (clockTime[3])  % 10
    
    updateLED(DIG_1, sMdig)
    updateLED(DIG_2, round(fMdig))
    updateLED(DIG_3, sHdig)
    updateLED(DIG_4, round(fHdig))



def updateDots():
    global ledvalues
    
    dotsOn = ledvals.getDots()

    if dotsOn != True: ledvals.setDots(True) 
    else: ledvals.setDots(False)
    
    r_val = ledvals.get_rColorval()
    g_val = ledvals.get_gColorval()
    b_val = ledvals.get_bColorval()
    
    if r_val > 8: r_val = int(r_val*0.3)
    if g_val > 8: g_val = int(g_val*0.3)
    if b_val > 8: b_val = int(b_val*0.3)
    #print(r_val, g_val, b_val)
  
    if dotsOn:
        LEDs[14] = (r_val, g_val, b_val)
        LEDs[15] = (r_val, g_val, b_val)
    else:
        LEDs[14] = (0,0,0)
        LEDs[15] = (0,0,0)
      


def updateBrightness():
    #lux = 0
    
    if VEML.read_lux() < 8:
        lux = 8
    elif VEML.read_lux() > 120:
        lux = 120
    else:
        lux = VEML.read_lux()
    #print(VEML.read_lux())   
    #print(lux)
    ledvals.updateBrightness(lux)
    
    
    
def updateColor(oldval):
    global ledvals
    
    val = round((DS3231.get_temperature())-3)
    
    # Only update if the temp has changed
    if val != oldval:
        print("Color Update")
   
        if val == 23:
            ledvals.setColor(ledvals.BLUE)
            updateBrightness()
        if val == 24:
            ledvals.setColor(ledvals.VIOLET)
            updateBrightness()
        if val == 25:
            ledvals.setColor(ledvals.CYAN)
            updateBrightness()
        if val == 26:
            ledvals.setColor(ledvals.GREEN)
            updateBrightness()
        if val == 27:
            ledvals.setColor(ledvals.FUCHSIA)
            updateBrightness()
        if val == 28:
            ledvals.setColor(ledvals.RED)
            updateBrightness()
        #print(val)
    
    # Set the new temp value
    ledvals.set_RTCTemp(val) 



def updateRTC():
    # Synchronise system time and the DS3231 RTC
    import ntptime
    utc_shift = 10

    print("Local time before synchronization：%s" %str(utime.localtime()))
    ntptime.settime()
    print("Local time after synchronization：%s" %str(utime.localtime()))

    DS3231.save_time()



# Global for the millisecond and second timer loop
milliSec = 0
oneSec = 0

# While loop for clock update
while True:
    # 1000 millisecond or second function
    millis = int(utime.ticks_ms())
    secs = utime.time()
    # Update the LEDx
    LEDs.write()
    
    # Sync the RTC every 10 minutes
    if secs - oneSec >= 3600:
        oneSec = secs
        updateRTC()
    
    # 1 second loop
    if millis - milliSec >= 1000:
        milliSec = millis
        updateDots()        
        updateClock()
        updateBrightness()
        updateColor(ledvals.get_RTCTemp())
        

        
