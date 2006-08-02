TEMPLATE    = lib
TARGET      = ppltcoremodules

CONFIG      += debug plugin
DESTDIR     = /opt/pplt2/plugins

INSTALLS = 

VERSION     = 2.0.0a

SOURCES     = HexDumpModule.cc HexifierModule.cc LoopbackModule.cc \
              NULLModule.cc RandomModule.cc TimeModule.cc

HEADERS     = HexDumpModule.h HexifierModule.h LoopbackModule.h \
              NULLModule.h RandomModule.h TimeModule.h
