import serial

s = serial.Serial( port="/dev/ttyS0")

def ist_offen():
    s.setRTS()
    return s.getCTS()
