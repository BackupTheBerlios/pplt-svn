#ifndef PPLTCORE_H
#define PPLTCORE_H

#include "config.h"

#include "Exceptions.h"
#include "Logging.h"
#include "Portability.h"

#include "cObject.h"
#include "cModule.h"
#include "cInnerModule.h"
#include "cConnection.h"
#include "cValueConnection.h"
#include "cFloatConnection.h"
#include "cIntegerConnection.h"
#include "cSequenceConnection.h"
#include "cStreamConnection.h"

#include "cSymbol.h"
#include "cStreamSymbol.h"

// Interfaces:
#include "cDisposable.h"
#include "iFloatModule.h"
#include "iIntegerModule.h"
#include "iNotifyDestruction.h"
#include "iSequenceModule.h"
#include "iStreamModule.h"
#include "iModuleLoader.h"


//Module loader
#include "soModuleLoader.h"


#if HAVE_PYTHON && 1
    #include "cPyModule.h"
    #include "pyModuleLoader.h"
#endif

#endif

