import serial

s = serial.Serial( port="/dev/ttyS0")
s.setRTS()

def ist_offen():
    global s
    return not s.getCTS()

def potinfo():
    return [
    {'status':"keine info", 'level':"0"},
    {'status':"keine info", "level":"0"},
    ]

