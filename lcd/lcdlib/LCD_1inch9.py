
import time

import numpy as np
from . import lcdconfig

class LCD_1inch9(lcdconfig.RaspberryPi):
    width = 170
    height = 320 
    
    def command(self, cmd):
        self.digital_write(self.DC_PIN, False)
        self.spi_writebyte([cmd])   
        
    def data(self, val):
        self.digital_write(self.DC_PIN, True)
        self.spi_writebyte([val])   
        
    def reset(self):
        """Reset the display"""
        self.digital_write(self.RST_PIN,True)
        time.sleep(0.01)
        self.digital_write(self.RST_PIN,False)
        time.sleep(0.01)
        self.digital_write(self.RST_PIN,True)
        time.sleep(0.01)
        
    def Init(self):
        """Initialize dispaly"""  
        self.module_init()
        self.reset()

        self.command(0x36)
        self.data(0x00)

        self.command(0x3A) 
        self.data(0x55)

        self.command(0xB2)
        self.data(0x0C)
        self.data(0x0C)
        self.data(0x00)
        self.data(0x33)
        self.data(0x33)

        self.command(0xB7)
        self.data(0x35) 

        self.command(0xBB)
        self.data(0x13)

        self.command(0xC0)
        self.data(0x2C)

        self.command(0xC2)
        self.data(0x01)

        self.command(0xC3)
        self.data(0x0B)   

        self.command(0xC4)
        self.data(0x20)

        self.command(0xC6)
        self.data(0x0F) 

        self.command(0xD0)
        self.data(0xA4)
        self.data(0xA1)

        self.command(0xE0)
        self.data(0x00)
        self.data(0x03)
        self.data(0x07)
        self.data(0x08)
        self.data(0x07)
        self.data(0x15)
        self.data(0x2A)
        self.data(0x44)
        self.data(0x42)
        self.data(0x0A)
        self.data(0x17)
        self.data(0x18)
        self.data(0x25)
        self.data(0x27)

        self.command(0xE1)
        self.data(0x00)
        self.data(0x03)
        self.data(0x08)
        self.data(0x07)
        self.data(0x07)
        self.data(0x23)
        self.data(0x2A)
        self.data(0x43)
        self.data(0x42)
        self.data(0x09)
        self.data(0x18)
        self.data(0x17)
        self.data(0x25)
        self.data(0x27)
        
        self.command(0x21)

        self.command(0x11)

        self.command(0x29)
  
    def SetWindows(self, Xstart, Ystart, Xend, Yend, horizontal = 0):
        if horizontal:
            #set the X coordinates
            self.command(0x2A)
            self.data(Xstart>>8)        #Set the horizontal starting point to the high octet
            self.data(Xstart & 0xff)    #Set the horizontal starting point to the low octet
            self.data(Xend-1>>8)        #Set the horizontal end to the high octet
            self.data((Xend-1) & 0xff)  #Set the horizontal end to the low octet 
            #set the Y coordinates
            self.command(0x2B)
            self.data(Ystart+35>>8)
            self.data((Ystart+35 & 0xff))
            self.data(Yend+35-1>>8)
            self.data((Yend+35-1 ) & 0xff )
            self.command(0x2C)    
        else:
            #set the X coordinates
            self.command(0x2A)
            self.data(Xstart+35>>8)         #Set the horizontal starting point to the high octet
            self.data(Xstart+35 & 0xff)     #Set the horizontal starting point to the low octet
            self.data(Xend+35-1>>8)         #Set the horizontal end to the high octet
            self.data((Xend+35 - 1) & 0xff) #Set the horizontal end to the low octet 
            #set the Y coordinates
            self.command(0x2B)
            self.data(Ystart>>8)
            self.data((Ystart & 0xff))
            self.data(Yend -1>>8)
            self.data((Yend - 1) & 0xff )
            self.command(0x2C)

    def ShowImage(self, Image):
        """Set buffer to value of Python Imaging Library image."""
        """Write display buffer to physical display"""
        imwidth, imheight = Image.size
        if imwidth == self.height and imheight ==  self.width:
            img = np.array(Image)
            pix = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)
            pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8), self.np.right_shift(img[...,[1]],5)).reshape(-1, img.shape[1], 1)
            pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0), self.np.right_shift(img[...,[2]],3))
            pix = pix.flatten().tolist()
            
            self.command(0x36)
            self.data(0x70) 
            self.SetWindows(0, 0, self.height,self.width, 1)
            self.digital_write(self.DC_PIN,True)
            for i in range(0,len(pix),4096):
                self.spi_writebyte(pix[i:i+4096])
        else :
            img = np.array(Image)
            pix = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)
            pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8), self.np.right_shift(img[...,[1]],5)).reshape(-1, img.shape[1], 1)
            pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0), self.np.right_shift(img[...,[2]],3))
            pix = pix.flatten().tolist()
            
            self.command(0x36)
            self.data(0x00) 
            self.SetWindows(0, 0, self.width, self.height)
            self.digital_write(self.DC_PIN,True)
        for i in range(0, len(pix), 4096):
            self.spi_writebyte(pix[i: i+4096])
        

    def clear(self):
        """Clear contents of image buffer"""
        _buffer = [0xff] * (self.width*self.height*2)
        self.SetWindows(0, 0, self.width, self.height)
        self.digital_write(self.DC_PIN,True)
        for i in range(0, len(_buffer), 4096):
            self.spi_writebyte(_buffer[i: i+4096])
        
