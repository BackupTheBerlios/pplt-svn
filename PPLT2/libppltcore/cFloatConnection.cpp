/***************************************************************************
 *            cFloatConnection.cpp
 *
 *  Fri Apr 28 14:13:02 2006
 *  Copyright  2006  Hannes Matuschek
 *  hmatuschek@gmx.net
 ****************************************************************************/
 
#include "cFloatConnection.h"


using namespace PPLTCore;


cFloatConnection::cFloatConnection(cModule *parent, cDisposable *child)
: cValueConnection(parent,child){
    if(0 == dynamic_cast<iFloatModule *>(parent)){
        throw Error("Unable to cast parent module to iFloatModule!"\
                    " Need a FloatModule as parent for a FloatConnection!");
    }    
}

void cFloatConnection::push(double value){
    // save the pushed value into the cache and update value-timestamp:
    d_cached_value = value;
    UpdateTimestamp();
    
    // if events are enabled for this connection -> notify_child()
    if(events_enabled())
        notify_child();
}



// will be called by the parent module to get the last value...
double cFloatConnection::pop( void ){
    return d_cached_value;
}



/* GET method: will be called like: value = connection.get(); */
double cFloatConnection::get(){
    iFloatModule    *mod;
 
    // if the cached value is still up to date -> return it.
    if(!CacheTimeElapsed()){
        CORELOG_DEBUG("Return cached value: "<< d_cached_value);
        return d_cached_value;
    }
    
    // try to cast parent-module to a float-module!
    if(0 == (mod = dynamic_cast<iFloatModule *>(d_parent_module)) ){
        throw CoreError("Unable to cast parent module to iFloatModule! A"\
                        "a cFloatConnection needs a iFloatModule as parent!");
    }
    
    CORELOG_DEBUG("Update iternal cache...");
    // lock parent
    if(autolock())
        d_parent_module->reserve();
    // try to get new value:
    try{
        d_cached_value = mod->get_float(Identifier());
    }catch(...){
        // on error release and rethrow exception.
        if(autolock())
            d_parent_module->release();
        throw;
    }
    // release parent
    if(autolock())
        d_parent_module->release();
    // update timestamp and return value.
    UpdateTimestamp();
    
    return d_cached_value;        
}   



void cFloatConnection::set(double value){
    iFloatModule  *mod;
    
    // check cast to iIntegerModule:
    if(0 == (mod = dynamic_cast<iFloatModule *>(d_parent_module)) )
        throw CoreError("Unable to cast parent module to iFloatModule! "
                        "But a cFloatConnection needs a iFloatModule!");
    
    // lock parent
    if(autolock())
        d_parent_module->reserve();
    
    // try to get new value
    try{ 
        mod->set_float(Identifier(), value);
    }catch(...){
        // on error: unlock parent and rethrow exception.
        if(autolock()){ d_parent_module->release(); }
        throw;
    }
    // unlock parent
    if(autolock()){ d_parent_module->release(); }
    
    // if success -> save new value in cache:
    d_cached_value = value;
    UpdateTimestamp();
}



int cFloatConnection::Integer(){
    return (int)get();
}   

void cFloatConnection::Integer(int value){
    set((double) value);
}


double cFloatConnection::Float(){ 
    return get();
}

void cFloatConnection::Float(double value){
    set(value);
}


std::string cFloatConnection::String(){
    //TODO: Implement!
    throw NotImplementedYet("cFloatConnection::String() is not implemented yet!");
}

void cFloatConnection::String(std::string value){
    throw NotImplementedYet("cFloatConnection::String(value) is not implemented yet!");
}
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     /c++/4.0.2/bits/stl_raw_storage_iter.h \
  /usr/include/c++/4.0.2/limits \
  /usr/include/c++/4.0.2/bits/stl_function.h \
  /usr/include/c++/4.0.2/bits/basic_string.h \
  /usr/include/c++/4.0.2/bits/atomicity.h \
  /usr/include/c++/4.0.2/i586-suse-linux/bits/atomic_word.h \
  /usr/include/c++/4.0.2/algorithm /usr/include/c++/4.0.2/bits/stl_algo.h \
  /usr/include/c++/4.0.2/bits/stl_heap.h \
  /usr/include/c++/4.0.2/bits/stl_tempbuf.h \
  /usr/include/c++/4.0.2/bits/basic_string.tcc \
  /usr/include/c++/4.0.2/list /usr/include/c++/4.0.2/bits/stl_list.h \
  /usr/include/c++/4.0.2/bits/list.tcc /usr/include/c++/4.0.2/map \
  /usr/include/c++/4.0.2/bits/stl_tree.h \
  /usr/include/c++/4.0.2/bits/stl_map.h \
  /usr/include/c++/4.0.2/bits/stl_multimap.h Logging.h \
  /usr/include/c++/4.0.2/iostream /usr/include/c++/4.0.2/ostream \
  /usr/include/c++/4.0.2/ios /usr/include/c++/4.0.2/bits/localefwd.h \
  /usr/include/c++/4.0.2/bits/ios_base.h \
  /usr/include/c++/4.0.2/bits/locale_classes.h \
  /usr/include/c++/4.0.2/streambuf \
  /usr/include/c++/4.0.2/bits/streambuf.tcc \
  /usr/include/c++/4.0.2/bits/basic_ios.h \
  /usr/include/c++/4.0.2/bits/streambuf_iterator.h \
  /usr/include/c++/4.0.2/bits/locale_facets.h \
  /usr/include/c++/4.0.2/cwctype \
  /usr/include/c++/4.0.2/i586-suse-linux/bits/ctype_base.h \
  /usr/include/c++/4.0.2/i586-suse-linux/bits/ctype_inline.h \
  /usr/include/c++/4.0.2/bits/codecvt.h \
  /usr/include/c++/4.0.2/i586-suse-linux/bits/time_members.h \
  /usr/include/c++/4.0.2/i586-suse-linux/bits/messages_members.h \
  /usr/include/c++/4.0.2/bits/basic_ios.tcc \
  /usr/include/c++/4.0.2/bits/ostream.tcc /usr/include/c++/4.0.2/locale \
  /usr/include/c++/4.0.2/bits/locale_facets.tcc \
  /usr/include/c++/4.0.2/typeinfo /usr/include/c++/4.0.2/istream \
  /usr/include/c++/4.0.2/bits/istream.tcc /usr/include/c++/4.0.2/sstream \
  /usr/include/c++/4.0.2/bits/sstream.tcc /usr/include/c++/4.0.2/fstream \
  /usr/include/c++/4.0.2/i586-suse-linux/bits/basic_file.h \
  /usr/include/c++/4.0.2/bits/fstream.tcc Exceptions.h \
  /usr/include/execinfo.h /opt/pplt2/include/wx-2.6/wx/strconv.h \
  /opt/pplt2/include/wx-2.6/wx/buffer.h \
  /opt/pplt2/include/wx-2.6/wx/fontenc.h \
  /opt/pplt2/include/wx-2.6/wx/string.h \
  /opt/pplt2/include/wx-2.6/wx/beforestd.h \
  /opt/pplt2/include/wx-2.6/wx/afterstd.h \
  /opt/pplt2/include/wx-2.6/wx/arrstr.h \
  /opt/pplt2/include/wx-2.6/wx/iosfwrap.h \
  /opt/pplt2/include/wx-2.6/wx/regex.h cDisposable.h cObject.h \
  iNotifyDestruction.h
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       