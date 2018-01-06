from RPi import GPIO
from RPLCD.gpio import CharLCD
import time

GPIO.setwarnings(False)

lcd = CharLCD(pin_rs=22, pin_rw=24, pin_e=23, pins_data=[21, 16, 12, 20],
              numbering_mode=GPIO.BCM,

cols=16, rows=2, dotsize=8,
              charmap='A02',
              auto_linebreaks=True)

lcd.write_string('Mahoney & Luke\r\n  are great!')

