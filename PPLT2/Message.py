# ########################################################################### #
# This is part of the PPLT project. PPLT is a framework for master-slave      #
# based communication.                                                        #
# Copyright (C) 2003-2006 Hannes Matuschek <hmatuschek@gmx.net>               #
#                                                                             #
# This library is free software; you can redistribute it and/or               #
# modify it under the terms of the GNU Lesser General Public                  #
# License as published by the Free Software Foundation; either                #
# version 2.1 of the License, or (at your option) any later version.          #
#                                                                             #
# This library is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU            #
# Lesser General Public License for more details.                             #
#                                                                             #
# You should have received a copy of the GNU Lesser General Public            #
# License along with this library; if not, write to the Free Software         #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA   #
# ########################################################################### #

import time;
import thread;

import Enums;
import Exceptions;


# BASE_CLASS:
class baseMessage:
    """ The base-class, please used a class derived from this."""
    def __init__(self, direction, TTL=0, priority=Enums.MESSAGE_PRI_NORMAL):
        # check parameters:
        if not (direction in Enums.MESSAGE_DIRECTIONS):
            raise Exceptions.InternalError("Mad message-direction: %s"%str(direction));
        if not (priority in Enums.MESSAGE_PRIORITIES):
            raise Exceptions.IternalError("Mad message-priority: %s"%str(priority));
        #set values:    
        self._TimeToLife = TTL;
        self._CreateTime = time.time();
        self._MessageDirection = direction;
        self._MessagePriority = priority;

    def getPriority(self): return self._MessagePriority;
    def getDirection(self): return self._MessageDirection;
    def isOutOfTime(self):
        if self._TimeToLife <= 0: return False;
        if (self._CreateTime+self._TimeToLife) < time.time(): return True;
        return False;
    def timeElapsed(self):
        return (time.time()-self.CreateTime)/self._TimeToLife;

  
  
# LOCK:
class lockMessage (baseMessage):
    """ The lockMessage:
 This message should be send by a module to reserve the upper or lower part
 of the module-tree. This prevents other modules on the locked 
 module-tree-part to emit messages. Think of it like a "shut-off" of the 
 interrups."""
 
    def __init__(self, direction, TTL=0, priority=Enums.MESSAGE_PRI_NORMAL, threadID=None):
        """ Construktor:
 The parameter direction specifies the direction of the message. This can be
 one of MESSAGE_UP or MESSAGE_DOWN. MESSAGE_UP specifies that the message will
 run the module-tree up, that means in the direction to the symbols (leafes).
 
 The optional parameter TTL specifies the time-to-life in seconds. This is a 
 possibility to unlock the module-tree if a module missed to unlock the tree. 
 But the module have to had completed all work in this time-period. By default
 the value will be set to 0 that means that the lock will never expire. 
 
 The optional parameter priority specifies the message-priority. By default
 it will be MESSAGE_PRI_NORMAL. 

 The optional parameter threadID specifies the id of the thread that get the 
 lock. This is by default the id of the current thread. Note: Only the
 thread with the same id can unlock the symboltree!""" 

        baseMessage.__init__(self, direction, TTL, priority);
        # save thread ID:
        if not threadID: self._ThreadID = thread.get_ident();
        else: self._ThreadID = threadID;

    def getThreadID(self): return self._ThreadID;



# UNLOCK: 
class unlockMessage (baseMessage):
    """ This message unlocks the module-tree locked by a lockMessage: """
    
    def __init__(self, direction, threadID=None):
        """ Constructor:
 The parameter direction specifies the direction of the message. This can be 
 one of (MESSAGE_UP, MESSAGE_DOWN). 
 
 The optional parameter threadID specifies the id of the thread that locked 
 the tree!  By default this is the id of the current thread. Note: only the
 thread that locks the tree can unlock it!"""        
        baseMessage.__init__(self, direction);
        # save thread-id:
        if not threadID: self._ThreadID = thread.get_ident();
        else: self._ThreadID = threadID;

    def getThreadID(self): return self._ThreadID;



# POP-MESSAGE:
class popMessage (baseMessage):
    """ This is the popMessage:
 The popMessage requests data or a value from the reciver."""

    def __init__(self, direction, length=1, TTL=0, priority=Enums.MESSAGE_PRI_NORMAL):
        """ Constructor:
 The parameter direction specifies the direction of the message; this should 
 be one of (MESSAGE_UP,MESSAGE_DOWN)!
 
 The optional parameter length specifies the (max.) length of the requested 
 data.  If you request a value or a data-sequenec (like a singe packet) set 
 length to 1 (default).
 
 The parameter TTL specifies the time-to-life for this message. Until this 
 time-period the message should return with content or a TimeOut will raised!
 
 The parameter priority specifies the message priority; by defaut it is
 MESSAGE_PRI_NORMAL."""
        baseMessage.__init__(self, direction, TTL, priority);
        self._MessageData = None;
        self._Length = length;
        
    def getData(self): return self._MessageData;
    def setData(self, data): self._MessageData = data;
    def getLength(self): return self._Length;
    def setLength(self, length): self._Length=length;



# PUSH-MESSAGE:
class pushMessage (baseMessage):
    """ This is the pushMessage; 
 with this message you can push data or a value to an other module."""
 
    def __init__(self, direction, data, TTL=0, priority=Enums.MESSAGE_PRI_NORMAL):
        """ Constructor:
 The parameter direction specifies the direction of the message. This should 
 be one of (MESSAGE_UP, MESSAGE_DOWN).
 
 The parameter data specifies the data or the value that will be pushed.
 
 The optional parameter TTL specifies the time-to-life for the message.
 By default this is 0, meaning that the message never expires.
 
 The optional parameter priority specifies the priority of the message;
 by default this will be MESSAGE_PRI_NORMAL."""
        baseMessage.__init__(self, direction, TTL, priority);
        self._MessageData = data;
    
    def getData(self): return self._MessageData;
    def setData(self, data): self._MessageData = data;
