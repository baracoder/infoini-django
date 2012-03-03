# coding=utf-8

usage = """Usage: arduino_emu.py PORT
Einfacher Emulator für die Kommunikation des CAFE-Servers
mit dem Arduino.

Zum Testen kann ein tty verwendet werden.  socat kann ttys mit einander
verbinden:

    socat -d -d pty,raw,echo=0 pty,raw,echo=0

die Namen der beiden ttys werden beim Start ausgegeben

"""

import sys

if len(sys.argv)>1:
    port = sys.argv[1]
else:
    print usage
    sys.exit(1)

import serial
import random
from time import sleep


s = serial.Serial(port=port)
s.open()

answers = [
    "ACK pots:[0,570,234],[1,400,345] tueroffen:0 stat:0",
    "ACK pots:[0,570,234],[1,400,345] tueroffen:1 stat:200",
    "ACK pots:[0,570,234],[1,2345,345] tueroffen:0 stat:200",
    "ACK pots:[0,809,234],[1,2345,345] tueroffen:1 stat:x",
    "FAIL",
    "asdfasdfs",
    "",
    "                                                                 ",
]
for i in range(20):
    answers.append("ACK pots:[0,"+str(random.randrange(560,600))+",234],[1,"
        +str(random.randrange(600))+",345] tueroffen:1 stat:200")

while True:
    s.flushInput()
    s.flushOutput()
    print s.readline()
    a = random.choice(answers)
    print a
    s.write(a+'\n')
    sleep(0.1)
