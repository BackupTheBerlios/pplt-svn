// created on 16.02.2006 at 14:58
using System;
using PPLTMessages;
using PPLTInnerModule;
using PPLTExceptions;


class HexDump:baseInnerModule, IfInnerModule{
    public HexDump(string ID):base(ID){
    }
    
    protected override void Dispatch(IfMessage msg){
        if(msg is Datagram){
            Console.WriteLine("Datagram from patent: {0}",
                                ((Datagram)msg).Data);
            this.EmitToChild((Datagram)msg,null);
        }
        if(msg is PopMessage){
            this.EmitToParent(msg);
            Console.WriteLine("PopMessage from child. Result: {0}",
                                ((PopMessage)msg).Result);
        }
        if(msg is PushMessage){
            Console.WriteLine("PushMessage from child. Data: {0}",
                                ((PushMessage)msg).Data);
            this.EmitToParent(msg);
        }    
    }
    
    protected override object Map(string Address){
        if(null != Address && "" != Address)
            throw new ErrModule("This module knows no address.");
        return null;
    }
    
    protected override ConnectionType MapType(string Address){
        if(null != Address && "" != Address)
            throw new ErrModule("This module known no address!");
        return this.ParentType;
    }
    
    
    private string hex_encode(object data){
            return null;
    }
}