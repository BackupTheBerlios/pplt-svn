import pyDCPU;

[...]
try: core = pyDCPU.Core();
except pyDCPU.Error, e:
    print "Unable to instance core: %s"%str(e);
    # handle error...
except:
    # handle exceptions, that aren't raised by the core,
    # this should never hapens -> please contact me if
    # you notice such an exception.
