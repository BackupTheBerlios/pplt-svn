// created on 15.02.2006 at 16:23
using System;
using PPLTMessages;
using PPLTInnerModule;

// TODO: Let Symbol has a queue.
// TODO: Let Symbol has a cache.

namespace PPLTSymbol{
    
    public class Symbol:IfAttachable{
        protected string myName;
        protected string myID;
        protected MsgReciver myParent;
        protected ConnectionType myType;
        
        public Symbol(string ID, string Name){
            this.myID = ID;
            this.myName = Name;
        }
        
        public string Identifier{
            get { return this.myID; }
        }
        
        public MsgReciver Parent{
            set { this.myParent = value; }
        }
        
        public ConnectionType ParentType{
            get { return this.myType; }
            set { this.myType = value; }
        }
        
        public ConnectionType Type{
            get{ return this.myType;}
        }
            
        public void Queue(IfMessage msg){
            this.Dispatch(msg);
        }    
        
        public object Value{
            get{
                PopMessage msg = new PopMessage(0);
                msg.Reciver = this.myParent;
                msg.SenderID = this.myID;
                msg.Emit();
                return msg.Result;
            }
            set{
                PushMessage msg = new PushMessage(0, MsgPriority.Normal,
                                                   value);
                msg.Reciver = this.myParent;
                msg.SenderID = this.myID;
                msg.Emit();
            }    
        }
        
        public void Dispatch(IfMessage msg){
        }            
    }
}    