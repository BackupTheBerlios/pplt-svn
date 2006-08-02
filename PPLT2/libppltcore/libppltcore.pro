TEMPLATE = lib
TARGET   = ppltcore
VAERSION = 2.0.0


SOURCES  = cConnection.cpp cDisposable.cpp cFloatConnection.cpp \
           cInnerModule.cpp cIntegerConnection.cpp cModule.cpp cObject.cpp \
           cSequenceConnection.cpp cStreamConnection.cpp cStreamSymbol.cpp \
           cSymbol.cpp cValueConnection.cpp Exceptions.cpp Logging.cpp \
           LogOutputter.cpp soModuleLoader.cc

HEADERS  = cConnection.h cDisposable.h cFloatConnection.h \
           cInnerModule.h cIntegerConnection.h cModule.h cObject.h \
           cSequenceConnection.h cStreamConnection.h cStreamSymbol.h \
           cSymbol.h cValueConnection.h Exceptions.h Logging.h \
           soModuleLoader.h iFloatModule.h iIntegerModule.h \
           iModuleLoader.h iNotifyDestruction.h iSequenceModule.h \ 
           iStreamModule.h


DESTDIR  = /opt/pplt2/lib
CONFIG   += debug qt exceptions

DEFINES  += HAVE_EXECINFO
