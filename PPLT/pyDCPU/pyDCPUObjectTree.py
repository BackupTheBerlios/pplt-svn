# ############################################################################ #
# This is part of the pyDCPU project. pyDCPU is a framework for industrial     # 
#   communication.                                                             # 
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

import copy;

class pyObjectNode:
    def __init__(self,ObjectID,Logger):
        self.ID = ObjectID;
        self.Logger = Logger;
        self.Children = [];
        self.ChildrenHash = {};     #Hashtable between childid an his parameter/address/class hash
                                    #to provide searching a loaded module with the same configuration
        self.Parent = None;

    def AddChild(self,NewNode):
        for Node in self.Children:
            if Node.ID == NewNode.ID:
                self.Logger.warning("Can't add child twice");
                return(False);
        self.Children.append(NewNode);
        NewNode.Parent = self;
        #self.Logger.debug("Child added");
        return(True);

    def DelChild(self,ChildID):
        for Node in self.Children:
            if Node.ID == ChildID:
                if 0 != len(Node.Children):
                    self.Logger.warning("Can't del (because child has children");
                    return(False);
                else:
                    self.Children.remove(Node);
                    del Node;
                    self.Logger.debug("Child Deleted...");
                    return(True);
        self.Logger.warning("Child not Found");
        return(False);

    def List(self):
        childlist = [];
        for child in self.Children:
            childlist.append(child.GetID());
        return(childlist);

    def search(self,ChildID):
        if self.ID == ChildID:
            #self.Logger.debug("Obj Found...");
            return(self);

        for Node in self.Children:
            Found = Node.search(ChildID);
            if Found:
                return(Found);
        return(None);

    def ToXML(self, Document, Core):
        obj = Core.ObjectToXML(Document,self.ID);
        for child in self.Children:
            cnode = child.ToXML(Document, Core);
            if cnode:
                obj.appendChild(cnode);
            else:
                del cnode;
        return(obj);

    def GetID(self):
        return(self.ID);

class pyObjectTree:
    def __init__(self,Logger):
        self.Logger = Logger;
        self.Children = [];

    def Add(self,ParentID,ChildID):
        if not ParentID:
            self.Children.append(pyObjectNode(ChildID,self.Logger));
            #self.Logger.debug("Object added");
            return(True);
        
        Parent = self.Find(ParentID);
        if Parent:
            if not Parent.AddChild(pyObjectNode(ChildID,self.Logger)):
                self.Logger.warning("Error while add child");
                return(False);
            #self.Logger.debug("Child added");
            return(True);
        self.Logger.warning("Can't Find Parent");
        return(False);

    def Del(self, ObjectID):
        Object = self.Find(ObjectID);
        if Object:
            if Object.Parent:
                if Object.Parent.DelChild(ObjectID):
                    self.Logger.debug("Child deleted");
                    return(True);
                else:
                    self.Logger.warning("Error while del child");
                    return(False);

            if len(Object.Children)!=0:
                self.Logger.warning("Object has children!");
                return(False);
            self.Children.remove(Object);
            del Object;
            self.Logger.debug("Child deleted");
            return(True);
        else:
            self.Logger.warning("Object not found");
            return(False);
        

    def Find(self,ObjectID):
        for Node in self.Children:
            Found = Node.search(ObjectID);
            if Found:
                #self.Logger.debug("Child found");
                return(Found);
        self.Logger.warning("Child not Found");
        return(None);


    def List(self, ParentID):
        childlist = []
        if not ParentID:
            for child in self.Children:
                childlist.append(child.GetID());
            return(childlist);
        Found = self.Find(ParentID);
        if not Found:
            return(None);
        return(Found.List());


    def ToXML(self, ParentNode, Document, Core):
        for child in self.Children:
            cnode = child.ToXML(Document, Core);
            if cnode:
                ParentNode.appendChild(cnode);
            else:
                del cnode;
        return(True);
