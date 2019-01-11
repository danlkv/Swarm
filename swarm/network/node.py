
from sys import argv
import time
import socket
import socketserver
from multiprocessing.dummy import Process as Thread, Pipe
from .piped_server import PipedThreadedServer

class Node:

        def __init__(s,
                func,
                name,
                host,
                pid,
                port,
                network ):

            s.func = func
            s.name = name
            s.host = host
            s.network = network
            s.pid = pid
            s.port = port

        def start(s):
            s._print("starting...")
            s._start_threads()
            # this will be replaced by connection establishment
            time.sleep(0.2)
            ret = s.func(s)
            s._print('user func returned',ret)
            return ret

        def _start_threads(s):
            s.server_pipe, pipe_end = Pipe(duplex=False)
            s.server = PipedThreadedServer(s.port, pipe_end)

        def _print(s,*args):
            print("<<node %s"%s.name,*args)

        def _get_node_by_name(s,name):
            r = [n for n in s.network if n['name']==name]
            assert len(r)==1, 'Wrong network info in node'+s.name
            return r[0]

        def _send_to_node(s, data, node):
            host = node['host']
            port = node['port']
            s._print('sending to'+host+':'+str(port))

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, int(port) ))
                sock.sendall(bytes(data + "\n", "utf-8"))
                sock.shutdown(socket.SHUT_RDWR)

        def send(s, to, data):
            node = s._get_node_by_name(to)
            s._send_to_node(data, node)

        def recv(s):
            bytes = s.server_pipe.recv()
            # now we send oly strings
            # TODO: send pickle
            return bytes.decode('utf-8')