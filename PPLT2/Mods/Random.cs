// created on 15.02.2006 at 14:11
using System;
using PPLTInnerModule;
using PPLTExceptions;
using PPLTMessages;

enum RandAddr{ Bool, Int, Float, String }
    
class RandomGenerator:baseInnerModule, IfInnerModule{   
    protected Random  Rand;
    
    public RandomGenerator(string ID):base(ID){
        this.Rand = new Random();    
    }
    
    protected override void Dispatch(IfMessage msg){
        if(!(msg is IfPopMessage))
            throw new ErrModule("This module can' handle messages of type {0}",
                                  msg);
        
        RandAddr addr = (RandAddr)this.GetChildData(msg);
        switch(addr){
            case RandAddr.Bool:
                if (this.Rand.NextDouble() < 0.5)
                    ((IfPopMessage)msg).Result = true;
                else
                    ((IfPopMessage)msg).Result = false;
                break;
            case RandAddr.Int:
                ((IfPopMessage)msg).Result = this.Rand.Next();
                break;
            case RandAddr.Float:
                ((IfPopMessage)msg).Result = this.Rand.NextDouble();
                break;
            default: throw new ErrModule("Unknown address {0}",(int)addr);
        }    
    }
    
    
    protected override object Map(string Address){
        switch(Address){
            case "Bool": return RandAddr.Bool;
            case "Int": return RandAddr.Int;
            case "Float": return RandAddr.Float;
            default: throw new ErrItemNotFound("Don't know address {0}.",Address);    
        }    
    }
    
    protected override ConnectionType MapType(string Address){
        switch(Address){
            case "Bool": return ConnectionType.Bool;
            case "Int": return ConnectionType.Integer;
            case "Float": return ConnectionType.Double;
            default: throw new ErrItemNotFound("Don't know address {0}.",Address);
        }        
    }        
}