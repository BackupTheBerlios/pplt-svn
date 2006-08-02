TEMPLATE = app
TARGET   = test

CONFIG += qtestlib debug

unix:LIBS += -L/opt/pplt2/lib -lppltcore

SOURCES = main.cc soModuleLoaderTest.cc libPPLTCoreTest.cc CoreModuleTest.cc
HEADERS = libPPLTCoreTest.h

INCLUDEPATH += ../
INSTALLS = .

