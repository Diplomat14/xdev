#from termcolor2 import c

class logger(object):
    SCOPE_MSG= "LOG"
    SCOPE_WRN = "WRN"
    SCOPE_ERR = "ERR"
    PREFIX_SEPARATOR = "/"

    __prefix = "-"

    def __init__(self, prefix):
        self.__prefix = prefix

    @classmethod
    def from_prefix(cls,prefix:str):
        return cls(prefix)

    @classmethod
    def from_parent(cls,prefix,parentLogger):
        if parentLogger != None:
            assert isinstance(parentLogger,cls), "Parent object has to be of " + type(cls) + " type"
            prefix = parentLogger.prefix + cls.PREFIX_SEPARATOR + prefix
        return cls(prefix)


    @property
    def prefix(self):
        return self.__prefix

    def __log(self, scope, prefix, msg):
        return print("%s: [%s] %s" % (scope.upper(), prefix.upper(), msg))

    def msg(self, msg):
        #return print с("%s: [%s] %s" % (self.SCOPE_MSG.upper(), self.__mPrefix.upper(), msg)).white.on_black
        return self.__log(self.SCOPE_MSG, self.__prefix, msg)
    def warning(self, msg):
        #return print c("%s: [%s] %s" % (self.SCOPE_WRN.upper(), self.__mPrefix.upper(), msg)).orange.on_black
        return self.__log(self.SCOPE_WRN, self.__prefix, msg)
    def error(self, msg):
        #return print c("%s: [%s] %s" % (self.SCOPE_ERR.upper(), self.__mPrefix.upper(), msg)).red.on_black
        return self.__log(self.SCOPE_ERR, self.__prefix, msg)

    