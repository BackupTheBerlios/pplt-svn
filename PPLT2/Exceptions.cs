using System;

namespace PPLTExceptions{

/// <summary>This is the base exception for all PPLT specific 
/// Errors.</summary>
class ErrException: Exception{ 
    public ErrException():base(){}
    public ErrException(string Message):base(Message){}
    public ErrException(string Message, params object[] mods):
        base(String.Format(Message,mods)){}
}

/// <summary>This exception will be raised if a "item" ie a symbol, 
/// module... can't be found.</summary>
class ErrItemNotFound: ErrException{
    public ErrItemNotFound():base(){}
    public ErrItemNotFound(string Message):base(Message){}
    public ErrItemNotFound(string Message, params object[] mods):
        base(Message, mods){}
}

/// <summary>This exception will be raise if an item
/// like a module is used for a longer time than the TTL
/// of the message</summary>    
class ErrItemBusy: ErrException { 
    public ErrItemBusy():base(){}
    public ErrItemBusy(string Message):base(Message){}
    public ErrItemBusy(string Message, params object[] mods):
        base(Message, mods){}
}

/// <summary>This exception will be raised if a error accours in a module
/// </summary>  
class ErrModule: ErrException {
    public ErrModule():base(){}
    public ErrModule(string Message):base(Message){}
    public ErrModule(string Message, params object[] mods):
        base(Message,mods){}
}

/// <summary>This exception will be raised if a message can't be processed
/// before his TTL.</summary>
class ErrTimeOut: ErrException {
    public ErrTimeOut():base(){}
    public ErrTimeOut(string Message):base(Message){}
    public ErrTimeOut(string Message, params object[] mods):
        base(Message, mods){}
}


} // END OF NAMESPACE PPLTEXCEPTIONS
