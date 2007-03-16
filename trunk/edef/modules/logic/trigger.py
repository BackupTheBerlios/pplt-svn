import edef


class trigger:
    def __init__(self, period="1.0"):
        self._event_manager = edef.EventManager()

        try: self._conf_period = float(period)
        except: self._conf_period=1.0

        self.o_out = edef.BaseOutput()
        self.emmit_tigger()
        
 
    def emmit_tigger(self):
        self.o_out(None)
        self._event_manager.add_scheduled_event(self.emmit_tigger, self._conf_period)

