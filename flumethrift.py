
from genpy.flume import ThriftSourceProtocol  
from genpy.flume.ttypes import ThriftFlumeEvent  

import xml.dom.minidom  
  
from thrift.transport import TTransport, TSocket  
from thrift.protocol import TCompactProtocol  
  


  
class _Transport(object):  
    def __init__(self, thrift_host, thrift_port, timeout=None, unix_socket=None):  
        self.thrift_host = thrift_host  
        self.thrift_port = thrift_port  
        self.timeout = timeout  
        self.unix_socket = unix_socket  
          
        self._socket = TSocket.TSocket(self.thrift_host, self.thrift_port, self.unix_socket)  
        self._transport_factory = TTransport.TFramedTransportFactory()  
        self._transport = self._transport_factory.getTransport(self._socket)  
          
    def connect(self):  
        try:  
            if self.timeout:  
                self._socket.setTimeout(self.timeout)  
            if not self.is_open():  
                self._transport = self._transport_factory.getTransport(self._socket)  
                self._transport.open()  
        except Exception, e:  
            print(e)  
            self.close()  
      
    def is_open(self):  
        return self._transport.isOpen()  
      
    def get_transport(self):  
        return self._transport  
      
    def close(self):  
        self._transport.close()  
          
class FlumeClient(object):  
    def __init__(self, thrift_host, thrift_port, timeout=None, unix_socket=None):  
        self._transObj = _Transport(thrift_host, thrift_port, timeout=timeout, unix_socket=unix_socket)  
        self._protocol = TCompactProtocol.TCompactProtocol(trans=self._transObj.get_transport())  
        self.client = ThriftSourceProtocol.Client(iprot=self._protocol, oprot=self._protocol)  
        self.header = dict()

    def add_header(self,**thrift_header):
        for k in thrift_header:
          self.header[k] = thrift_header[k]

    def _make_event(self,strevent):
        tfevent = ThriftFlumeEvent(self.header,strevent)
        return tfevent 

    def _make_events(self,strevents):
        tfevents = [ThriftFlumeEvent(self.header,stri) for stri in strevents]  
        return tfevents

    def send_event(self, strevent):  
        try: 
            self._transObj.connect()   
            tfevent = self._make_event(strevent)
            self.client.append(tfevent)  
        except Exception, e:  
            print(e)  
        finally:  
            self._transObj.connect()  
    def send_event_batch(self, strevents):  
        try: 
            self._transObj.connect()  
            tfevents = self._make_events(strevents) 
            self.client.appendBatch(tfevents)  
        except Exception, e:  
            print(e)  
        finally:  
            self._transObj.connect()  
      
    def close(self):  
        self._transObj.close()  
  
        
        
