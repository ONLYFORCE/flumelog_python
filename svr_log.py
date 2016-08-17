import log
import sys
loglevelinfo ={'LOG_LEVEL_FATAL':0, 'LOG_LEVEL_ALERT':1,'LOG_LEVEL_ERR':2,'LOG_LEVEL_WARN':3,'LOG_LEVEL_INFO':4, 'LOG_LEVEL_DEBUG':5}

class ErrLog(log.Log):
      def __init__(self,iOutLevel = None):
          log.Log.__init__(self)
          self._logleveldefs ={'LOG_LEVEL_FATAL':'fatal','LOG_LEVEL_ALERT':'alert','LOG_LEVEL_ERR':'err','LOG_LEVEL_WARN':'warn','LOG_LEVEL_INFO':'info', 'LOG_LEVEL_DEBUG':'debug' }
          self._iOutLevel = iOutLevel

      def _is_enable(self,slevel):
          return (loglevelinfo[slevel] <= self._iOutLevel) and self.is_enable()

      def setout_level(self,ilevel):
          self._iOutLevel = ilevel

      def _get_level_in_str(self,slevel):
          return self._logleveldefs[slevel]
g_Errlog = ErrLog()
g_VisitLog = ErrLog()
g_StatisLog = ErrLog()

def LOG_LEVEL(slevel,fmt,*arg):
    if g_Errlog._is_enable(slevel):
       strlevel = g_Errlog._get_level_in_str(slevel)
       line = sys._getframe().f_lineno 
       strline  = '%d'%line
       str2 = '[' + strlevel + ']'+ ' ' + sys._getframe().f_code.co_filename + '.' + strline + '(' + sys._getframe().f_code.co_name  + ')'
       str3 = str2 + fmt
       g_Errlog.wirte(str3,arg)


def FATAL(fmt,*arg):
    LOG_LEVEL('LOG_LEVEL_FATAL',fmt,*arg)

def ALERT(fmt,*arg):
    LOG_LEVEL('LOG_LEVEL_ALERT',fmt,*arg)

def ERROR(fmt,*arg):
    LOG_LEVEL('LOG_LEVEL_ERR',fmt,*arg)

def WARNING(fmt,*arg):
    LOG_LEVEL('LOG_LEVEL_WARN',fmt,*arg)

def NOTICE(fmt,*arg):
    LOG_LEVEL('LOG_LEVEL_INFO',fmt,*arg)

def DEBUG(fmt,*arg):
    LOG_LEVEL('LOG_LEVEL_DEBUG',fmt,*arg)



def LOG_FATAL(fmt,*arg):
    LOG_LEVEL('LOG_LEVEL_FATAL',fmt,*arg)

def LOG_ALERT(fmt,*arg):
    LOG_LEVEL('LOG_LEVEL_ALERT',fmt,*arg)

def LOG_ERROR(fmt,*arg):
    LOG_LEVEL('LOG_LEVEL_ERR',fmt,*arg)

def LOG_WARNING(fmt,*arg):
    LOG_LEVEL('LOG_LEVEL_WARN',fmt,*arg)

def LOG_NOTICE(fmt,*arg):
    LOG_LEVEL('LOG_LEVEL_INFO',fmt,*arg)

def LOG_DEBUG(fmt,*arg):
    LOG_LEVEL('LOG_LEVEL_DEBUG',fmt,*arg)

def LOG_LEVEL_V(level,fmt,*arg):
    if g_VisitLog._is_enable(level):                          
       g_Errlog.wirte(fmt,*arg)


def LOG_FATAL_V(fmt,*arg):
    LOG_LEVEL_V('LOG_LEVEL_FATAL',fmt,*arg)

def LOG_ALERT_V(fmt,*arg):
    LOG_LEVEL_V('LOG_LEVEL_ALERT',fmt,*arg)

def LOG_ERROR_V(fmt,*arg):
    LOG_LEVEL_V('LOG_LEVEL_ERR',fmt,*arg)

def LOG_WARNING_V(fmt,*arg):
    LOG_LEVEL_V('LOG_LEVEL_WARN',fmt,*arg)

def LOG_NOTICE_V(fmt,*arg):
    LOG_LEVEL_V('LOG_LEVEL_INFO',fmt,*arg)

def LOG_DEBUG_V(fmt,*arg):
    LOG_LEVEL_V('LOG_LEVEL_DEBUG',fmt,*arg)



            
