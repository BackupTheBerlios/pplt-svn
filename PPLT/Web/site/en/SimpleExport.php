        <div class="TextBody">
            <p>I will now discribe how you can access the values stored in the SymbolTree exported
            by the SimpleExport Module. Befor you continue reading I notice you that you need to
            know how setup a Symbol-Tree and how to load Export-Modules. And you need to know something
            about the unser and group managment.</p>

            <div class="Head">Accessing PPLT's Symbol-Tree by SimpleExport</div>
            <div class="Text">
               The SimpleExport is an PPLT export module that use the XML-RPC
               implementation to give you an API to access the values stored in the
               SymbolTree of an running PPLT system.

               <p>Imgine the PPLT system as an server providing some commands to get or
               set values in his Symbol-Tree. In this paper I describe how to write a client
               for this realy simple server. I think it will be the best to show you an
               example sourcecode and then discuss this code step by step.</p>
            </div>

            <div class="Head">A Python client</div>
            <div class="Text">
               In this section I describe how you can access symbols using the Python
               scripting language. But at first the example:
<!-- excuse me but <pre> is ugly //-->
<pre>
#!/usr/bin/python
import xmlrpclib

con = xmlrpclib.server_proxy("http://10.1.1.4:8000/")
print con.Get('/PLC/Marker1')
</pre>
               <p>That's all. Only two lines are needed to get the actual value of the symbol
               "/PLC/Marker1". But now step by step: In the 4th line (i ignore simply the
               existance of the import call) you create a server proxy object. That means that
               this object repesents (proxy) the real server and each methodcall you make
               on this object will be executed in reality on the server. RPC stands for
               Remote Procedure Call. Here you see the sens of this name. After such
               a remote call the result will be send back to the client and in this case
               the value will be returned by the method Get(). You can imagine it like
               telnet or ssh(PuTTY) where all you type into your keyboard will be send to
               the server, executed there and the results were send back to you to be
               displayed on your monitor.</p>

               <p>In the 5th line you make such a remote call of a function. This function
               will return the value of the symbol you've given by the parameter. It is
               your job to find out what kind of value you've got. In the most cases
               you will know it, because you've seted the symbol tree up self. But it
               can be only a bool, integer, float or string value. Meaning all basic
               datatypes python know.</p>

               <p>After this you may ask why you have to know something about the users
               and groups in the symboltree, if this API seems not to need any
               authentification?!?<br>
               You will have to know. As you loaded the SimpleExport module the system
               asked for a <i>default user</i>. This was build in for modules that can't
               make any authentifications. But this can. As long as you doesn't
               login you will run each call of any method as this default user. For
               this reason you should allways use a user with less rights for such
               default accounts. Imagine this user as a guest user like anonymous in
               FTP.</p>

               <p>So let us login.
<pre>
#!/usr/bin/python
import xmlrpclib
import sys;

con = xmlrpclib.server_proxy("http://10.1.1.4:8000")

session = con.LogOn('user','pass')
if not session:
   print "Error while login"
   sys.exit()

print con.Get("/PLC/Marker1",session)
con.LogOff(session);
</pre>
               This does quite the same like the first example but in this case you
               will be logged-in befor you call the Get() method.</p>
               
               <p>A lot of things are different, let's start with the first. The LogOn() call.
               This call need allways two parameters username ans password. You will get back
               a session id. This id is normaly a 128bit hexencoded string. But this you don't
               need to know. You only need to know that if the login fails the method
               will return False, so you can easily check it with the if clause (line:8-10).</p>
               
               <p>If you're successfully logged in you have to add this session id to each 
               call you'll make. If you miss it you will be automatic the default user. So
               don't miss it.</p>
               
               <p>At least you should logout with the LogOff() method. I think this it
               not difficault.</p>

            </div>


            </div>
        </div>
