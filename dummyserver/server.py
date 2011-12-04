#!/usr/bin/env python

"""
Dummy server used for unit testing.
"""

import logging
import os
import sys

from .app import TestingApp


log = logging.getLogger(__name__)

CERTS_PATH = os.path.join(os.path.dirname(__file__), 'certs')
DEFAULT_CERTS = {
    'certfile': os.path.join(CERTS_PATH, 'server.crt'),
    'keyfile': os.path.join(CERTS_PATH, 'server.key'),
}
DEFAULT_CA = os.path.join(CERTS_PATH, 'client.pem')
DEFAULT_CA_BAD = os.path.join(CERTS_PATH, 'client_bad.pem')


def eventlet_server(host="localhost", port=8081, scheme='http', certs=None, **kw):
    import eventlet
    import eventlet.wsgi

    certs = certs or {}

    socket = eventlet.listen((host, port))

    if scheme == 'https':
        socket = eventlet.wrap_ssl(socket, server_side=True, **certs)

    dummy_log_fp = open(os.devnull, 'a')

    return eventlet.wsgi.server(socket, TestingApp(), log=dummy_log_fp, **kw)


def make_server_thread(target, **kw):
    import threading
    t = threading.Thread(target=target, kwargs=kw)
    t.start()
    return t


if __name__ == '__main__':
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler(sys.stderr))

    from urllib3 import get_host

    url = "http://localhost:8081"
    if len(sys.argv) > 1:
        url = sys.argv[1]

    scheme, host, port = get_host(url)
    eventlet_server(scheme=scheme, host=host, port=port)
