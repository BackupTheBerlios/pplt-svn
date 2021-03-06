import socket;
import thread;
import logging;
import JVisuCMD, JVisuProcess;


def HandleClient(Sock, CAddr, SymbolTree, Server):
    """ Clienthandler """
    Logger = logging.getLogger('pyDCPU');
    Logger.debug("In ClientHander");

    VarHash = {};
    ClientLoop = True;

    #start update-thread:
    #thread.start_new_thread(UpdateThread,(VarHash,ClientLoop))

    while ClientLoop and Server.DoRun():
        # get and handle new commands from client
        try:
            CMD = JVisuCMD.JVisuCMD(Sock=Sock);
            JVisuProcess.JVisuProcess(CMD, VarHash, Sock, SymbolTree);
        except socket.error, (errno, txt):
            if errno == 11:
                # if no new data there...
                pass;
            elif errno == 10035:
                # there was no data (windows code)
                pass;
            else:
                # else:
                Logger.error("Error: %s(%i)"%(txt,errno));
                ClientLoop = False;


    try:
        Sock.close();
    except:
        pass;


#def UpdateThread(VarHash, DoRun):
#    Logger = logging.getLogger("pyDCPU");
#    while DoRun:
#        VarIDList = VarHash.keys();
#        for VarID in VarIDList:
#            Var = VarHash.get(VarID);
#            if Var.NeedUpdate():
#                try:
#                    if not Var.Update():
#                        Logger.warning("Error while update var");
#                    else:
#                        Logger.debug("Var Updated");
#                except:
#                    Logger.warning("Exception while update!, quit ClientHandler");
#                    DoRun = False;
   
