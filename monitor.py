import time

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import psutil

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from subprocess import check_output





# Raspberry Pi software SPI config:
SCLK = 17
DIN = 18
DC = 27
RST = 23
CS = 8

# Software SPI usage (defaults to bit-bang SPI interface):
disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Initialize library.
disp.begin(contrast=100)

# Clear display.
disp.clear()
disp.display()

image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
draw = ImageDraw.Draw(image)

#font = ImageFont.truetype('res/fonts/silkscreen.ttf', 8)
#font = ImageFont.truetype('res/fonts/retro_c.ttf', 7)
#font = ImageFont.truetype('res/fonts/minecraftia.ttf', 8)
#font = ImageFont.truetype('res/fonts/visitor2.ttf', 12)
#font = ImageFont.truetype('res/fonts/type_writer.ttf', 8)
font = ImageFont.truetype('res/fonts/pixelart.ttf', 8)

# data
currentTime = 0

ipAddressUpdateInterval = 300
ramUsageUpdateInterval = 10
cpuUsageUpdateInterval = 2

ipAddressValue = ""
ramUsageValue = ""
cpuUsageValue = ""

def updateMonitoringData(force):
	global ipAddressValue
	global ramUsageValue
	global cpuUsageValue
	
	if (force or currentTime % ipAddressUpdateInterval == 0):
		ipAddressValue = "ip: " + check_output(['hostname', '-I'])
	if (force or currentTime % ramUsageUpdateInterval == 0):
		ramUsageValue  = "ram: " + str(psutil.virtual_memory().used / 1024 / 1024 ) + "/" + str(psutil.virtual_memory().total / 1024 / 1024 ) + "MB"
	if (force or currentTime % cpuUsageUpdateInterval == 0):	
		cpuUsageValue  = "cpu: " + str(psutil.cpu_percent()) + "%"



def redraw():
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	
	renderData()
	
	disp.image(image)
	disp.display()
	

def renderTextLine(line, text):
	draw.text((2,( line * 14 ) + 2), text, font=font, fill=0)
	draw.line((2,( line * 14 ) + 12,LCD.LCDWIDTH,( line * 14 ) + 12), fill=0)

def renderData():
	updateMonitoringData(False)
	
	renderTextLine( 0, ipAddressValue )
	renderTextLine( 1, cpuUsageValue )
	renderTextLine( 2, ramUsageValue )



updateMonitoringData(True)


print('Press Ctrl-C to quit.')
while True:
	currentTime+=1
	redraw()
	time.sleep(1.0)
