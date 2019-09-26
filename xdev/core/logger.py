from datetime import datetime
import traceback

class logger(object):
    SCOPE_MSG= "LOG"
    SCOPE_WRN = "WRN"
    SCOPE_ERR = "ERR"
    PREFIX_SEPARATOR = "/"

    __prefix = "-"

    def __init__(self, prefix, fileoutputpath=None, debug = False):
        self.__prefix = prefix
        self.__fileoutputpath = None
        self.__fileoutput = None
        self.set_debug(debug)
        self.set_path(self.__fileoutputpath)

    def __del__(self):
        if self.__fileoutput != None:
            self.__fileoutput.close()

    @classmethod
    def from_prefix(cls,prefix:str):
        return cls(prefix)

    @classmethod
    def from_parent(cls,prefix,parentLogger):
        if parentLogger != None:
            assert isinstance(parentLogger,cls), "Parent object has to be of " + type(cls) + " type"
            prefix = parentLogger.prefix + cls.PREFIX_SEPARATOR + prefix
        return cls(prefix)

    def set_debug(self,debug):
        assert isinstance(debug,bool), "Debug parameter shall be of bool value"
        self.__debug = debug

    def set_path(self,fileoutputpath):
        if fileoutputpath != None:
            assert isinstance(fileoutputpath,str), "log file path has to be a string, '%s' given" % str(type(fileoutputpath))
            self.__fileoutputpath = fileoutputpath
            self.__fileoutput = open(self.__fileoutputpath, "a", encoding="utf-8")


    @property
    def path(self):
        return self.__fileoutputpath

    @property
    def prefix(self):
        return self.__prefix

    def __log(self, scope, prefix, msg, exception = None):
        dt = datetime.utcnow()

        if exception != None and self.__debug == True:
            traceback.print_exception(type(exception), exception, exception.__traceback__)

        if exception == None:
            s = u"%d.%d.%d %d:%d:%d.%d %s: [%s] %s" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, scope.upper(), prefix.upper(), msg)
        else:
            s = u"%d.%d.%d %d:%d:%d.%d %s: [%s] %s #ex: %s" % (
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, scope.upper(), prefix.upper(),
            msg, str(exception))
            
        if self.__fileoutput != None:
            self.__fileoutput.write((s+"\n"))
        r = print(s)

        return r

    def msg(self, msg):
        #return print с("%s: [%s] %s" % (self.SCOPE_MSG.upper(), self.__mPrefix.upper(), msg)).white.on_black
        return self.__log(self.SCOPE_MSG, self.__prefix, msg)
    def warning(self, msg):
        #return print c("%s: [%s] %s" % (self.SCOPE_WRN.upper(), self.__mPrefix.upper(), msg)).orange.on_black
        return self.__log(self.SCOPE_WRN, self.__prefix, msg)
    def error(self, msg, exception = None):
        #return print c("%s: [%s] %s" % (self.SCOPE_ERR.upper(), self.__mPrefix.upper(), msg)).red.on_black
        return self.__log(self.SCOPE_ERR, self.__prefix, msg, exception)

    