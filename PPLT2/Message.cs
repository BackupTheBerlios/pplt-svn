using System;
using System.Threading;
using PPLTExceptions;
using PPLTInnerModule;


namespace PPLTMessages{

/// <summary>Baseclass for all messages.</summary>
/// <remarks>This is the base-class. Please don't use it to implement your 
/// messages. Use <see cref="ReserveMessage">ReserveMessage</see>, 
/// <see cref="FreeMessage">FreeMessage</see>, <see cref="PushMessage">
/// PushMessage</see>, <see cref="PopMessage">PopMessage</see> or
/// <see cref="Datagram">Datagram</see> instead.</remarks>
public class baseMessage{
    protected Thread       myThread;
    protected MsgPriority	myPriority;
    protected MsgReciver   myReciver;
    protected long			myCreateTime;
    protected int 			myTimeToLife;
    protected string        mySenderID;

    public baseMessage(int TTL, MsgPriority priority){ // {{{
        this.myPriority	= priority;
        this.myTimeToLife	= TTL;
        this.myThread		= Thread.CurrentThread;
        this.myCreateTime = DateTime.Now.Ticks;
    }
    //}}}
    public baseMessage(int TTL): this(TTL, MsgPriority.Normal){}

    
    public void Suspend(){ 	this.myThread.Suspend(); } 
    public void Resume(){ this.myThread.Resume(); }

	/// <summary>Emits the message to the reciver.</summary>
    public virtual void Emit(){ 
        this.myReciver((IfMessage)this);
    }

	/// <summary>By this property you can set/get the reciver for
	/// the message</summary>
    public  MsgReciver Reciver{
        get { return this.myReciver; }
        set { this.myReciver = value; }
    }

	///<summary>This property returns the priority of the message.</summary>
	///<remarks>This is not allway the priority the message was created with.
	/// it is a feature, that the priority of a message rises with time so that
	/// messages that are waiting for a longer time than others will have a 
	/// higher priority. By default the message will get one level for each
	/// 25% of life time. So it can get max 3 stages.</remarks>
    public MsgPriority Priority{
        get {
        	if (this.myTimeToLife <= 0)
        		return this.myPriority;
        	// calculate dyn. priority:
        	int t_left = (int)((DateTime.Now.Ticks - this.myCreateTime)/10000);
        	int p_up   = (int)(4*(t_left/this.myTimeToLife));
        	if((int)this.myPriority >= p_up)
        		return this.myPriority - p_up;
        	return MsgPriority.Highest;
        }
        set { this.myPriority = value; }
    }    

	///<summary>Returns the id of the sender!</summary>
    public string SenderID{
        get{ return this.mySenderID; }
        set{ this.mySenderID = value; }
    }        
}    


/// <summary>Baseclass for all data-messages.</summary>
/// <remarks>This is a base-class. Please don't use it to implement your 
/// messages. Use <see cref="ReserveMessage">ReserveMessage</see>, 
/// <see cref="FreeMessage">FreeMessage</see>, <see cref="PushMessage">
/// PushMessage</see>, <see cref="PopMessage">PopMessage</see> or
/// <see cref="Datagram">Datagram</see> instead.</remarks>
public class baseDataMessage: baseMessage{
    protected object    myData;
    protected object    myResult;

    public baseDataMessage(int TTL, MsgPriority pri, object data): base(TTL, pri){
        this.myData = data;
    }
    public baseDataMessage(int TTL, MsgPriority pri): this(TTL, pri, null){}
    public baseDataMessage(int TTL): this(TTL, MsgPriority.Normal, null){ }
    
    ///<summary>By this property you can set/get the data of this
    /// message.</summary>
    public object Data{
        get{ return this.myData; }
        set{ this.myData = value; }
    }

    public object Result{
        get{ return this.myResult; }
        set{ this.myResult = value; }
    }        
}



/// <summary>Baseclass for all thread-messages.</summary>
/// <remarks>This is a base-class. Please don't use it to implement your 
/// messages. Use <see cref="ReserveMessage">ReserveMessage</see>, 
/// <see cref="FreeMessage">FreeMessage</see>, <see cref="PushMessage">
/// PushMessage</see>, <see cref="PopMessage">PopMessage</see> or
/// <see cref="Datagram">Datagram</see> instead.</remarks>
public class baseThreadMessage: baseMessage{

