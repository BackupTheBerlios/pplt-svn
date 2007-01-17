import threading
import logging
import time


class EventManager(threading.Thread):
    _d_event_list   = None
    _d_sched_events = None
    _d_is_alive     = None
    _d_condition    = None
    _d_logger       = None
    _d_instance     = None
    
    
    def factory():
        """ Singleton implementation. """
        if EventManager._d_instance is None:
            EventManager._d_instance = EventManager()
        return EventManager._d_instance
    factory = staticmethod(factory)


    def __init__(self):
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
        self._d_condition.acquire()
        self._d_event_list.append((cb,value))
        self._d_condition.notify()
        self._d_logger.info("Event queue contains now: %s"%self._d_event_list)
        self._d_condition.release()


    def add_scheduled_event(self, cb, time, **kwargs):
        # FIXME make an scheduled event cancel
        self._d_condition.acquire()
        self._d_sched_events.append( (time.clock()+time, cb, kwargs) )
        self._d_sched_events.sort(cmp=_EventManager_sched_compare)
        self._d_condition.notify()
        self._d_condition.release()


    def _sched_event_pending(self):
        if len(self._d_sched_events) == 0:
            return False

        (timestamp, cb, args) = self._d_sched_events[0]
        if timestamp <= time.clock():
            return True



def _EventManager_sched_compare(tpl1, tpl2):
    (time1, cb, args) = tpl1
    (time2, cb, args) = tpl2
    if time1 == time2: return 0
    elif time1 < time2: return -1
    elif time2 < time1: return 1
