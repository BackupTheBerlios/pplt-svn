using System;
using System.Threading;
using System.Collections;

using PPLTMessages;

namespace PPLTInnerModule{


class qMsgCompare:IComparer{
    public int Compare(object obj1, object obj2){
        MsgPriority pri1 = ((IfMessage)obj1).Priority;
        MsgPriority pri2 = ((IfMessage)obj2).Priority;
        
        if ( pri1 > pri2 ){ return 1; }
        if ( pri1 < pri2 ){ return -1; }
        else{ return 0; }
    }        
}        



/// <summary>This is the messages-queue used by the inner-modules to queue
/// all messages recived.</summary>
public class MessageQueue: ArrayList{
    protected bool  myLock;
    protected IComparer comparer;

    public MessageQueue():base(){
        this.myLock = false;
        this.comparer = new qMsgCompare();
    }
    
    
    public void Add(IfMessage msg){
        if(!this.myLock){
            this.myLock = true;
            return;
        }    
        base.Add(msg);
        msg.Suspend();
    }

    
    public void Next(){
        if (0 == Count) {
            myLock = false;
            return;
        }            
        this.Sort( comparer );
        ((IfMessage)this[0]).Resume(); 
        this.RemoveAt(0);
    }    

}


}
