from threading import *
import time;

class Timer(Thread):
    """Call a function after a specified number of seconds:

    t = Timer(30.0, f, args=[], kwargs={})
    t.start()
    t.cancel() # stop the timer's action if it's still waiting
    """

    def __init__(self, interval, function, args=[], kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.fin = False;

    def cancel(self):
        """Stop the timer if it hasn't finished yet"""
        self.fin = True;

    def run(self):
        while not self.fin:
            time.sleep(self.interval);
            if not self.fin:
                self.function(*self.args, **self.kwargs)
            #self.finished.set()

        
