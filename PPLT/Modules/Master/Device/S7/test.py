import S7Reg;
import S7Message;

Addr = S7Reg.S7Register("AB0");
Comm = S7Message.S7CommandSet(S7Message.S7FunctionWrite,Addr);
Data = S7Message.S7DataSet("\x01",Addr);
Msg  = S7Message.S7Message(Comm,Data);

MsgStr = Msg.GetString();

for char in MsgStr:
    print "%x"%ord(char);
