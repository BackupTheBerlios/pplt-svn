// created on 18.02.2006 at 17:57

namespace Logging{
    using System;
    using System.Collections;
    
    /// <summary> All loglevels... </summary>
    enum LogLevel{
        fatal, error, warning, info, debug
    }
    
    // FIXME: type-def for hanlder: delegate
    
    /// <summary> Logger class -> hold all message-handlers 
    class Logger{
        protected LogLevel myLogLevel;
        protected static Hashtable loggers;   
        public delegate Handlers;
        
        public Logger(string name, LogLevel level){
            this.myLogLevel = level;
            if(null != this.loggers)
                this.loggers = new Hashtable();
            if(this.loggers.Contains(name)){
                throw ErrItemBusy("Can't create logger \"{0}\" there is allready a logger with this name.",
                                                  name);
            }
            this.loggers[name] = this;
        }
        
        public Logger(string name):this(name, LogLevel.info){}
        
        
        public static Logger Loggers[name]{
            get{
                if(!this.loggers.Contains(name)
                    throw new ErrItemNotFound("No logger \"{0}\" found.",
                                                                  name);
                return this.loggers[name];
            }    
        }    
        
        
        
        protected void log(string message, LogLevel level){ }
        
        
        public void fatal(string format, params object[] args){
        }
        
        public void error(string format, params object[] args){
        }
        
        public void warning(string format, params object[] args){
        }
        
        public void info(string format, params object[] args){
        }
        
        public void debug(string format, params object[] args){
        }
        
    }
    
}
    
    