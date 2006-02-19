using System;
using System.Collections;
using System.Threading;

namespace PPLTInnerModule{
    
    using PPLTMessages;
    using PPLTExceptions;
    
    ///<summary> One of this types a module/symbol can have.</summary>
    public enum ConnectionType{
        Stream, Bool, Integer, Double,
        String
    }
    
    /// <summary>Interface for all items that wants to be attached
    /// to a inner module.</summary>    
    public interface IfAttachable{
        string         Identifier { get; }
        MsgReciver     Parent { set; }
        ConnectionType ParentType { get; set; }
        void            Queue(IfMessage msg);
    }

    /// <summary>Interface for inner modules.</summary>
    public interface IfInnerModule: IfAttachable{
        void        Register(IfAttachable Child);
        void        Register(IfAttachable Child, string Addr);
        void        Dispatch(IfMessage msg);
        object      Map(string Address);
    }
    
    
    
    /// <summary>Base class for the internal modules.</summary>
    public class baseInnerModule{
        protected string          myModuleObjID;  // ObjectID : can be used to identify the module
        protected MessageQueue   myQueue;        // my Queue
        protected MsgReciver     myParent;       // the queue of my parent.
        protected ConnectionType myParentType;  // type of connection to parent.
        protected Hashtable      myChildren;     // map addr -> Queue(s)
        protected Hashtable      myChildAddr;    // map ID -> addr;
        protected Hashtable      myChildData;    // map ID -> user-data
        protected string          myReservedBy;   // ID of child that reserved this module.

        /// <summary>Constructor</summary>
        public baseInnerModule(string ID){
            this.myModuleObjID  = ID;
            this.myQueue        = new MessageQueue();
            this.myChildren     = new Hashtable();
            this.myChildData    = new Hashtable();
            this.myChildAddr    = new Hashtable();
        }   
    
        public MsgReciver Parent{
            set{ this.myParent = value; }
        }
        
        public ConnectionType ParentType{
            get { return this.myParentType; }
            set { this.myParentType = value; }
        }
        
        public string Identifier{
            get{ return this.myModuleObjID; }
        }
    
        protected object GetChildData(IfMessage msg){
            return this.myChildData[msg.SenderID];
        }
        protected string GetChildAddr(IfMessage msg){
            return (string)this.myChildAddr[msg.SenderID];
        }


        /// <summary>This method queues the incomming messages.</summary>
        /// <remarks>This method queues all incomming messages and suspend
        /// there threads untils the current message is done. Then the next
        /// message will be wakeed-up.
        public void Queue(IfMessage msg){
            // check if this module is reserved by the sender:
            if (null != this.myReservedBy && this.myReservedBy == msg.SenderID){
                // This block handles all messages from sender who reserved this 
                // module.
                // If free-msg -> unlock this module (and parent) and call Queue.Next();
                if(msg is IfFreeMessage){
                    this.myReservedBy = null;     // free my self
                    // if this module has a parent -> free them! 
                    try{ if(null != this.myParent){ this.EmitToParent(msg); } }  
                    finally{ this.myQueue.Next(); }
                // ignore multible reservations!                
                }else if(msg is IfReserveMessage){ return;
                } else{ this.Dispatch(msg); // handle "normal" mesages
                } 
            // This block handles messages from all modules that don't reserved 
            // this module.             
            }else{
                // queue message    
                this.myQueue.Add(msg);
                // if the message is a "reserve" message:
                if (msg is IfReserveMessage){
                    // try to reserve parent (if exists):
                    if(null != this.myParent){ this.EmitToParent(msg); }
                    this.myReservedBy = msg.SenderID; // reserve my self. 
                    return; // do not call Queue.Next()!
                // Handle "normal" Messages:    
                }else{
                    // call dispatcher and wake-up next in queue;
                    try{ this.Dispatch(msg);}
                    finally{ this.myQueue.Next(); }    
                }                
            }         
        }



        /// <summary>This method will be called by the system to register a new 
        /// child-module to this module.</summary>
        public void Register(IfAttachable Child, string Addr){
            string  ChildID = Child.Identifier;
            
            // map no address to "" address:
            if( null == Addr){ Addr = ""; }
            // add message-reciver to table:
            if(!this.myChildren.Contains(Addr)){
                this.myChildren[Addr] = (MsgReciver)Child.Queue;
            }else{ 
                MsgReciver tmp = (MsgReciver)this.myChildren[Addr];
                tmp += Child.Queue;
                this.myChildren[Addr] = tmp;
            }
            // save data and address in table:
            this.myChildData[ChildID] = this.Map(Addr);
            Child.ParentType = this.MapType(Addr);
            this.myChildAddr[ChildID] = Addr;
            // set "parent of child"
            Child.Parent = this.Queue;
        }
        
        public void Register(IfAttachable Child){ this.Register(Child, null); }
        
        /// <summary>This method can be used by the Dispatch() method to emmit new
        /// messages to the parent.</summary>
        protected void EmitToParent(IfMessage msg){
            // if this module is reserved by an other:
            // dont' emmit free an reserve messages.
            if((msg is ReserveMessage || msg is FreeMessage) &&
               null != this.myReservedBy){
                return;                   
            }                           
            msg.SenderID = this.myModuleObjID;
            msg.Reciver = this.myParent;
            msg.Emit();
        }

        protected void EmitToChild(IfDatagram msg, string to){
            if (null == to){ to = ""; }
            if (!this.myChildren.Contains(to)){
                throw new ErrItemNotFound("No child with addr \"{0}\" registred to this module", to);
            }
            //Console.WriteLine("emitting...");
            msg.SenderID = this.myModuleObjID;
            msg.Reciver = (MsgReciver)this.myChildren[to];
            msg.Emit();
        }
    
        protected virtual void Dispatch(IfMessage msg){}
        protected virtual object Map(string Addr){ return null; }
        protected virtual ConnectionType MapType(string Addr){
            return ConnectionType.Stream;
        }   
    }



}
