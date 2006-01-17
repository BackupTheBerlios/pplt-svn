import pyDCPU;
[...]
try: core.DoSomeThing();
except pyDCPU:
    # Handle exceptions from core
except Exception:    
    # Handle exception raised not by core;
    # this will be often an error! So, please 
    # contact the author if you notice an 
    # exception that is not derived from the
    # base-exception-class pyDCPU.Error!!!
