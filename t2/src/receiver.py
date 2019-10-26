from .protocols.stop_and_wait.receiver import SWReceiver
import time

class Receiver(object):
    def __init__(self, protocol, *args, **kwargs):
        self.protocol = self.load_protocol(protocol)
        self.message = []
        self.recv = []

    def load_protocol(self, name):
        protocol = None
        if name == "STOP_AND_WAIT":
            protocol = SWReceiver(self)
            protocol.state = 'wait_0' 
            
        if name == "GO_BACK_N":
            pass
        if name == "SELECTIVE_REPEAT":
            pass

        return protocol

    def process(self, *args, **kwargs):
        start_ = time.time()
        OFFSET = 5 # us
        OFFSET = OFFSET / 1000000
        for pkg, t in self.recv:
            if start_ - t > -OFFSET/2:
                self.recv.remove([pkg, t])
                self.protocol.process_response(pkg, *args, **kwargs)

    def receive(self, pkg, time, *args, **kwargs):
        if pkg != None:
            self.recv.append([pkg, time])

    def request_pkg(self, *args, **kwargs):
        return self.protocol.get_pkg(*args, **kwargs)