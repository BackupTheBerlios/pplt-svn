""" The eventmanager is the central element of the I{edef} system. It handles
    events emmitted by outputs and can also generate timed events. 
    
    If an output is updates it does not set the new value directly to all 
    inputs, that are connected to it. Because this can cause a recursive 
    loop. To avoid this, the I{edef} system uses an eventmanager. If an output
    is updated the output will tell the eventmanager which inputs have to be 
    updated with the new value and the eventmanager will do this job. 
    
    Additionally a module can tell the eventmanager to call a spcific method 
    in a period of time (timed event). This can be helpfull if a module needs 
    to poll for values. 
    
    The eventmanager is implemented as a singleton (by subclassing the 
    L{Singleton} class). You does not need to instance a eventmanager by your 
    self. At the latest the first output created will do this for you. But you
    need an instance to stop the eventmanager. To stop an eventmanager do:
    C{edef.EventManager().stop()}. """

# ########################################################################## #
# EventManager.py
#
# 2007-01-18
# Copyright 2007 Hannes Matuschek
# hmatuschek@gmx.net
# ########################################################################## #
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# ########################################################################## #


import threading
import logging
import time
from Singleton import Singleton


class EventManager(threading.Thread):
    """ This is the event-manager. The event-manager is the central part of
        edef. It queues all events emmited by the output and redirect them to
        the inputs. Additionaly this manager can provide scheduled events.
        This are events, that happen after a defined period of time. 
        
        This class is implemented as a singelton.  This ensures that there is 
        only one instance of this class in each application and you'll never 
        need to init. If a component needs an instance of this class it will 
        instance it or will get a reference on it. 
        
        Note that you need to stop the eventmanager by calling 
        C{EventManager().stop()}!"""

    _d_event_list   = None
    _d_sched_events = None
    _d_is_alive     = None
    _d_condition    = None
    _d_logger       = None
    _d_instance     = None
    


    __metaclass__=Singleton
    def __init__(self):
        """ Constructor. This constructor will init the instance and the 
            event-thread. This thread of control will wait until an event
            arrives. The thread will process it. """
        self._d_event_list = []
        self._d_sched_events = []
        self._d_is_alive = True
        self._d_condition = threading.Condition()
        self._d_logger = logging.getLogger("edef.core")

        # Fix for windows: It needs to call the time.clock() function at 
        #   least once to start the clock-counter!
        #time.clock()

        threading.Thread.__init__(self)
        self._d_logger.info("Init event-handler (id:%i)"%id(self))
        self.start()
   


    def stop(self):
        """ This method will stop the event-thread and waits until the thread 
            joined. Also it will destroy the singeton. But there may survive 
            some references to the EventManager, but it will not longer accept 
            any events. """
        # Notify event-handler-thread to exit:
        self._d_condition.acquire()
        self._d_is_alive = False
        self._d_condition.notify()
        self._d_condition.release()
        # Wait for thread to join
        if self.isAlive():
            self._d_logger.debug("Stop Eventmanager -> Join thread")
            self.join()
        EventManager._d_instance = None



    def run(self):
        """ This method will be called by the contructor as a new thread. 
            Never call this method direct! Simply forget that it exists! 
            """
        self._d_logger.debug("Start event-handler")
        # Event-Loop
        while (self._d_is_alive):
            self._d_condition.acquire()
            if len(self._d_event_list) == 0 and not self._sched_event_pending():
                if len(self._d_sched_events) > 0:
                    (nxt_event, cb, args) = self._d_sched_events[0]
                    timeout = nxt_event - time.time()
                    self._d_logger.debug("Events pending, check in %f sec.",timeout)
                else: timeout = None                
                self._d_condition.wait(timeout)
            
            if not self._d_is_alive:
                self._d_logger.debug("Eventhandler stopped...")
                return
            
            if self._sched_event_pending():
                (to, callback, params) = self._d_sched_events.pop(0)
                self._d_condition.release()
                self._d_logger.debug("Process scheduled event: %s(%s)"%(callback.__name__, params))
                try: callback(**params)
                except: self._d_logger.exception("Exeption while exec event-callback")
                continue

            elif len(self._d_event_list) > 0:
                (callback, value) = self._d_event_list.pop(0)
                self._d_condition.release()
            
            else:
                self._d_condition.release()
                continue
           
            self._d_logger.debug("Calling %s(%s)"%(callback.__name__,value))
            try:
                callback(value)
            except Exception, e:
                self._d_logger.exception("Exeption while exec event-callback")
        
        self._d_logger.debug("Stop event-handler")



    def add_event(self, cb, value):
        """ This method will put the given callback and value on the 
            event-queue. If the event is processed the event-manager
            will call cb(value). Norally this method will be invoked by 
            outputs to emmit a changed value. Call this only if you know what
            you are doing. """

        if not self._d_is_alive:
            raise Exception("EventManager stoped: No events where processed.")
        
        self._d_condition.acquire()
        self._d_event_list.append((cb,value))
        self._d_condition.notify()
        self._d_logger.info("Added %s(%s); Event queue contains now: %i elments."%(cb.__name__, value, len(self._d_event_list)))
        self._d_condition.release()



    def add_scheduled_event(self, cb, timeout, params={}):
        """ This method adds a scheduled event to the queue. The event-manager
            will call cb(**kwargs) after a period of time defined by time. """
        # FIXME make an scheduled event cancelable?
        self._d_condition.acquire()
        self._d_sched_events.append( (time.time()+timeout, cb, params) )
        self._d_sched_events.sort(cmp=_EventManager_sched_compare)
        self._d_condition.notify()
        self._d_condition.release()



    def _sched_event_pending(self):
        """ Internal used method. Simply tests if there are some scheduled 
            events, that should be processed now."""
        #self._d_logger.debug("Scheduled events pending: %i"%len(self._d_sched_events))
        if len(self._d_sched_events) == 0:
            return False

        (timestamp, cb, args) = self._d_sched_events[0]
        if timestamp <= time.time():
            return True





def _EventManager_sched_compare(tpl1, tpl2):
    """ Intenal used function to compare two scheduled-events in repect to 
        time. Used to order scheduled events by time."""
    (time1, cb, args) = tpl1
    (time2, cb, args) = tpl2
    if time1 == time2: return 0
    elif time1 < time2: return -1
    elif time2 < time1: return 1



