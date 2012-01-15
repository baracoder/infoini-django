import serial
from struct import unpack
from time import sleep
import SocketServer
import threading
import json

#######################################################################
## TCP Kommunikation
class SensorServerHandler(SocketServer.BaseRequestHandler):
    """
    Sendet aktuelle Sensordaten im JSON Format
    """

    def handle(self):
        # TODO
        print "request"
        data = json.dumps(get_all())
        self.request.send(data)

class SensorThreadServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

#######################################################################
## Werteerfassung

s = serial.Serial( port="/dev/ttyS0")
s.setRTS()

def ist_offen():
    global s
    return not s.getCTS()

def potinfo():
    pots = [
        {'port':"/dev/ttyUSB0",'val_min':552,'val_max':900},
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
            info_list.append({'status':"vorhanden", 'level':""+str(l)})
            continue

    return info_list


ser_ports = {}

def _get_pot_data(s):
    return False
    if not s in ser_ports.keys():
        try:
            print "open"
            ser_ports[s] = serial.Serial(port=s)
            ser_ports[s].open()
        except Exception:
            return False

    while ser_ports[s].isOpen():
        ser_ports[s].flush()
        ser_ports[s].flushInput()
        if ser_ports[s].read()== '\xff':
            b1=ser_ports[s].read()
            b2=ser_ports[s].read()
            val_tuple=unpack('h',''.join([b2,b1]))
            return val_tuple[0]
    return False

def _get_pot_level(val,val_min, val_max):
    return round( 100* (val-val_min) / (val_max-val_min) )

def get_all():
    return {'tuer_offen':ist_offen(), 'cafepots':potinfo()}


#######################################################################
## Logging

def log(data):
    # TODO
    pass



#######################################################################
## Start
if __name__ == "__main__":

    ## Server starten
    # port CAFE, 51966
    HOST, PORT = "localhost", 0xCAFE
    server = SensorThreadServer((HOST, PORT), SensorServerHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()


    try:
        while True:
            print "werte erfassen"
            data = get_all()
            if False: log(data)
            sleep(1)
    except KeyboardInterrupt:
        server.shutdown()
        server_thread.join()


