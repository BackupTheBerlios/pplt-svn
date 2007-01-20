import threading
import logging
import time


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




class EventManager(threading.Thread):
    """ This is the event-manager. The event-manager is the central part of
        edef. It queues all events emmited by the output and redirect them to
        the inputs. Additionaly this manager can provide scheduled events.
        This are events, that happen after a defined period of time. 
        
        This class is implemented as a singelton, means that you should 
        instance this class only by calling the instance() method. This 
        ensures that there is only one instance of this class in each 
        application and you'll never need to init. If a component needs an
        instance of this class it will instance it or will get a reference on
        it. """

    _d_event_list   = None
    _d_sched_events = None
    _d_is_alive     = None
    _d_condition    = None
    _d_logger       = None
    _d_instance     = None
    


    def instance():
        """ Singleton implementation. """
        if EventManager._d_instance is None:
            EventManager._d_instance = EventManager()
        return EventManager._d_instance
    instance = staticmethod(instance)



    def __init__(self):
        """ Constructor. This constructor will init the instance and the 
            event-thread. This thread of control will wait until an event
            arrives. The thread will process it. """
        self._d_event_list = []
        self._d_sched_events = []
        self._d_is_alive = True
        self._d_condition = threading.Condition()
        self._d_logger = logging.getLogger("PPLT.core")

        # Fix for windows: It needs to call the time.clock() function at 
        #   least once to start the clock-counter!
        time.clock()

        threading.Thread.__init__(self)
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
        self._d_logger.debug("Stop Eventmanager -> Join thread")
        self.join()
        # destroy singleton!
        EventManager._d_instance = None



    def run(self):
        self._d_logger.debug("Start event-handler")

        # Event-Loop
        while (self._d_is_alive):
            
            self._d_condition.acquire()
            if len(self._d_event_list) == 0 and not self._sched_event_pending():
                if len(self._d_sched_events) > 0:
                    (nxt_event, cb, args) = self._d_sched_events[0]
                    timeout = nxt_event - time.clock()
                else: timeout = 0                    
                self._d_condition.wait(timeout)
            
            if not self._d_is_alive:
                break
            
            if self._sched_event_pending():
                (callback, kwargs) = self._d_sched_events.pop(0)
                self._d_condition.release()
            elif len(self._d_event_list) > 0:
                (callback, value) = self._d_event_list.pop(0)
                self._d_condition.release()
            else:
                self._d_condition.release()
                continue
           
            self._d_logger.debug("Calling %s with %s"%(id(callback),value))
            try:
                callback(value)
            except Exception, e:
                self._d_logger.exception("Exeption while exec event-callback")
        
        self._d_logger.debug("Stop event-handler")



    def add_event(self, cb, value):
        """ This method will put the give callback and value on the 
            event-queue. If the event is processed the event-manager
            will call cb(value). """
        if not self._d_is_alive:
            raise Exception("EventManager stoped: No events where processed.")
        self._d_condition.acquire()
        self._d_event_list.append((cb,value))
        self._d_condition.notify()
        self._d_logger.info("Event queue contains now: %s"%self._d_event_list)
        self._d_condition.release()



    def add_scheduled_event(self, cb, time, **kwargs):
        """ This method adds a scheduled event to the queue. The event-manager
            will call cb(**kwargs) after a period of time defined by time. """
        # FIXME make an scheduled event cancelable?^
        self._d_condition.acquire()
        self._d_sched_events.append( (time.clock()+time, cb, kwargs) )
        self._d_sched_events.sort(cmp=_EventManager_sched_compare)
        self._d_condition.notify()
        self._d_condition.release()



    def _sched_event_pending(self):
        """ Internal used method. """
        if len(self._d_sched_events) == 0:
            return False

        (timestamp, cb, args) = self._d_sched_events[0]
        if timestamp <= time.clock():
            return True





def _EventManager_sched_compare(tpl1, tpl2):
    """ Intenal used function to compare two scheduled-events in repect to 
        time. """
    (time1, cb, args) = tpl1
    (time2, cb, args) = tpl2
    if time1 == time2: return 0
    elif time1 < time2: return -1
    elif time2 < time1: return 1



