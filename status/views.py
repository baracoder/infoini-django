# coding=utf-8
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page


import socket
import json

def get_all():
    HOST, PORT = "localhost", 0xCAFE

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
        received = sock.recv(1024)
    finally:
        sock.close()
    return json.loads(received)


@cache_page(2) # für 2 sekunden cachen um spitzen besser abfangen zu können
def status(request):
    return render_to_response('status.xml',get_all(), mimetype='text/xml; charset=utf-8')

@cache_page(2) # für 2 sekunden cachen um spitzen besser abfangen zu können
def status_html(request):
    return render_to_response('status.html',get_all())


