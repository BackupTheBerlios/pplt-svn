# ############################################################################ #
# This is part of the pyDCPU project. pyDCPU is a framework for industrial     #
# communication.                                                               #
# Copyright (C) 2003-2005 Hannes Matuschek <hmatuschek@gmx.net>                #
#                                                                              #
# This library is free software; you can redistribute it and/or                #
# modify it under the terms of the GNU Lesser General Public                   #
# License as published by the Free Software Foundation; either                 #
# version 2.1 of the License, or (at your option) any later version.           #
#                                                                              #
# This library is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU             #
# Lesser General Public License for more details.                              #
#                                                                              #
# You should have received a copy of the GNU Lesser General Public             #
# License along with this library; if not, write to the Free Software          #
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA    #
# ############################################################################ #



import xml.dom.minidom;
import md5;

class User:
    def __init__(self, Name=None, Password=None, Description=None):
        self.__Name = Name;
        self.__Password = Password;
        self.__Description = Description;





    # ######################################################################## #
    #                                                                          #
    # ######################################################################## #
    def GetName(self):
        return(self.__Name);

    def SetName(self, Name):
        self.__Name = Name;
        return(True);



    def GetPasswd(self):
        return(self.__Password);

    def SetPasswd(self, Passwd):
        self.__Password = md5.new(Passwd).hexdigest();
        return(True);

    def CheckPasswd(self, Passwd):
        if md5.new(Passwd).hexdigest() == self.__Password:
            return(True);
        else:
            return(False);



    def GetDescription(self):
        return(self.__Description);
    def SetDescription(self, Descr):
        self.__Description = Descr;
        return(True);
 




    # ######################################################################## #
    #                                                                          #
    # ######################################################################## #
    def CreateXMLNode(self,Document):
        myNode = Document.createElement("Member");
        NameAttr = Document.createAttribute("name");
        PassAttr = Document.createAttribute("passwd");
        DescAttr = Document.createAttribute("desc");

        NameAttr.nodeValue = self.__Name;
        PassAttr.nodeValue = self.__Password;
        if self.__Description:
            DescAttr.nodeValue = self.__Description;
        else:
            DescAttr.nodeValue = "None";

        myNode.setAttributeNode(NameAttr);
        myNode.setAttributeNode(PassAttr);
        myNode.setAttributeNode(DescAttr);
        return(myNode);
    
