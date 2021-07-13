"""
Class for the NEOPIXEL LEDs object variablesclass
"""

class LEDVALS:
    RED     = [255, 0, 0]
    GREEN   = [0, 255, 0]
    BLUE    = [0, 0, 255]
    CYAN    = [0, 255, 255]
    VIOLET  = [148, 0, 211]
    FUCHSIA = [255, 0, 255]
    
    DIGITS = { 0: '0111111',
       1: '0001100',
       2: '1011011',
       3: '1011110',
       4: '1101100',
       5: '1110110',
       6: '1110111',
       7: '0011100',
       8: '1111111',
       9: '1111100'
      }
    
    def __init__(self, rgb, brightval):
        # RGB color and brightness variables
        self.Brightval = brightval
        self.rColorval = rgb[0]
        self.gColorval = rgb[1]
        self.bColorval = rgb[2]
        self.rBrightval = 0
        self.gBrightval = 0
        self.bBrightval = 0
 
        self.dotsOn = False
        
        self.RTCTemp = 0
        
        # Set the brightness on start
        self.setBrightness(brightval)
        


    def getDots(self):
        return self.dotsOn
    
    def setDots(self, val):
        self.dotsOn = val
    
    def get_Brightval(self):
        return int(self.Brightval)
    
    def set_Brightval(self, val):
        self.Brightval = val
        
    def get_rColorval(self):
        return int(self.rColorval)
    
    def get_gColorval(self):
        return int(self.gColorval)
    
    def get_bColorval(self):
        return int(self.bColorval)
    
    def set_rColorval(self, val):
        self.rColorval = val
    
    def set_gColorval(self, val):
        self.gColorval = val
    
    def set_bColorval(self, val):
        self.bColorval = val
        
    def set_RTCTemp(self, val):
        self.RTCTemp = val
    
    def get_RTCTemp(self):
        return int(self.RTCTemp)      
        
    def setBrightness(self, brightval):
        self.rColorval = (brightval / 255)*self.rColorval
        self.gColorval = (brightval / 255)*self.gColorval
        self.bColorval = (brightval / 255)*self.bColorval
        self.rBrightval = self.rColorval
        self.gBrightval = self.gColorval
        self.bBrightval = self.bColorval
        brightval = self.Brightval
    
    def updateBrightness(self, brightval):
        self.rColorval = (brightval / 120)*self.rBrightval
        self.gColorval = (brightval / 120)*self.gBrightval
        self.bColorval = (brightval / 120)*self.bBrightval

    def setColor(self, rgb):
        self.rColorval = rgb[0]
        self.gColorval = rgb[1]
        self.bColorval = rgb[2]
        self.rBrightval = self.rColorval
        self.gBrightval = self.gColorval
        self.bBrightval = self.bColorval






