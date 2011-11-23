import serial

s = serial.Serial( port="/dev/ttyS0")
s.setRTS()

# TODO: cache implementieren

def ist_offen():
    global s
    return not s.getCTS()

def potinfo():
    pots = [
        {'port':"/dev/ttyUSB0",'val_min':0,'val_max':800},
        {'port':"/dev/ttyUSB1",'val_min':0,'val_max':800},
    ]

    info_list = []

    for pot in pots:
        d=_get_pot_data(pot['port'])

        if d == False:
            info_list.append({'status':"keine info", 'level':"0"})
            continue
        if d < pot['val_min']:
            info_list.append({'status':"nicht vorhanden", 'level':"0"})
            continue
        if d >= pot['val_min']:
            l=_get_pot_level(d,pot['val_min'],pot['val_max'])
            info_list.append({'status':"vorhanden", 'level':""+l})
            continue

    return info_list


def _get_pot_data(ser_port):
    try:
        ser = serial.Serial(port=ser_port)
        ser.open()
    except Exception:
        return False

    while ser.isOpen():
        if ser.read()== '\xff':
            b1=s.read()
            b2=s.read()
            val_tuple=unpack('h',''.join([b2,b1]))
            return val_tuple[0]

def _get_pot_level(val,val_min, val_max):
    return (val-val_min)/(val_max-val_min)