    public baseThreadMessage(int TTL, MsgPriority pri):base(TTL, pri){
        // set the Emit() method of the base class as the method the new 
        // thread will start with.
        this.myThread = new Thread( new ThreadStart(base.Emit) );
    }
    
    public baseThreadMessage(int TTL): this(TTL, MsgPriority.Normal){}

    
    public override void Emit(){ 
        if(this.myThread.IsAlive){ base.Emit(); }
        else{ this.myThread.Start(); }
    }    
        
}    



/// <summary>Enumeration of all message-priorities.</summary>
/// <remarks>The messages are used in the inter-message communication. To 
/// prevent collisions each module has its own message-queue. To influence
/// the order of the waiting messages you have the possiblility to set a 
/// priority for each message. This enumeration holds all priorities 
/// available.</remarks>
public enum MsgPriority{ Highest, High, Normal, Low, Lowest}


///<summary>Base-interface for all messages.</summary>
///<remarks>This interface will be used by all methods of the modules that
/// have to deal will all message-types. You can use it to write seperate
/// dispatch-methods for each message-type be overloading the Dispatch() 
/// method of the <see cref="baseInnerModule">module</see>.
/// For example:
/// <code>
/// class myModule:baseInnerModule, IfInnerModule{
/// (...)
///     protected void Dispatch(IfMessage msg){
///         // do nothing by default
///     }
///     protected void Dispatch(IfPushMessage msg){
///         // handle push-messages
///     }
///     protected void Dispatch(IfPopMessage msg){
///         // handle pop-messages
///     }
///     protected void Dispatch(IfDatagram msg){
///         // handle data-telegrams.
///     }
/// (...)
/// }
/// </code></remarks>
public interface IfMessage{
    MsgPriority Priority { get; set; }      
    MsgReciver  Reciver { get; set; }   
    string      SenderID { get; set; }

    void        Emit();

    void        Suspend();
    void        Resume();
}




///<summary>Data message. This message can contain data.</summary>
public interface IfPushMessage: IfMessage{
    object Data { get; set; }
    object Result { get; set; }
}
public interface IfPopMessage: IfMessage{
    int Length { get; set; }
    object Result { get; set; }
}
public interface IfReserveMessage: IfMessage{
}
public interface IfFreeMessage: IfMessage{
}
public interface IfDatagram: IfMessage{
    object Data { get; set; }
}


public class ReserveMessage: baseMessage,IfReserveMessage{
    public ReserveMessage(int TTL, MsgPriority pri): base(TTL, pri) {}
    public ReserveMessage(int TTL): base(TTL, MsgPriority.Normal) {}
}


public class FreeMessage: baseMessage,IfFreeMessage{
    public FreeMessage(int TTL, MsgPriority pri): base(TTL, pri) {}
    public FreeMessage(int TTL): base(TTL, MsgPriority.Normal) {}
}


public class PushMessage: baseDataMessage,IfPushMessage{
    public PushMessage(int TTL, MsgPriority pri, object data): base(TTL, pri, data){}
    public PushMessage(int TTL, MsgPriority pri): base(TTL, pri, null){}
    public PushMessage(int TTL): base(TTL, MsgPriority.Normal, null){}
}


public class PopMessage: baseMessage,IfPopMessage{
    protected int       myLength;
    protected object    myResult;

    public PopMessage(int TTL, MsgPriority pri, int length): base(TTL, pri){
        this.myLength = length;
    }
    public PopMessage(int TTL, MsgPriority pri): this(TTL, pri, -1){}
    public PopMessage(int TTL): this(TTL, MsgPriority.Normal, -1){}

    
    public int Length{
        get{ return this.myLength; }
        set{ this.myLength = value; }
    }

    public object Result{
        get{ return this.myResult; }
        set{ this.myResult = value; }
    }        
}


public class Datagram: baseThreadMessage,IfDatagram{
    protected object    myData;
    
    public Datagram(int TTL, MsgPriority pri, object data): base(TTL, pri) { this.myData = data; }
    public Datagram(int TTL, MsgPriority pri): this(TTL,pri,null){}
    public Datagram(int TTL): this(TTL, MsgPriority.Normal, null){}

    public object Data{
        get{ return this.myData; }
        set{ this.myData = value; }
    }
}


public delegate void MsgReciver(IfMessage msg);

} // END OF NAMESPACE.
