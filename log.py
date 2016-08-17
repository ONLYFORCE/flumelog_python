#coding=utf-8
import flumethrift 
import xml.dom.minidom
import threading
import time
import datetime
import Queue

          

g_queue = Queue.Queue()

class Log(object):
      def __init__(self,bufferlength = 1000,logbuffer = None,confpath = "../etc/serverconf/flume_log.xml",asyn = False):
          self._log_batch = bufferlength
          self._logbuffer = []
          self._clientlist = []
          self._confpath = confpath
          self.load_config(self._confpath)
          self.idx = 0
          self._asyn = asyn

                      
      
          
                 
      def _get_date_time_str(self):
          Atime=datetime.datetime.now().microsecond/1000   
          Btime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) 
          strtime = str(Btime)+':'+str(Atime) 
          return strtime




      def _set_log_batch(self,lenth):
          self._log_batch = lenth



      def set_file_name(self,filename):
          self._set_property('filename',filename)
     
      def set_service(self,service):
          self._set_property('service',service)



      def _set_property(self,key,value):
          header ={key:value}
          for client in self._clientlist:
              client.add_header(**header)


      def add_log_server(self,ipadd,port):
          self._clientlist.append(flumethrift.FlumeClient(ipadd,port))
       


      def load_config(self,configpath):
          if not configpath: 
              print 'not set config path'
              return
          DOMTree = xml.dom.minidom.parse(configpath)
          collection = DOMTree.documentElement
          serverinfos = collection.getElementsByTagName('logServer')
          for server in serverinfos:
              port = server.getAttribute('port')
              ip = server.getAttribute('ip')
              self.add_log_server(ip,int(port))

      def is_enable(self):
          return True


      def set_asyn(self,asyn): 
          self._asyn = asyn
          self._thread_runing = True
          num = len(self._clientlist)
          id = 0
          self._queue = Queue.Queue() 
          while(id < num):
             pr = threading.Thread(target = Log.write_thread,args=(self,id))
             pr.start()
             id = id+1





      def write_thread(self,id):
          while self._thread_runing:
            if g_queue.qsize() > self._log_batch:
                i = 0
                strevents = []
                while(i < self._log_batch):
                 strevents.append(g_queue.get())
                 i = i+1
                self._clientlist[id].send_event_batch(strevents)

          while(g_queue.qsize() > self._log_batch):
            strevents = []
            i = 0
            while i < self._log_batch:
             tupl = g_queue.get()
             strevents.append(tupl)
             i=i+1
            self._clientlist[id].send_event_batch(strevents)


          strevents = []
          while(g_queue.qsize() > 0):
           tupl = g_queue.get()
           strevents.append(tupl)
          self._clientlist[id].send_event_batch(strevents)
        
      def stop_asyn(self):
          self._thread_runing = False


      def wirte(self,strs,arg):
          strtime = self._get_date_time_str()
          strformat = strs % arg
          str3 = strtime + strformat
          if not self._asyn:
              self._logbuffer.append(str3)
              if len(self._logbuffer) >= self._log_batch:
                 self.idx = self.idx % len(self._clientlist)
                 self._clientlist[self.idx].send_event_batch(self._logbuffer)
                 self.idx = self.idx+1
                 self._logbuffer = []
          else:
               g_queue.put(str3)
