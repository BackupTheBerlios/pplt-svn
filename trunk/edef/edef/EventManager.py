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
import weakref
from Singleton import Singleton
import sys
import types

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
        C{EventManager().shutdown()}!"""

    _d_event_list   = None
    _d_sched_events = None
    _d_finish_events= False

    _d_is_alive     = None

    _d_condition    = None
    
    _d_pause_lock   = None
    _d_signal_pause = None
    
    _d_logger       = None
   

    __metaclass__=Singleton
    def __init__(self, starts_now=False):
        """ Constructor. This constructor will init the instance and the 
            event-thread. If the optional argument is left or C{False} the 
            EventManager will be started in pause mode."""

        self._d_event_list      = []
        self._d_sched_events    = []
        self._d_finish_events   = False

        self._d_is_alive        = True
        self._d_condition       = threading.Condition()
        self._d_logger          = logging.getLogger("edef.core")
        
        self._d_signal_toresume = threading.Event()
        self._d_signal_ispaused = threading.Event()
        self._d_signal_isresumed= threading.Event()

        threading.Thread.__init__(self)
        self._d_logger.info("Init event-handler (id:%i)"%id(self))
        
        self._d_signal_toresume.clear()
        self.start()    # start event-manager thread
        
        # wait untill mngr is paused:
        self._d_logger.debug("On init: Pause evt-mngr!")
        self._d_signal_ispaused.wait()
        
        if starts_now:
            self.resume()
         

    def resume(self):
        """ This method will start the event-handler. It should be called 
            after the event-manager was instanced and to resume the 
            event-manager after a C{pause()} call. """
        self._d_logger.debug("Signal mngr to resume")
        self._d_signal_toresume.set()   # resume paused EventManager
        #self._d_logger.debug("Wait until mngr is resumed")
        self._d_signal_isresumed.wait() # wait for thread to resume 
        self._d_logger.debug("Mngr is running")
       

    def pause(self):
        """ This method will pause the event-manager. This method blocks until
            the current event was processed. You can resume the 
            event-processing by calling the C{start()} method. """
        # FIXME DEADLOCK> check if the calling thread isn't the event-handling
        #                 thread! 
        if self.isPaused():
            self._d_logger.info("Mngr allready paused!")
            return

        self._d_condition.acquire()
        self._d_logger.debug("Signal mngr to pause")
        self._d_signal_toresume.clear() # set state to pause
        self._d_condition.notify()      # signal "event"
        self._d_condition.release()
        
        #self._d_logger.debug("Wait until mngr sleeps")
        self._d_signal_ispaused.wait() # wait for evt-mngr to be paused
        self._d_logger.debug("Mngr is paused")


    def finish(self, timeout=1.0):
        """ This method will block until all queued events are processed or 
            the given timeout elaps. The default timeout is 1 sec. This method
            will allways left the EventManager in a pause state. You can 
            resume the EventManager by calling the C{start()} method. This 
            method returns C{True} if the event-manager successfully finished 
            his job or C{False] if a timeout occures."""
        # FIXME DEADLOCK> check if the calling thread isn't the event-handling
        #                 thread! 
        self._d_logger.debug("Let mngr finish his job")
        if self.isPaused():
            self._d_logger.debug("Mngr is paued -> seems like his finished")
            return True # If it is allready paused
        
        self._d_condition.acquire()
        self._d_finish_events = True    # tell event-manager to finisch
        self._d_condition.notify()      # signal "event"
        self._d_condition.release()

        if self._d_signal_ispaused.isSet():
            # if mngr should run but not reseted pause signal
            # wait until he runs and then retry to finish:
            self._d_logger.debug("Mngr not paused and not running again -> wait for!")
            self._d_signal_isresumed.wait()
            return self.finish(timeout)

        #self._d_logger.debug("Is signal_paused (%s) and isPaused (%s)?"%(self._d_signal_ispaused.isSet(), self.isPaused()))
        
        #self._d_logger.debug("Wait until mngr is paused")
        self._d_signal_ispaused.wait(float(timeout)) # wait until he gets paused (by him self)
        #self._d_logger.debug("Manager is paused now -> finished")
        
        self._d_finish_events = False   # reset finish-flag
        if not self.isPaused():         # if event-mgr is not paused (timeout)
            self.pause()                # force him to pause even if there 
            return False                # are events left to process
        return True


    def shutdown(self):
        """ This method will stop the event-thread and waits until the thread 
            joined. Also it will destroy the singeton. But there may survive 
            some references to the EventManager, but they will not longer 
            accept any events. """
        # FIXME DEADLOCK> check if the calling thread isn't the event-handling
        #                 thread! 
        # Notify event-handler-thread to exit:
        self._d_condition.acquire()
        self._d_is_alive = False    # signal to shutdown
        self._d_signal_toresume.set()    # wakeup paused EventManager
        self._d_condition.notify()  # signal "event"
        self._d_condition.release()
        # Wait for thread to join
        if self.isAlive():
            self._d_logger.debug("Stop Eventmanager -> Join thread")
            self.join()
        EventManager._d_instance = None


    def clear(self):
        """ Removes all events from event-queue. """
        self._d_condition.acquire()
        if len(self._d_event_list) > 0:
            del self._d_event_list[0:]
        if len(self._d_sched_events) > 0:
            del self._d_sched_events[0:]
        self._d_condition.release()


    def isPaused(self):
        """ This method will return C{True} if the EventManager is in the
            pause mode. This method will event return C{True} if the last
            event is still processed. """
        return not self._d_signal_toresume.isSet()


    def run(self):
        """ This method will be called by the contructor as a new thread. 
            Never call this method directly! Simply forget that it exists! """
        
        self._d_logger.debug("Start event-handler")
        # Event-Loop
        while (self._d_is_alive):
            # blocks here if state is "paused"
            self._blocks_on_pause()
            if not self._d_is_alive: continue

            self._d_condition.acquire()
            # if there are no events and finish() was called:
            if len(self._d_event_list) == 0 and len(self._d_sched_events) == 0 and self._d_finish_events:
                self._d_signal_toresume.clear()  # set my self into pause
                self._d_condition.release()
                continue

            if len(self._d_event_list) == 0 and not self._sched_event_pending() and not self.isPaused():
                if len(self._d_sched_events) > 0:
                    (nxt_event, cb, args) = self._d_sched_events[0]
                    timeout = nxt_event - time.time()
                    #self._d_logger.debug("Events pending, check in %f sec.",timeout)
                else: timeout = None                
                #self._d_logger.debug("Wait for events (%s)"%timeout)
                self._d_condition.wait(timeout)
                #self._d_logger.debug("Got an event -> process")
            
            if not self._d_is_alive or self.isPaused():
                self._d_condition.release()
                continue
            
            # process pending schduled events:
            if self._sched_event_pending():
                (to, callback, params) = self._d_sched_events.pop(0)
                self._d_condition.release()
                try:
                    self._d_logger.debug("Process scheduled event: %s(%s)"%(callback.__name__, params))
                    callback(**params)
                except:
                    self._d_logger.exception("Exeption while exec event-callback")
                continue
            
            # process "normal" events:
            elif len(self._d_event_list) > 0:
                (callback, value) = self._d_event_list.pop(0)
                self._d_condition.release()
                try:
                    self._d_logger.debug("Calling %s(%s)"%(getattr(callback,"__name__",callback),value))
                    callback(value)
                except Exception, e:
                    self._d_logger.exception("Exeption while exec event-callback")
             
            # this should not happen:
            else:
                self._d_condition.release()
            
            #END OF "while self._d_is_alive"
        self._d_logger.debug("Stop event-handler")


    def add_event(self, cb, value):
        """ This method will put the given callback and value on the 
            event-queue. If the event is processed the event-manager
            will call cb(value). Norally this method will be invoked by 
            outputs to emmit a changed value. Call this only if you know what
            you are doing. """
        if not self._d_is_alive:
            raise Exception("EventManager stoped: No events where processed.")
        
        # store event-callback as a weak-reference:
        if type(cb) == types.MethodType:
            cb = InstanceMethodProxy(cb)
            # cb = weakref.proxy(cb)
        else: self._d_logger.warning("No reference created for %s"%cb)

        self._d_condition.acquire()
        self._d_event_list.append((cb,value))
        self._d_condition.notify()
        self._d_condition.release()
        self._d_logger.debug("Added %s(%s); Event queue contains now: %i elments."%(getattr(cb,"__name__",cb), value, len(self._d_event_list)))



    def add_scheduled_event(self, cb, timeout, params={}):
        """ This method adds a scheduled event to the queue. The event-manager
            will call cb(**kwargs) after a period of time defined by time. """
        # FIXME make an scheduled event cancelable?
        self._d_logger.debug("Add scheduled event: %s(%s) in %fs"%(getattr(cb,'__name__',cb), params, timeout))
        
        if not self._d_is_alive:
            raise Exception("EventManager stoped: No events where processed.")
        
        # store callback as a weak-reference:
        if type(cb) == types.MethodType:
            cb = InstanceMethodProxy(cb)
            # cb = weakref.proxy(cb)

        # store event:
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

    
    def _blocks_on_pause(self):
        if not self.isPaused(): return
        #self._d_logger.debug("Signal to wait for resume")
        self._d_signal_ispaused.set()   # signals that EventManager gets paused
        self._d_signal_isresumed.clear()
        #self._d_logger.debug("Wait for resume")
        self._d_signal_toresume.wait()     # wait for resume
        #self._d_logger.debug("Resumed! Signal this...")
        self._d_signal_ispaused.clear() # signals EventManager resumed    
        self._d_signal_isresumed.set()


def _EventManager_sched_compare(tpl1, tpl2):
    """ Intenal used function to compare two scheduled-events in repect to 
        time. Used to order scheduled events by time."""
    (time1, cb, args) = tpl1
    (time2, cb, args) = tpl2
    if time1 == time2: return 0
    elif time1 < time2: return -1
    elif time2 < time1: return 1




class InstanceMethodProxy:
    _object_ref = None
    _funct_name = None

    def __init__(self, meth):
        self._logger = logging.getLogger("edef.core")
        assert type(meth) == types.MethodType
        self._object_ref = weakref.ref(meth.im_self)
        self._funct_name = meth.im_func.__name__
        self.__name__ = self._funct_name
        
        self._logger.debug("Refcount of instance %s"%sys.getrefcount(meth.im_self))


    def __call__(self, *args, **kwargs):
        if not self._object_ref():
            self._logger.info("Input destucted -> skip event")
            return
        meth = getattr(self._object_ref(), self._funct_name)
        meth(*args, **kwargs)


