# -*- encoding: utf-8 -*-
import binascii;

GSM_ENCODING = {u'@':0x00, u'£':0x01, u'$':0x02, u'¥':0x03, u'è':0x04, u'é':0x05, u'ù':0x06, u'ì':0x07,
                u'ò':0x08, u'Ç':0x09, "\n":0x0A, u'Ø':0x0B, u'ø':0x0C, "\r":0x0D, u'Å':0x0E, u'å':0x0F,
                u'Δ':0x10, u'_':0x11, u'Φ':0x12, u'Γ':0x13, u'Λ':0x14, u'Π':0x15, u'Ψ':0x16, u'Σ':0x17,
                u'Σ':0x18, u'Θ':0x19, u'Ξ':0x1A, "\x0c":0x1B0A, u'^':0x1B14, u'{':0x1B28, u'}':0x1B29,
                u'\\':0x1B2F, u'[':0x1B3C, u'~':0x1B3D, u']':0x1B3E, u'|':0x1B40, u'€':0x1B65, u'Æ':0x1C,
                u'æ':0x1D, u'ß':0x1E, u'É':0x1F, u' ':0x20, u'!':0x21, u'"':0x22, u'#':0x23, u'¤':0x24,
                u'%':0x25, u'&':0x26, u"'":0x27, u'(':0x28, u')':0x29, u'*':0x2A, u'+':0x2B, u',':0x2C,
                u'-':0x2D, u'.':0x2E, u'/':0x2F, u'0':0x30, u'1':0x31, u'2':0x32, u'3':0x33, u'4':0x34,
                u'5':0x35, u'6':0x36, u'7':0x37, u'8':0x38, u'9':0x39, u':':0x3A, u';':0x2B, u'<':0x3C,
                u'=':0x3D, u'>':0x3E, u'?':0x3F, u'¡':0x40, u'A':0x41, u'B':0x42, u'C':0x43, u'D':0x44,
                u'E':0x45, u'F':0x46, u'G':0x47, u'H':0x48, u'I':0x49, u'J':0x4A, u'K':0x4B, u'L':0x4C,
                u'M':0x4D, u'N':0x4E, u'O':0x4F, u'P':0x50, u'Q':0x51, u'R':0x52, u'S':0x53, u'T':0x54,
                u'U':0x55, u'V':0x56, u'W':0x57, u'X':0x58, u'Y':0x59, u'Z':0x5A, u'Ä':0x5B, u'Ö':0x5C,
                u'Ñ':0x5D, u'Ü':0x5E, u'§':0x5F, u'¿':0x60, u'a':0x61, u'b':0x62, u'c':0x63, u'd':0x64,
                u'e':0x65, u'f':0x66, u'g':0x67, u'h':0x68, u'i':0x69, u'j':0x6A, u'k':0x6B, u'l':0x6C,
                u'm':0x6D, u'n':0x6E, u'o':0x6F, u'p':0x70, u'q':0x71, u'r':0x72, u's':0x73, u't':0x74,
                u'u':0x75, u'v':0x76, u'w':0x77, u'x':0x78, u'y':0x79, u'z':0x7A, u'ä':0x7B, u'ö':0x7C,
                u'ñ':0x7D, u'ü':0x7E, u'à':0x7F};


def String2GSMList(str):
    Liste = [];
    for char in str:
        # map char to GSM-Code or to 0x20(' ') if not known
        code = GSM_ENCODING.get(char,0x20);
        if code <= 127:
            Liste.append(code);
        else:
            Liste.append( (code&0xff00)>>8);
            Liste.append( (code&0x00ff));
    return(Liste);

def IsInternational(Number):
    if len(Number)<2:
        return(False);
    if Number[0] == '+':
        return(True);
    else:
        return(False);

def EncodeNumber(Number):
    if not Number or Number=='':
        return(None);

    inter = IsInternational(Number);

    BCD = [];
    if inter:
        pos = 1;
        BCD.append(0x91);
    else:
        pos = 0;
        BCD.append(0x81);

    nibble = 0;
    byte = 0x00;
    len = 0;
    for digit in Number[pos:]:
        len +=1;
        if nibble:
            byte |= (int(digit)&0x0F)<<4;
        else:
            byte |= (int(digit)&0x0F);
        nibble = (nibble+1)%2;
        if nibble == 0:
            BCD.append(byte);
            byte = 0x00;

    if nibble:
        byte |= 0xF0;
        BCD.append(byte);

    if len > 255:
        return(None);
    BCD.insert(0,len);
    return(BCD);


def GSMPack(MSG):
    List = String2GSMList(MSG);
    shift = 0;
    byte  = 0x00;
    buff  = [];
    for item in List:
        if shift == 0:
            byte = (int(item)&0x7F);
        elif shift == 1:
            byte |= (int(item)&0x01)<<7
            buff.append(byte);
            byte = (int(item)&0x7F)>>1;
        elif shift == 2:
            byte |= (int(item)&0x03)<<6;
            buff.append(byte);
            byte = (int(item)&0x7F)>>2;
        elif shift == 3:
            byte |= (int(item)&0x07)<<5;
            buff.append(byte);
            byte = (int(item)&0x7F)>>3;
        elif shift == 4:
            byte |= (int(item)&0x0F)<<4;
            buff.append(byte);
            byte = (int(item)&0x7F)>>4;
        elif shift == 5:
            byte |= (int(item)&0x1F)<<3;
            buff.append(byte);
            byte = (int(item)&0x7F)>>5;
        elif shift == 6:
            byte |= (int(item)&0x3F)<<2;
            buff.append(byte);
            byte = (int(item)&0x7F)>>6;
        elif shift == 7:
            byte |= (int(item)&0x7F)<<1;
            buff.append(byte);
        shift = (shift+1)%8;

    if shift:
        buff.append(byte);

    if len(List)>255:
        return(None);
    buff.insert(0,len(List));
    return(buff);


            




class PDUSMS:
    def __init__(self, DEST, MSG):
        self.__Dest = DEST;
        self.__DestBCD = EncodeNumber(DEST);
        self.__Msg = MSG;
        self.__SMSCLen = 0x00;                      #Use internal SMSC-Number
        self.__MsgFlag = 0x11;                      #Use dafault MsgFlags
        self.__UKB      = 0xFF;
        self.__MsgRefNum = 0x00;                    #No reference number
        self.__ProtoID = 0x00;                      #Default
        self.__DCodeScheme = 0x00;                  #Default
        self.__MsgData = GSMPack(self.__Msg);       #pack Msg to GSM Format 8->7Bit packing

    def SMSToData(self):
        sms = '';
        sms += chr(self.__SMSCLen);
        sms += chr(self.__MsgFlag);
        sms += chr(self.__MsgRefNum);
        for char in self.__DestBCD:
            sms += chr(char);
        sms += chr(self.__ProtoID);
        sms += chr(self.__DCodeScheme);
        sms += chr(self.__UKB);
        for char in self.__MsgData:
            sms += chr(char);
        return(sms);

    def SMSToHex(self):
        data = self.SMSToData();
        hexdata = '';
        for char in data:
            hexdata += "%02X"%ord(char);
        return(hexdata);
    
