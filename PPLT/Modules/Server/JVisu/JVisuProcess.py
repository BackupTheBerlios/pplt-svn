from JVisuTypes import *;
import JVisuVar;
from JVisuConverter import ToValue;
import logging;

def JVisuProcess(CMD, VarHash, Sock, SymbolTree):
    Logger = logging.getLogger("pyDCPU");
    if CMD.GetCMD() == JVISU_CMD_REGVAR:
        Var = JVisuVar.JVisuVar(CMD.GetData(),
                                CMD.GetID(),
                                CMD.GetRate(),
                                CMD.GetType(),
                                SymbolTree,
                                Sock);
        ID = CMD.GetID();
        Logger.debug("register var %i"%ID);
        VarHash.update( {ID:Var} );
        return(True);
    elif CMD.GetCMD() == JVISU_CMD_DELVAR:
        ID = CMD.GetID();
        if VarHash.has_key(ID):
            del VarHash[ID];
            Logger.debug("Var %i removed"%ID);
            return(True);
        Logger.warning("Var %i unknown"%ID);
        return(False);
    elif CMD.GetCMD() == JVISU_CMD_SNDVAR:
        ID = CMD.GetID();
        Logger.debug("Set Value of var %i"%ID);
        if VarHash.has_key(ID):
            Value = ToValue(CMD.GetData(),CMD.GetType());
            Var = VarHash[ID];
            if not Var.SetValue(Value):
                Logger.warning("Error while set Value");
                # test if symbol exist
    return(False);
