import sys, os, time, gevent

from locust import events
from pprint import pprint
from gevent.socket import socket
from gevent.queue import Queue

graphite_queue = Queue()
user_count_map = {}
HOST = os.getenv('GRAPHITE_HOST', '127.0.0.1')
PORT = os.getenv('GRAPHITE_PORT', '2003')

def is_worker():
    return '--slave' in sys.argv or '--worker' in sys.argv

def graphite_worker():
    """The worker pops each item off the queue and sends it to graphite."""
    pprint('[+] Connecting to graphite on (%s:%s)' %(HOST,PORT))

    sock = socket()
    try:
        sock.connect((HOST,int(PORT)))
    except Exception as e :
        raise Exception("Couldn't connect to Graphite server {0} on port {1}: {2}".format(HOST,PORT, e))
    pprint('[+] Done connecting to Graphite.')

    while True:
        data = graphite_queue.get()
        pprint('[+] Graphite_worker: got data {0!r}'.format(data))
        pprint('[+] Send data')
        sock.sendall(data)


def graphite_producer(client_id, data):
    """This take a Locust cliend_id and some data, as give to
    locust event worker_report handler."""
    pass

def setup_graphite():
    """Only the master send data to graphite."""
    if not is_worker():
        gevent.spawn(graphite_worker)
        pprint("[+] Get Events Listener.")
        events.worker_report.add_listener(graphite_producer)
