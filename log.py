import sys
sys.path.append('./swig')
import timestr
import flumethrift 
import xml.dom.minidom
import time
import datetime
import Queue
import multiprocessing
g_process_runing = multiprocessing.Value('i',1)
g_queue =multiprocessing.Queue()
g_lock = multiprocessing.Lock()
g_prlist = []
g_logbuffer = []
class Log(object):
      def __init__(self,bufferlength = 1000,logbuffer = None,confpath = "flume_log.xml",asyn = False):
          self._log_batch = bufferlength
          self._logbuffer = []
          self._clientlist = []
          self._confpath = confpath
          self.load_config(self._confpath)
          self.idx = 0
          self._asyn = False
      def _get_date_time_str(self):
          #strtime =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
          return timestr.GetDateTimeStr()


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
              global g_logbuffer
              g_logbuffer.append(str3)
              if len(g_logbuffer) >= self._log_batch:
                 g_queue.put(g_logbuffer,False)
                 g_logbuffer = []
     
      def set_asyn(self,asyn):
          self._asyn = asyn
          if asyn :
            g_process_runing.value = 1 #共享变量
            num = len(self._clientlist)
            id = 0
            while(id < num):
               pr = multiprocessing.Process(target = write_Process,args=(g_lock,g_queue,id,g_process_runing))
               pr.start()
               id = id+1
               g_prlist.append(pr)
      def stop_asyn(self):
           g_process_runing.value = 0
           for pr in g_prlist:
            pr.join()  
           g_queue.close()


def write_Process(g_lock,g_queue,id,g_process_runing): 
#####加锁实现方法 每次put log_batch个str
    log = Log()
    while g_process_runing.value:
      try:
          strevents = g_queue.get(False)
          if strevents:
              log._clientlist[id].send_event_batch(strevents)
              strevents = []
      except Queue.Empty:
                   pass
    while not g_queue.empty():
        try:
            strevents = g_queue.get(False)
            if strevents:
                log._clientlist[id].send_event_batch(strevents)
                strevents = []
        except Queue.Empty:
                     pass

####加锁的多线程是使用方法，加锁的原因是因为每次put的是一个str，而不是上面实现的每次put log_batch个str    
  #log = Log()   
  #while(1):
  #  g_lock.acquire()
  #  queue_size = g_queue.qsize()
  #  sendcount = log._log_batch
  #  if g_process_runing.value:
  #      if queue_size < log._log_batch:
  #         g_lock.release()
  #         continue
  #  else:
  #      if queue_size <= 0:
  #         g_lock.release()
  #         break    
  #      if queue_size < log._log_batch:
  #         sendcount = queue_size
  #  strevents=[]          
  #  for i in xrange(sendcount):
  #     tupl = g_queue.get()
  #     strevents.append(tupl)
  #  g_lock.release()
  #  log._clientlist[id].send_event_batch(strevents)


#####另一种实现方法，不加锁，而每次put的也是一个str
#strevents = []
#log = Log()
#while 1:
#  if g_process_runing.value:
#     try: 
#        strevents.append(g_queue.get(False))
#     except Queue.Empty:
#          pass
#     if len(strevents) >= log._log_batch:
#        log._clientlist[id].send_event_batch(strevents)
#        strevents =[] 
#  else:
#       if strevents:
#          log._clientlist[id].send_event_batch(strevents)
#          strevents = []
#       if g_queue.empty():
#          break;
#       else:
#           while 1:
#               try: 
#                  strevents.append(g_queue.get(False))
#               except Queue.Empty:
#                    break
#               if len(strevents) >= log._log_batch:
#                  log._clientlist[id].send_event_batch(strevents)
#                  strevents =[] 
#           if strevents:
#               log._clientlist[id].send_event_batch(strevents)
#           break

          


        
