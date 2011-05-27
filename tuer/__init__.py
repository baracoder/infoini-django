import serial

s = serial.Serial( port="/dev/ttyS0")
s.setRTS()

def ist_offen():
    global s
    return not s.getCTS()
