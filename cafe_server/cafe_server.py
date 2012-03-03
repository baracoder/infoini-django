# coding=utf-8
import serial
from time import sleep
import SocketServer
import threading
import json

#######################################################################
## TCP Kommunikation
class TCPRequestHandler(SocketServer.BaseRequestHandler):
    """
    Sendet aktuelle Sensordaten im JSON Format
    """
    def __init__(self, callback, *args, **keys):
        self.callback = callback
        SocketServer.BaseRequestHandler.__init__(self, *args, **keys)

    def handle(self):
        data = self.callback()
        print "request: " + data
        self.request.send(data)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


#######################################################################
## Sensoren

class Sensor(object):
    """Sensor mit Zwischenspeicher für letzten Wert"""
    _name = "Unbenannt"
    _value = 0

    def __init__(self,name):
        self._name = name

    def getData(self):
        """gibt aktuelle Daten strukturiert zurück"""
        return self._value

    def update(self):
        """Aktualisiert Wert"""
        pass

    def save(self):
        """Speichert Wert in der DB"""
        pass

class TuerSensor(Sensor):
    """Benutzt CTS und RTS Pin am Serielanschluss"""

    def __init__(self,name):
        self._s = serial.Serial( port="/dev/ttyS0")
        self._s.setRTS()

    def ist_offen(self):
        return not self._s.getCTS()

class PotSensor(Sensor):
    """Benutzt Arduino Objekt"""
    def __init__(self,name,arduino,index):
        self._name = name
        self._arduino = arduino
        self._index = index

        # TODO aus Datenbank lesen
        pots = [
            {'val_min':552,'val_max':600},
            {'val_min':0,'val_max':600},
        ]
        self._pot = pots[index]

    def _get_pot_level(self,val):
        val_min = self._pot['val_min']
        val_max = self._pot['val_max']
        return round( 100* (val-val_min) / (val_max-val_min) )

    def getData(self):
        pods = self._arduino.getCoffepots()
        if len(pods)-1 < self._index:
            d = False
        else:
            d = pods[self._index]

        if d == False:
            return {'status':"keine Info", 'level':0}
        if d < self._pot['val_min']:
            return {'status':"nicht vorhanden", 'level':0}
        if d > self._pot['val_max']:
            return {'status':"keine Info", 'level':0}
        if d >= self._pot['val_min']:
            l=self._get_pot_level(d)
            return {'status':"vorhanden", 'level':l}


#######################################################################
## Datenaufbereitung

class Arduino(object):
    def __init__(self):
        self._cofepots = []
        self._tueroffen = False
        self._status = 0
        # öffne schnittstelle


    def request_line(self):
        # forde zeile an
        # zeile auslesen
        pass

    def _parse(self,line):
        # TODO
        # parse zeile
        # werte parsen
        # bei fehler False, sonst true
        return False

    def getCoffepots(self):
        return self._cofepots

    def getTueroffen(self):
        return self._tueroffen

    def getStatus(self):
        return self._status


#######################################################################
## Server

class CafeServer(object):
    """Hauptklasse"""

    def __init__(self):
        """Erzeugt Sensoren und Quellen"""
        self._arduino = Arduino()
        self._coffepots = [
                           PotSensor("Pot-1",self._arduino,0), 
                           PotSensor("Pot-2",self._arduino,1)]
        self._tuer = TuerSensor("Tür")

    def update(self):
        """Aktualisiert Werte und loggt ggf Fehler"""
        if not self._arduino.request_line():
            # TODO fehler loggen
            pass

    def _getPots(self):
        return [p.getData() for p in self._coffepots]

    def getData(self):
        return {'tuer_offen':self._tuer.ist_offen(), 'cafepots':self._getPots()}


    def getJson(self):
        return json.dumps(self.getData())



#######################################################################
## Start
if __name__ == "__main__":

    cafeserver = CafeServer()

    ## Server starten
    # port CAFE, 51966
    HOST, PORT = "localhost", 0xCAFE
    #server = SensorThreadServer((HOST, PORT), SensorServerHandler(cafeserver))
    server = ThreadedTCPServer((HOST, PORT), lambda *args, **keys: TCPRequestHandler(cafeserver.getJson, *args, **keys))
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()


    try:
        while True:
            print "werte erfassen"
            cafeserver.update()
            sleep(1)
    except KeyboardInterrupt:
        server.shutdown()
        server_thread.join()


