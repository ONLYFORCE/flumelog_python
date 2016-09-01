import svr_log
if __name__ == '__main__':  
    svr_log.g_Errlog.set_file_name('errlog')
    svr_log.g_Errlog.set_service('test log server')
    svr_log.g_Errlog.setout_level('LOG_LEVEL_DEBUG')
    svr_log.g_Errlog.set_asyn(True)
    for i in range(100000): 
      svr_log.LOG_DEBUG('hello world %d',i)
    svr_log.g_Errlog.stop_asyn()
