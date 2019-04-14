import time

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import psutil
import math
import requests
import json
import time


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from subprocess import check_output
from gpiozero import CPUTemperature
from wireless import Wireless

wireless = Wireless()

print("kek")
