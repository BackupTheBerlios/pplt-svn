# ###
# testLock module:
#  This module implements an other (time based) module locking. It can be 
#  unsed to test the module-locking of the PPLT system. Normaly a module will 
#  be locked by a call of the lock() method and will be unlocked by a call of 
#  the unlock() method. This module will be also locked by a call of the 
#  lock() method but it will be unlocked after 5 sec automaticly.

from testLock import Object;


