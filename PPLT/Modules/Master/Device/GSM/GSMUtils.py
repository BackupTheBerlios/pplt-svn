import GSMSMS;

def Reset(Con):
    Con.flush();
    Con.write("ATZ");
    Con.read(100);
    if Con.read(100) == 'OK':
        Con.flush();
        return(True);
    return(False);

def GetServiceCenter(Con):
    Con.flush();
    Con.write('AT+CSCA?');
    Con.read(100);          # get echo ...
    tmp = Con.read(100);
    if tmp == 'ERROR':
        return(None);
    Con.read(100);          # read empty line
    if not Con.read(100) == 'OK':
        return(None);
    if -1 == tmp.find('"'):
        return(None);
    sc = tmp.split('"')[1];
    return("\"%s\""%sc);

def GetManufacturer(Con):
    Con.write('AT+CGMI');
    Con.read(100);      # get echo
    s = Con.read(128);
    if s == 'ERROR':
        return(None);
    Con.read(100);      # read empty line
    if not Con.read(100) == 'OK':
        return(None);
    return(s);

def GetModel(Con):
    Con.write('AT+CGMM');
    Con.read(100);      # get echo
    s = Con.read(128);
    if s == 'ERROR':
        return(None);
    Con.read(100);      # get empty line;
    if not Con.read(100) == 'OK':
        return(None);
    return(s);
    
def GetQuality(Con):
    Con.write('AT+CSQ');
    Con.read(100);      # get echo
    tmp = Con.read(100);
    if tmp == 'ERROR':
        return(None);
    Con.read(100);      # read empty line
    if not Con.read(100) == 'OK':
        return(None);
    tq = tmp.split(' ')[1];
    q = tq.split(',');
    return(q);

def GetBattery(Con):
    Con.write('AT+CBC');
    Con.read(100);      # get echo
    tmp = Con.read(100);
    if tmp == 'ERROR':
        return(None);
    Con.read(100);      # read empty line
    if not Con.read(100) == 'OK':
        return(None);
    tq = tmp.split(' ')[1];
    q = tq.split(',')[1];
    return(q);

def GetNetwork(Con):
    Con.write('AT+CREG?');
    Con.read(100);      # get echo
    tmp = Con.read(100);
    if tmp == 'ERROR':
        return(None);
    Con.read(100);      # read empty line;
    if not Con.read(100) == 'OK':
        return(None);
    tq = tmp.split(' ');
    if len(tq)>1:
        q = tq[1].split(',');
    else:
        return(None);
    return(q);

def SendSMS(Con, Dest, Msg):
    sms = GSMSMS.PDUSMS(Dest,Msg);
    data = sms.SMSToHex();

    if not data:
        return(False);
    print "SMSPDU(hex): %s"%data;
    Con.write("AT+CMGS=%i\x0D%s\x1A"%(int(len(data)/2)-1,data));
    Con.read(300);  #get echo

    tmp = Con.read(100);
    print tmp;
    if not 0 == tmp.find('+CMGC:'):
        print "Error: %s"%tmp;
        return(False);

    return(True);
