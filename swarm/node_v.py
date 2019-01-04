from multiprocessing.connection import wait


class Node:
    """
    A wrapper class for node data to pass to user
    """
    def __init__(s, name, pipes):
        s.name = name
        s.pipes = pipes

    def send(s, addr, msg):
        s.pipes[addr].send(msg)

    def recv(s, addr=None):
        if addr:
            return s.pipes[addr].recv()
        else:
            pipes = [s.pipes[item] for item in s.pipes if s.pipes[item]] 
            for waiter in wait(pipes):
                msg = waiter.recv()
                return msg


def run_node(name, function, pipes):
    """
    A function that wraps the user's function that to be
    executed in this node.
    Parameters
    ---------
    idx: int
        index of the process, ie it's address
    function: a function to run
    pipe: a interface for communication
    """

    node = Node(name, pipes)
    print("node %s started" % name)
    ret = function(node)
    print('node %s exited' % name)
    return ret