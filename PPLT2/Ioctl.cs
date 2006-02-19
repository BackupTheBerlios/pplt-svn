// created on 15.02.2006 at 01:56
using System;
using System.Collections;
using Mono.Unix.Native;


namespace PPLTIoctl{
    
/// <summary>This is a simple implementation of the Unix ioctl()</summary>
public class Ioctl{
    protected CdeclFunction _ioctl;
    
    public Ioctl(){
        this._ioctl = new CdeclFunction("libc","ioctl",typeof(int));
    }
    
    public int ioctl(int fd, ulong request, params object[] args){
        ArrayList opts = new ArrayList();
        opts.Add(fd); opts.Add(request);
        opts.AddRange(args);
        return (int)this._ioctl.Invoke(opts.ToArray());
    }
}


} // END OF NAMESPACE PPLTIOCTL