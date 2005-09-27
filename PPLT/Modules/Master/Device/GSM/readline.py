def read(Con, LineEnd):
    buff = "";
    lineend = False;

    while not lineend:
        buff = buff + Con.read(1);
        pos = buff.find(LineEnd);
        if pos != -1:
            line = buff.strip(LineEnd); #remove lineendings
            lineend = True;
    return line;
    
