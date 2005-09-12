import BaseHTTPServer;
import pyDCPU;
import PPLT;
import string;
import base64;
import sys;
import socket;

#Changelog:
# 2005-08-25:
#   - fixed heavy cpu-load problem 
#       (causes Win8x to crash)
#   - fixed problem with python version < 2.4
# 2005-08-20:
#   - add http-auth 
#   - server will not use the default user anymore.
# 2005-06-10:
#   - fixed problem with non-blocking sockets unter windows.


class PPLTWebServer(BaseHTTPServer.HTTPServer):
    def __init__(self, Address, Handler, ExpSymbolTree):
        BaseHTTPServer.HTTPServer.__init__(self, Address, Handler);
        self.ExpSymbolTree = ExpSymbolTree;
        self.__RUNNING = True;

    def serve_forever(self):
        while self.__RUNNING:
            self.handle_request();

    def Stop(self, Addr, Port):
        self.__RUNNING = False;
        self.socket.setblocking(0);
        self.socket.close();
        tmpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        try: tmpSock.connect( (Addr, Port) );
        except: pass;


class PPLTWebHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):

        # do authenticate:
        auth = self.headers.getheader("Authorization");
        if not auth:
            self.send_response(401);
            self.send_header("www-authenticate","Basic realm=\"PPLTWebServer\"")
            self.end_headers();
            return(None);

        (TYPE, CODE)= auth.split(" ",1);
        if sys.version < "2.4":
            CODE = base64.decodestring(CODE)
        else:
            CODE = base64.b64decode(CODE);
        (USER, PASS)= CODE.split(":",1);

        symbtree = self.server.ExpSymbolTree;
        session = symbtree.Logon(USER, PASS);
        if not session:
            self.send_error(403);
            return(None);

        folders = symbtree.ListFolders(self.path, session);
        if folders  == None:
            self.send_error(404);
            if session : symbtree.Logoff(session);
            return(None);
        self.wfile.write("""<html>
<head>
    <title>PPLT Web-Server</title>
    <style>
        table{ width:100%; border-collapse:collapse; }
        td{padding-left:10px;}
    </style>
</head><body>""");
        self.wfile.write("""<h2 style="padding-left:5px;">Content of %s</h2>"""%self.path);
        self.wfile.write("""<table style="width:100%"><tr style="background-color:#e6b42f"><th>Name</th><th>Value</th></tr>""");
        even = True;
        if self.path != '/':
            self.wfile.write("""<tr><td> <a href="%s">..</a></td><td> Parent Folder</td></tr>"""%PathUp(self.path));
        for folder in folders:
            if even:
                self.wfile.write("""<tr style="background-color:#dddddd">""");
                even = False;
            else:
                self.wfile.write("""<tr style="background-color:#ffffff">""");
                even = True;

            folderaddr = PathAdd(self.path,folder);
            self.wfile.write("""<td><b> <a href="%s">%s</a></b></td><td> [Folder]</td></tr>"""%(folderaddr,folder));
        
        symbols = symbtree.ListSymbols(self.path, session);
        for symbol in symbols:
            if even:
                self.wfile.write("""<tr style="background-color:#dddddd">""");
                even = False;
            else:
                self.wfile.write("""<tr style="background-color:#ffffff">""");
                even = True;
            value = str(symbtree.GetValue(PathAdd(self.path,symbol),session));
            self.wfile.write("<td><b> %s</b></td><td> %s</td></tr>"%(symbol,value));
        self.wfile.write("""</table><p><i>Generated by PPLTWeb - Server Module by Hannes Matuschek</i></p></body></html>""");
        if session: symbtree.Logoff(session);




def PathAdd(path,folder):
    pl = path.split('/');
    npl = [''];
    for dir in pl:
        if dir != '':
            npl.append(dir);
    npl.append(folder);
    return(string.join(npl,'/'));

def PathUp(path):
    pl = path.split('/');
    npl = [];
    for dir in pl:
        if dir != '':
            npl.append(dir);
    if len(npl[:-1])==0:
        return("/");
    return('/'+string.join(npl[:-1],'/'));


class Object(pyDCPU.ExportObject):
    def setup(self):
        self.__BindAddress = self.Parameters.get('Address');
        if not self.__BindAddress:
            self.Logger.error("No Address given...");
            return(False);
        
        self.__Port = None;
        try:
            self.__Port = int(self.Parameters.get("Port"));
        except:
            self.Logger.error("Invalid Port format: have to be a Number as String");
            return(False);
        if self.__Port == None:
            self.Logger.error("No Port given");
            return(False);
        try:
            self.__ServerObject = PPLTWebServer((self.__BindAddress,self.__Port), PPLTWebHandler, self.SymbolTree);
        except:
            self.Logger.error("Error while setup create object");
            return(False);
        if not self.__ServerObject:
            self.Logger.error("No server object");
            return(False);
        return(True);

    def start(self):
        self.__ServerObject.serve_forever();
        return(True);

    def stop(self):
        self.__ServerObject.Stop(self.__BindAddress, self.__Port);
        return(True);

